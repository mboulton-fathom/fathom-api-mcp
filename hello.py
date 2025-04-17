import functools
import os
from typing import List, TypedDict, Tuple
import click
import httpx

from fathom.sdk.v2 import Client, point
from mcp.server.fastmcp import FastMCP

from google.protobuf.json_format import MessageToDict

# Initialize FastMCP server
mcp = FastMCP("fathom-api")


@functools.lru_cache
def create_fathom_client() -> Client:
    """Initializes a Fathom API client."""
    client_id: str = os.getenv("FATHOM_CLIENT_ID")
    client_secret: str = os.getenv("FATHOM_CLIENT_SECRET")
    return Client(client_id, client_secret, api_address="dev.fathom.global")


class Address(TypedDict):
    """
    Represents an address from the OpenStreetMap API.
    """

    place_id: int
    licence: str
    osm_type: str
    osm_id: int
    lat: str
    lon: str
    category: str
    type: str
    place_rank: int
    importance: float
    addresstype: str
    name: str
    display_name: str
    boundingbox: List[str]


@mcp.tool()
async def get_fathom_data(latitude: float, longitude: float, layer_id: str) -> dict:
    """Retrieves Fathom data for a specific location and layer.

    Args:
        latitude: Latitude of the location.
        longitude: Longitude of the location.
        layer_id: The ID of the Fathom data layer to retrieve.
    """
    client: Client = create_fathom_client()
    pt = point(lat=latitude, lng=longitude)
    points_response = client.geo.get_points(([pt]), [layer_id])

    return MessageToDict(points_response)


@mcp.tool()
async def get_city_bounding_box(city_name: str) -> Tuple[float, float]:
    """Retrieves the bounding box of a city by name from OpenStreetMap.

    Args:
        city_name: The name of the city.
    """
    async with httpx.AsyncClient() as client:
        url = f"https://nominatim.openstreetmap.org/search?q={city_name}&format=jsonv2&limit=1"
        response = await client.get(url)
        response.raise_for_status()
        addresses: List[Address] = response.json()

        if not addresses:
            raise ValueError(f"City '{city_name}' not found")

        address: Address = addresses[0]
        boundingbox: List[str] = address["boundingbox"]
        min_lat: float = float(boundingbox[0])
        max_lat: float = float(boundingbox[1])
        min_lon: float = float(boundingbox[2])
        max_lon: float = float(boundingbox[3])
        return (min_lat + max_lat) / 2, (min_lon + max_lon) / 2


@mcp.tool()
async def get_layer_id(return_period: int, year: int, type: str) -> str:
    """Gets a layer ID from the given return period and year

    Args:
        return_period: The return period.
        year: The year.
        type: the type of layer (FLUVIAL, PLUVIAL, COASTAL)
    """
    return f"FLOOD_MAP-1ARCSEC-NW_OFFSET-1in{return_period}-{type}-DEFENDED-DEPTH-{year}-PERCENTILE50-v3.1"


@click.command()
@click.option('--transport', default='stdio', help='Transport to use for the MCP server.')
def run_mcp(transport: str):
    """Runs the MCP server with the specified transport."""
    mcp.run(transport=transport)


if __name__ == "__main__":
    # Initialize and run the server
    run_mcp()

