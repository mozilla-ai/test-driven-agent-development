from datetime import datetime

from any_agent.tracing.attributes import GenAI

from find_surf_spots.agent import find_surf_spots_agent
from find_surf_spots.tools.openmeteo import DIRECTIONS
from find_surf_spots.schema import SurfSpot, SurfSpots


def assert_tool_was_used(agent_trace, tool_name):
    assert any(
        (
            span.attributes.get(GenAI.TOOL_NAME) == tool_name
            and span.status.status_code.value == "ok"
        )
        for span in agent_trace.spans
        if span.is_tool_execution()
    )


def test_find_surf_spots_agent():
    agent_trace = find_surf_spots_agent("Vigo", datetime.now().isoformat())

    spots: SurfSpots = agent_trace.final_output.spots
    assert all(isinstance(spot, SurfSpot) for spot in spots)
    assert any(spot.name == "Praia de Patos" for spot in spots)
    for spot in spots:
        assert all(f.wave_direction in DIRECTIONS for f in spot.wave_forecasts)
        assert all(f.wind_direction in DIRECTIONS for f in spot.wind_forecasts)

    assert_tool_was_used(agent_trace, "get_surfing_spots")
