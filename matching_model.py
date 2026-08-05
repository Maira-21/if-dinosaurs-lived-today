"""
If Dinosaurs Lived Today - Climate Suitability Model
------------------------------------------------------
A simplified Species Distribution Model (SDM) style scorer.
Compares a dinosaur's estimated paleoclimate envelope (temperature,
precipitation, humidity) against a modern region's climate normals,
and produces a suitability score, a survival probability estimate,
and a natural-language explanation.

This is a demonstration-grade model. Real SDM tools (e.g. MaxEnt)
use much larger occurrence datasets and additional variables
(soil, elevation, land cover, competition). Treat outputs here as
directionally illustrative, not scientific fact.
"""

import json
import math
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def load_data():
    with open(DATA_DIR / "dinosaurs.json") as f:
        dinosaurs = json.load(f)
    with open(DATA_DIR / "regions.json") as f:
        regions = json.load(f)
    return dinosaurs, regions


def variable_score(value, low, high):
    """
    Returns 1.0 if value falls inside [low, high].
    Falls off smoothly (Gaussian-style) the further outside the range it is.
    """
    if low <= value <= high:
        return 1.0
    width = max(high - low, 1e-6)
    sigma = width * 0.6
    distance = low - value if value < low else value - high
    return math.exp(-(distance ** 2) / (2 * sigma ** 2))


def score_region(dino, region):
    """
    Returns a dict with the overall suitability score (0-100),
    per-variable sub-scores, and a survival probability estimate.
    """
    t_score = variable_score(region["temp_c"], *dino["temp_range_c"])
    p_score = variable_score(region["precip_mm"], *dino["precip_range_mm"])
    h_score = variable_score(region["humidity_pct"], *dino["humidity_range_pct"])

    # Temperature and precipitation matter most for large-animal survival;
    # humidity is a secondary but still relevant factor.
    suitability = (t_score * 0.40 + p_score * 0.35 + h_score * 0.25) * 100

    # Simplified diet-based adjustment: this is NOT modeling real food
    # webs, just a small illustrative penalty reflecting that predators
    # additionally depend on modern prey availability, which this model
    # does not have data for.
    diet_modifier = 0.90 if dino["diet"] == "herbivore" else 0.82
    survival_probability = round(suitability * diet_modifier, 1)

    return {
        "region_id": region["id"],
        "region_name": region["name"],
        "lat": region["lat"],
        "lon": region["lon"],
        "suitability": round(suitability, 1),
        "survival_probability": max(0.0, min(100.0, survival_probability)),
        "temp_score": round(t_score * 100, 1),
        "precip_score": round(p_score * 100, 1),
        "humidity_score": round(h_score * 100, 1),
    }


def explain(dino, region_result):
    """Generates a plain-language explanation of the suitability score."""
    parts = []
    subscores = {
        "temperature": region_result["temp_score"],
        "rainfall": region_result["precip_score"],
        "humidity": region_result["humidity_score"],
    }
    best = max(subscores, key=subscores.get)
    worst = min(subscores, key=subscores.get)

    parts.append(
        f"{region_result['region_name']} scores {region_result['suitability']}% "
        f"suitable for {dino['name']}."
    )
    if subscores[best] >= 85:
        parts.append(f"Its {best} closely matches the species' Mesozoic habitat range.")
    if subscores[worst] < 60:
        parts.append(f"However, its {worst} deviates significantly from what {dino['name']} was adapted to.")
    if subscores[worst] >= 60 and subscores[best] < 85:
        parts.append("Overall climate conditions are a moderate but imperfect match.")

    confidence_note = {
        "high": "Paleoclimate envelope sourced from direct proxy data (CLAMP/leaf-margin analysis).",
        "medium": "Paleoclimate envelope inferred from sedimentology/palynology; no direct numeric proxy published.",
    }.get(dino.get("confidence"), "")
    if confidence_note:
        parts.append(confidence_note)

    return " ".join(parts)


def rank_regions_for_dino(dino_id):
    dinosaurs, regions = load_data()
    dino = next(d for d in dinosaurs if d["id"] == dino_id)
    results = [score_region(dino, r) for r in regions]
    results.sort(key=lambda r: r["suitability"], reverse=True)
    return dino, results


def maxent_cross_check(dino, regions, n_presence=300, seed=42):
    """
    Cross-validates the Gaussian envelope score against a real MaxEnt
    implementation (elapid), the same algorithm class ecologists use
    for species distribution modeling.

    LIMITATION: because we only have one paleocoordinate per species
    (not a full set of real fossil occurrence records), 'presence'
    points here are synthetic samples drawn uniformly from the
    species' estimated climate envelope, not literal GPS fossil
    localities. This is a legitimate way to represent an estimated
    tolerance range to MaxEnt, but it is NOT the same rigor as fitting
    MaxEnt on real multi-locality occurrence data. Pulling real
    multi-locality data from the Paleobiology Database (see the
    live-fetch cell in this notebook, run in Google Colab) is the
    natural next step to remove this limitation.
    """
    import numpy as np
    from elapid import MaxentModel

    rng = np.random.default_rng(seed)
    presence = np.column_stack([
        rng.uniform(*dino["temp_range_c"], n_presence),
        rng.uniform(*dino["precip_range_mm"], n_presence),
        rng.uniform(*dino["humidity_range_pct"], n_presence),
    ])
    background = np.array([[r["temp_c"], r["precip_mm"], r["humidity_pct"]] for r in regions])

    model = MaxentModel(transform="cloglog")
    X = np.vstack([presence, background])
    y = np.concatenate([np.ones(len(presence)), np.zeros(len(background))])
    model.fit(X, y)

    scores = model.predict(background)
    out = []
    for r, s in zip(regions, scores):
        out.append({"region_name": r["name"], "maxent_suitability": round(float(s) * 100, 1)})
    out.sort(key=lambda x: x["maxent_suitability"], reverse=True)
    return out


if __name__ == "__main__":
    dino, results = rank_regions_for_dino("trex")
    print(f"Top 5 modern regions for {dino['name']}:\n")
    for r in results[:5]:
        print(f"  {r['region_name']:<35} suitability={r['suitability']}%  survival={r['survival_probability']}%")
        print(f"    -> {explain(dino, r)}\n")
