from numpy import arange
from geopandas import read_file,datasets
from shapely.geometry import Point, Polygon
from typing import Set, Tuple


def get_country_coords(country: str, step: float) -> Set[Tuple[float, float]]:
    """
    Generate a set of geographical coordinates within the bounding box of a specified country.

    Parameters
    ----------
    country: str
        The name of the country for which to generate coordinates.
        List of country names according to https://geopandas.org/en/v0.2.1/mapping.html documentation
    step: float
        The step size for generating the grid of coordinates.

    Returns
    -------
    Set[Tuple[float, float]]
        A set of (latitude, longitude) tuples representing the grid of coordinates.
    """

    world = read_file(datasets.get_path('naturalearth_lowres'))
    country_geom = world.loc[world.name == country]
    
    lon_min, lat_min, lon_max, lat_max = country_geom.total_bounds.round(2)
    lats = arange(lat_min, lat_max, step)
    lons = arange(lon_min, lon_max, step)

    return {(lat,lon) for lat in lats for lon in lons}