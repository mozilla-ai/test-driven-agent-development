from pydantic import BaseModel


class WaveForecast(BaseModel):
    sea_level_height: float
    wave_direction: str
    wave_height: float
    wave_period: float


class WindForecast(BaseModel):
    wind_direction: str
    wind_speed: float


class SurfSpot(BaseModel):
    name: str
    wave_forecasts: list[WaveForecast]
    wind_forecasts: list[WindForecast]


class SurfSpots(BaseModel):
    spots: list[SurfSpot]
