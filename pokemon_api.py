"""
pokemon_api.py
Handles all PokéAPI requests and data parsing.
"""

import requests

BASE_URL = "https://pokeapi.co/api/v2"


def get_pokemon(name: str) -> dict | None:
    """
    Fetch a single Pokémon's data from PokéAPI.
    Returns a clean dict with types, stats, and abilities.
    Returns None if the Pokémon is not found.
    """
    url = f"{BASE_URL}/pokemon/{name.lower().strip()}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError:
        print(f"  ✗ '{name}' not found. Check the spelling!")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Network error: {e}")
        return None

    # Parse the raw API response into something clean
    pokemon = {
        "name": data["name"].capitalize(),
        "id": data["id"],
        "types": [t["type"]["name"] for t in data["types"]],
        "abilities": [a["ability"]["name"] for a in data["abilities"]],
        "stats": {
            s["stat"]["name"]: s["base_stat"] for s in data["stats"]
        },
        "sprite": data["sprites"]["front_default"],
    }

    return pokemon


def get_random_pokemon_names(count: int = 6) -> list[str]:
    """
    Fetch a list of random Pokémon names from the API.
    Uses the /pokemon endpoint with a random offset.
    """
    import random

    # There are ~1010 Pokémon total; we stick to the first 898 (Gen 1-8)
    offset = random.randint(0, 892)
    url = f"{BASE_URL}/pokemon?limit={count}&offset={offset}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        results = response.json()["results"]
        return [p["name"] for p in results]
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Could not fetch random team: {e}")
        return []
