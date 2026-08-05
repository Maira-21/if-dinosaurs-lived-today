# If Dinosaurs Lived Today

A climate-based Species Distribution Model (SDM) that predicts which modern regions of Earth
would be climatically suitable for 12 well-documented dinosaur species, cross-validated against
a real MaxEnt implementation.

**Live demo:** open `if_dinosaurs_lived_today.html` directly, or enable GitHub Pages on this repo
(Settings → Pages → deploy from `main` branch → `/root`) for a shareable link.

## What's in this repo

| File | What it is |
|---|---|
| `if_dinosaurs_lived_today.html` | Multi-page interactive web app (catalog, per-species map dossier, methodology). Open directly in any browser, no install. |
| `EcoVerse_Dinosaur_Climate_Model.ipynb` | Executed research notebook: citations, scoring model, MaxEnt cross-validation, live-fetch cells for NASA POWER + Paleobiology Database (run those cells in Google Colab). |
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

## Data provenance

- **9 of 12 species** use paleoclimate ranges backed by cited, formation-specific published
  research (leaf-margin analysis, CLAMP, paleosol geochemistry). See each species' `sources`
  field in `data/dinosaurs.json`, or the Methodology page in the web app.
- **3 of 12 species** (Parasaurolophus, Iguanodon, Argentinosaurus) currently use formation-level
  qualitative interpretation rather than a quantitative multi-proxy study. Flagged explicitly.
- **Modern climate data** is a curated 59-region sample. The notebook includes a ready-to-run
  NASA POWER live-fetch cell (free public API, no key) to replace it with real point-queried data.
- **Fossil occurrences** currently use one paleocoordinate per species. The notebook includes a
  ready-to-run Paleobiology Database live-fetch cell (free public API, no key) to pull the full
  real occurrence set per species.

Both live-fetch cells need an open internet connection (they work in Google Colab); they are
commented out by default since some sandboxed environments block outbound API calls.

## Known limitations

See the Methodology page in the web app or Section 10 of the notebook for the full, explicit
limitations list. Short version: this is a demonstration-grade research prototype that shows a
real SDM methodology applied to paleontology, not a peer-reviewed paleoclimate reconstruction.

## License / attribution

Paleoclimate figures are drawn from and cited to the published sources listed in the References
section of the notebook and the Methodology page. Modern climate figures are curated reference
estimates pending live API replacement.
