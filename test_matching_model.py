"""Basic tests for the suitability scoring model."""
import math
from matching_model import variable_score, score_region, load_data

def test_variable_score_inside_range():
    assert variable_score(15, 10, 20) == 1.0

def test_variable_score_at_boundary():
    assert variable_score(10, 10, 20) == 1.0
    assert variable_score(20, 10, 20) == 1.0

def test_variable_score_outside_range_decays():
    s_near = variable_score(21, 10, 20)
    s_far = variable_score(50, 10, 20)
    assert 0 < s_far < s_near < 1.0

def test_variable_score_symmetric_falloff():
    below = variable_score(5, 10, 20)
    above = variable_score(25, 10, 20)
    assert math.isclose(below, above, rel_tol=1e-9)

def test_score_region_bounds():
    dinosaurs, regions = load_data()
    dino = dinosaurs[0]
    region = regions[0]
    result = score_region(dino, region)
    assert 0 <= result["suitability"] <= 100
    assert 0 <= result["survival_probability"] <= 100

def test_all_species_have_sources():
    dinosaurs, _ = load_data()
    for d in dinosaurs:
        assert len(d.get("sources", [])) > 0, f"{d['name']} missing sources"

def test_all_species_valid_ranges():
    dinosaurs, _ = load_data()
    for d in dinosaurs:
        assert d["temp_range_c"][0] < d["temp_range_c"][1]
        assert d["precip_range_mm"][0] < d["precip_range_mm"][1]
        assert d["humidity_range_pct"][0] < d["humidity_range_pct"][1]

if __name__ == "__main__":
    import sys
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS  {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
    print(f"\n{len(tests)-failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
