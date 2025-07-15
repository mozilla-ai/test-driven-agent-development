from datetime import datetime

from loguru import logger

from find_surf_spots.schema import SurfSpot, SurfSpots, WaveForecast, WindForecast
from find_surf_spots.tools.openmeteo import get_wave_forecast, get_wind_forecast
from find_surf_spots.tools.openstreetmap import (
    driving_hours_to_meters,
    get_area_lat_lon,
    get_surfing_spots,
)


def find_surf_spots(
    location: str, date: datetime, max_driving_hours: int = 1
) -> SurfSpots:
    max_driving_meters = driving_hours_to_meters(max_driving_hours)
    lat, lon = get_area_lat_lon(location)

    logger.info(f"Getting surfing spots around {location}")
    surf_spots = get_surfing_spots(lat, lon, max_driving_meters)[:5]

    if not surf_spots:
        logger.warning("No surfing spots found around {location}")
        return None

    results = SurfSpots(spots=[])
    for spot_name, (spot_lat, spot_lon) in surf_spots:
        logger.info(f"Processing {spot_name}")
        logger.debug("Getting wave forecast...")
        wave_forecasts = get_wave_forecast(spot_lat, spot_lon, date)
        logger.debug("Getting wind forecast...")
        wind_forecasts = get_wind_forecast(spot_lat, spot_lon, date)

        results.spots.append(
            SurfSpot(
                name=spot_name,
                wave_forecasts=[
                    WaveForecast(
                        sea_level_height=wave_forecast["sea_level_height_msl"],
                        wave_direction=wave_forecast["wave_direction"],
                        wave_height=wave_forecast["wave_height"],
                        wave_period=wave_forecast["wave_period"],
                    )
                    for wave_forecast in wave_forecasts
                ],
                wind_forecasts=[
                    WindForecast(
                        wind_direction=wind_forecast["winddirection_10m"],
                        wind_speed=wind_forecast["windspeed_10m"],
                    )
                    for wind_forecast in wind_forecasts
                ],
            )
        )

    return results
