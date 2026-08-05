# If Dinosaurs Lived Today

A climate-based Species Distribution Model (SDM) that predicts which modern regions of Earth
would be climatically suitable for 12 well-documented dinosaur species, cross-validated against
a real MaxEnt implementation.

**Live demo:** open `if_dinosaurs_lived_today.html` directly in any browser, or enable GitHub
Pages on this repo (Settings → Pages → deploy from `main` branch → `/root`) for a shareable link.

## What's in this repo

| File | What it is |
|---|---|
| `if_dinosaurs_lived_today.html` | Self-contained interactive web app (specimen catalog + per-species map dossier). No install, no external dependencies, open directly in any browser. |
| `EcoVerse_Dinosaur_Climate_Model.ipynb` | Executed research notebook: citation-backed climate data, the scoring model, MaxEnt cross-validation, and 8 interactive visualizations. |
| `If_Dinosaurs_Lived_Today_OnePager.pdf` | One-page project summary for presentations/applications. |
| `matching_model.py` | Reusable Python scoring engine (Gaussian envelope model + MaxEnt cross-check). |
| `test_matching_model.py` | Test suite (`python3 test_matching_model.py`). |
| `data/dinosaurs.json` | 12 species with citation-backed paleoclimate envelopes. |
| `data/regions.json` | 59 modern world regions with climate normals. |
| `requirements.txt` | Python dependencies. |

## Quick start

```bash
pip install -r requirements.txt --break-system-packages
python3 test_matching_model.py          # run tests
python3 matching_model.py               # CLI demo
jupyter notebook EcoVerse_Dinosaur_Climate_Model.ipynb
```

Or just open `if_dinosaurs_lived_today.html` in a browser, nothing to install.

## How it works

For each dinosaur species, an estimated paleoclimate envelope (temperature, precipitation,
humidity range) is reconstructed from published paleoclimate literature where available, then
compared against real modern climate data across 59 world regions using a weighted Gaussian
scoring formula:

```
suitability = 0.40 x temp_score + 0.35 x precip_score + 0.25 x humidity_score
```

This is independently cross-validated against a real MaxEnt implementation ([elapid](https://elapid.org)),
the algorithm class ecologists actually use for species distribution modeling.

## Data provenance

- **9 of 12 species** use paleoclimate ranges backed by cited, formation-specific published
  research (leaf-margin analysis, CLAMP, paleosol geochemistry). See each species' `sources`
  field in `data/dinosaurs.json`, or Section 1 of the notebook.
- **3 of 12 species** (Parasaurolophus, Iguanodon, Argentinosaurus) currently use formation-level
  qualitative interpretation rather than a quantitative multi-proxy study. Flagged explicitly.
- **Modern climate data** is a curated 59-region sample of real-world climate normals.

## Known limitations

- Paleoclimate envelopes are estimates from published research, not direct physiological
  measurement (impossible for extinct animals).
- MaxEnt presence points are synthetic, sampled from the estimated envelope rather than real
  multi-locality GPS fossil occurrences.
- No food-web, competition, or human land-use modeling; the diet-based survival modifier is
  illustrative only.
- No physiological modeling of thermoregulation strategy or body-size-scaled water needs.

This is a demonstration-grade research prototype that applies a real SDM methodology to
paleontology, not a peer-reviewed paleoclimate reconstruction. Full details and references are
in the notebook.

## License / attribution

Paleoclimate figures are drawn from and cited to the published sources listed in the References
section of the notebook. Modern climate figures are curated reference estimates.
