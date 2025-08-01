import requests
import json


def get_area_lat_lon(area_name: str) -> tuple[float, float]:
    """Get the latitude and longitude of an area from Nominatim.

    Uses the [Nominatim API](https://nominatim.org/release-docs/develop/api/Search/).

    Args:
        area_name: The name of the area.

    Returns:
        The area found.
    """
    response = requests.get(
        f"https://nominatim.openstreetmap.org/search?q={area_name}&format=json",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    area = json.loads(response.content.decode())
    return area[0]["lat"], area[0]["lon"]


def driving_hours_to_meters(driving_hours: int) -> int:
    """Convert driving hours to meters assuming a 70 km/h average speed.


    Args:
        driving_hours: The driving hours.

    Returns:
        The distance in meters.
    """
    return driving_hours * 70 * 1000


def get_lat_lon_center(bounds: dict) -> tuple[float, float]:
    """Get the latitude and longitude of the center of a bounding box.

    Args:
        bounds: The bounding box.

            ```json
            {
                "minlat": float,
                "minlon": float,
                "maxlat": float,
                "maxlon": float,
            }
            ```

    Returns:
        The latitude and longitude of the center.
    """
    return (
        (bounds["minlat"] + bounds["maxlat"]) / 2,
        (bounds["minlon"] + bounds["maxlon"]) / 2,
    )


def get_surfing_spots(
    lat: float, lon: float, radius: int
) -> list[tuple[str, tuple[float, float]]]:
    """Get surfing spots around a given latitude and longitude.

    Uses the [Overpass API](https://wiki.openstreetmap.org/wiki/Overpass_API).

    Args:
        lat: The latitude.
        lon: The longitude.
        radius: The radius in meters.

    Returns:
        The surfing places found.
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    query = "[out:json];("
    query += f'nwr["natural"="beach"](around:{radius},{lat},{lon});'
    query += f'nwr["natural"="reef"](around:{radius},{lat},{lon});'
    query += ");out body geom;"
    params = {"data": query}
    response = requests.get(
        overpass_url, params=params, headers={"User-Agent": "Mozilla/5.0"}
    )
    response.raise_for_status()
    elements = response.json()["elements"]
    return [
        (element.get("tags", {}).get("name", ""), get_lat_lon_center(element["bounds"]))
        for element in elements
        if "surfing" in element.get("tags", {}).get("sport", "") and "bounds" in element
    ]
