from datetime import datetime

from find_surf_spots.workflow import find_surf_spots, SurfSpot
from find_surf_spots.tools.openmeteo import DIRECTIONS


def test_find_surf_spots():
    surf_spots = find_surf_spots("Vigo", datetime.now().isoformat())
    spots = surf_spots.spots
    assert all(isinstance(spot, SurfSpot) for spot in spots)
    assert any(spot.name == "Praia de Patos" for spot in spots)
    for spot in spots:
        assert all(f.wave_direction in DIRECTIONS for f in spot.wave_forecasts)
        assert all(f.wind_direction in DIRECTIONS for f in spot.wind_forecasts)
