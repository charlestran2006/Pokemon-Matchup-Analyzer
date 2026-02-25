"""
main.py  ─  Pokémon Team Builder & Battle Analyzer
Run with: python main.py
"""

from pokemon_api import get_pokemon, get_random_pokemon_names
from team_analysis import compute_team_stats, compare_teams, generate_type_summary
from display import (
    header, section, print_pokemon_card,
    print_team_stats, print_type_analysis, print_battle_comparison,
    BOLD, CYAN, WHITE, DIM, YELLOW, RESET
)


def build_team(prompt_label: str = "Your") -> list[dict]:
    """
    Interactively prompt the user to enter up to 6 Pokémon names.
    Returns a list of fetched Pokémon dicts.
    """
    team = []
    print(f"\n  {DIM}Enter up to 6 Pokémon names (press Enter with no input to stop){RESET}")

    while len(team) < 6:
        slot = len(team) + 1
        raw = input(f"  {prompt_label} Pokémon {slot}/6: ").strip()

        if not raw:
            if len(team) == 0:
                print("  Please enter at least one Pokémon!")
                continue
            break

        print(f"  Fetching {raw.capitalize()}...")
        pokemon = get_pokemon(raw)

        if pokemon:
            team.append(pokemon)
            types_str = " / ".join(t.capitalize() for t in pokemon["types"])
            print(f"  ✓ Added {BOLD}{pokemon['name']}{RESET} [{types_str}]")

    return team


def build_random_team() -> list[dict]:
    """Fetch 6 random Pokémon from the API."""
    print(f"\n  {DIM}Generating random opponent team...{RESET}")
    names = get_random_pokemon_names(6)
    team = []
    for name in names:
        pokemon = get_pokemon(name)
        if pokemon:
            team.append(pokemon)
            print(f"  ✓ {pokemon['name']}")
    return team


def run():
    header("POKÉMON TEAM BUILDER & BATTLE ANALYZER")
    print(f"\n  {DIM}Powered by PokéAPI · pokeapi.co{RESET}")

    # ── Build user team ──────────────────────────────────────────────
    section("BUILD YOUR TEAM")
    user_team = build_team("Your")

    if not user_team:
        print("No Pokémon entered. Exiting.")
        return

    # ── Display each Pokémon card ────────────────────────────────────
    section("YOUR TEAM")
    for pokemon in user_team:
        print_pokemon_card(pokemon)

    # ── Team stats ───────────────────────────────────────────────────
    stats = compute_team_stats(user_team)
    print_team_stats(stats)

    # ── Type analysis ────────────────────────────────────────────────
    summary = generate_type_summary(user_team)
    print_type_analysis(summary)

    # ── Optional: battle a random opponent ───────────────────────────
    print(f"\n  {YELLOW}Want to battle a random opponent team? (y/n){RESET} ", end="")
    if input().strip().lower() == "y":

        section("OPPONENT'S RANDOM TEAM")
        opponent_team = build_random_team()

        if opponent_team:
            for pokemon in opponent_team:
                print_pokemon_card(pokemon)

            comparison = compare_teams(user_team, opponent_team)
            user_names = [p["name"] for p in user_team]
            opp_names  = [p["name"] for p in opponent_team]
            print_battle_comparison(comparison, user_names, opp_names)

    print(f"\n{BOLD}{CYAN}  Thanks for using the Pokémon Team Analyzer!{RESET}\n")


if __name__ == "__main__":
    run()
