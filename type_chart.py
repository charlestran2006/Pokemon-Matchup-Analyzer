"""
type_chart.py
Full Gen 9 type effectiveness chart.
Used to calculate team-wide weaknesses and resistances.
"""

# type_chart[attacking_type][defending_type] = multiplier
# Only non-1x entries are listed (1x is assumed for missing pairs)
TYPE_CHART = {
    "normal":   {"rock": 0.5, "ghost": 0, "steel": 0.5},
    "fire":     {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 2, "bug": 2,
                 "rock": 0.5, "dragon": 0.5, "steel": 2},
    "water":    {"fire": 2, "water": 0.5, "grass": 0.5, "ground": 2,
                 "rock": 2, "dragon": 0.5},
    "electric": {"water": 2, "electric": 0.5, "grass": 0.5, "ground": 0,
                 "flying": 2, "dragon": 0.5},
    "grass":    {"fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5,
                 "ground": 2, "flying": 0.5, "bug": 0.5, "rock": 2,
                 "dragon": 0.5, "steel": 0.5},
    "ice":      {"water": 0.5, "grass": 2, "ice": 0.5, "ground": 2,
                 "flying": 2, "dragon": 2, "steel": 0.5},
    "fighting": {"normal": 2, "ice": 2, "poison": 0.5, "flying": 0.5,
                 "psychic": 0.5, "bug": 0.5, "rock": 2, "ghost": 0,
                 "dark": 2, "steel": 2, "fairy": 0.5},
    "poison":   {"grass": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5,
                 "ghost": 0.5, "steel": 0, "fairy": 2},
    "ground":   {"fire": 2, "electric": 2, "grass": 0.5, "poison": 2,
                 "flying": 0, "bug": 0.5, "rock": 2, "steel": 2},
    "flying":   {"electric": 0.5, "grass": 2, "fighting": 2, "bug": 2,
                 "rock": 0.5, "steel": 0.5},
    "psychic":  {"fighting": 2, "poison": 2, "psychic": 0.5, "dark": 0,
                 "steel": 0.5},
    "bug":      {"fire": 0.5, "grass": 2, "fighting": 0.5, "flying": 0.5,
                 "psychic": 2, "ghost": 0.5, "dark": 2, "steel": 0.5,
                 "fairy": 0.5},
    "rock":     {"fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5,
                 "flying": 2, "bug": 2, "steel": 0.5},
    "ghost":    {"normal": 0, "psychic": 2, "ghost": 2, "dark": 0.5},
    "dragon":   {"dragon": 2, "steel": 0.5, "fairy": 0},
    "dark":     {"fighting": 0.5, "psychic": 2, "ghost": 2, "dark": 0.5,
                 "fairy": 0.5},
    "steel":    {"fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2,
                 "rock": 2, "steel": 0.5, "fairy": 2},
    "fairy":    {"fire": 0.5, "fighting": 2, "poison": 0.5, "dragon": 2,
                 "dark": 2, "steel": 0.5},
}

ALL_TYPES = list(TYPE_CHART.keys())


def get_type_multiplier(attacking: str, defending: str) -> float:
    """Return the damage multiplier for attacking type vs defending type."""
    return TYPE_CHART.get(attacking, {}).get(defending, 1.0)


def get_pokemon_defenses(types: list[str]) -> dict[str, float]:
    """
    Calculate the combined defensive multiplier for a Pokémon
    with one or two types.
    Returns a dict of {attacking_type: multiplier}.
    """
    defenses = {}
    for atk_type in ALL_TYPES:
        multiplier = 1.0
        for def_type in types:
            multiplier *= get_type_multiplier(atk_type, def_type)
        defenses[atk_type] = multiplier
    return defenses


def analyze_team_types(team: list[dict]) -> dict:
    """
    Analyze the entire team's type profile.
    Returns a breakdown of weaknesses, resistances, and immunities
    counted by how many team members share them.
    """
    # Count how many team members are weak/resistant to each type
    weakness_counts = {t: 0 for t in ALL_TYPES}
    resistance_counts = {t: 0 for t in ALL_TYPES}
    immunity_counts = {t: 0 for t in ALL_TYPES}

    for pokemon in team:
        defenses = get_pokemon_defenses(pokemon["types"])
        for atk_type, mult in defenses.items():
            if mult > 1:
                weakness_counts[atk_type] += 1
            elif mult == 0:
                immunity_counts[atk_type] += 1
            elif mult < 1:
                resistance_counts[atk_type] += 1

    return {
        "weaknesses": {t: c for t, c in weakness_counts.items() if c > 0},
        "resistances": {t: c for t, c in resistance_counts.items() if c > 0},
        "immunities": {t: c for t, c in immunity_counts.items() if c > 0},
    }
