from datetime import datetime

from any_agent import AgentConfig, AgentTrace, AnyAgent
from any_agent.tools import search_tavily, visit_webpage

from find_surf_spots.schema import SurfSpots
from find_surf_spots.tools.openmeteo import get_wave_forecast, get_wind_forecast
from find_surf_spots.tools.openstreetmap import (
    driving_hours_to_meters,
    get_area_lat_lon,
    get_surfing_spots,
)


def find_surf_spots_agent(
    location: str, date: datetime, max_driving_hours: int = 1
) -> AgentTrace:
    user_prompt = (
        f"Find surf spots around {location} "
        f"for the given date {date} "
        f"within a maximum distance of {max_driving_hours} driving hours."
    )

    MODEL_ID = "gemini/gemini-2.5-pro"
    INSTRUCTIONS = "Use the tools to find an answer"
    TOOLS = [
        driving_hours_to_meters,
        get_area_lat_lon,
        get_surfing_spots,
        get_wave_forecast,
        get_wind_forecast,
        # Also provide generic web browsing tools
        search_tavily,
        visit_webpage,
    ]

    agent = AnyAgent.create(
        "tinyagent",
        AgentConfig(
            model_id=MODEL_ID,
            instructions=INSTRUCTIONS,
            tools=TOOLS,
            # Using an output type also helps guiding the agent behavior
            output_type=SurfSpots,
        ),
    )

    return agent.run(user_prompt)
