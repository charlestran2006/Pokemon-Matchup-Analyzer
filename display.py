"""
display.py
All CLI display/formatting functions. Keeps the UI layer separate from logic.
"""

from team_analysis import STAT_NAMES, STAT_LABELS

# ANSI color codes for a polished terminal look
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
DIM     = "\033[2m"
BOLD    = "\033[1m"
RESET   = "\033[0m"

BAR_WIDTH = 30  # Width of stat bars


def header(text: str):
    print(f"\n{BOLD}{CYAN}{'═' * 50}{RESET}")
    print(f"{BOLD}{CYAN}  {text}{RESET}")
    print(f"{BOLD}{CYAN}{'═' * 50}{RESET}")


def section(text: str):
    print(f"\n{BOLD}{YELLOW}── {text} {'─' * (45 - len(text))}{RESET}")


def print_pokemon_card(pokemon: dict):
    """Display a single Pokémon's info as a card."""
    types_str = " / ".join(t.capitalize() for t in pokemon["types"])
    abilities_str = ", ".join(a.replace("-", " ").title() for a in pokemon["abilities"])

    print(f"\n  {BOLD}{WHITE}{pokemon['name']}{RESET}  {DIM}#{pokemon['id']}{RESET}")
    print(f"  Type:    {CYAN}{types_str}{RESET}")
    print(f"  Ability: {DIM}{abilities_str}{RESET}")
    print(f"  {DIM}{'─' * 35}{RESET}")

    # Stat bars
    for stat in STAT_NAMES:
        val = pokemon["stats"].get(stat, 0)
        label = STAT_LABELS[stat].ljust(8)
        bar_fill = int((val / 255) * BAR_WIDTH)
        color = GREEN if val >= 100 else (YELLOW if val >= 60 else RED)
        bar = f"{color}{'█' * bar_fill}{DIM}{'░' * (BAR_WIDTH - bar_fill)}{RESET}"
        print(f"  {DIM}{label}{RESET} {bar} {WHITE}{val:>3}{RESET}")


def print_team_stats(stats: dict):
    """Display team-wide average stats as bars."""
    section("TEAM AVERAGE STATS")
    for stat in STAT_NAMES:
        val = stats["averages"][stat]
        label = STAT_LABELS[stat].ljust(8)
        bar_fill = int((val / 255) * BAR_WIDTH)
        color = GREEN if val >= 100 else (YELLOW if val >= 60 else RED)
        bar = f"{color}{'█' * bar_fill}{DIM}{'░' * (BAR_WIDTH - bar_fill)}{RESET}"
        print(f"  {DIM}{label}{RESET} {bar} {WHITE}{val:>5.1f}{RESET}")

    print(f"\n  {BOLD}Total BST (all 6): {WHITE}{stats['bst_total']}{RESET}")


def print_type_analysis(summary: str):
    """Display the type weakness/resistance summary."""
    section("TYPE ANALYSIS")
    for line in summary.split("\n"):
        print(f"  {line}")


def print_battle_comparison(comparison: dict, user_team_names: list, opp_team_names: list):
    """Display a side-by-side battle stat comparison."""
    section("BATTLE COMPARISON")

    user_names = ", ".join(user_team_names)
    opp_names  = ", ".join(opp_team_names)
    print(f"  {BLUE}YOUR TEAM{RESET}  vs  {RED}OPPONENT{RESET}")
    print(f"  {DIM}{user_names}{RESET}")
    print(f"  {DIM}vs {opp_names}{RESET}\n")

    for stat in STAT_NAMES:
        c = comparison["stat_comparison"][stat]
        label = STAT_LABELS[stat].ljust(8)
        user_col = f"{GREEN}{c['user']:>5.1f}{RESET}" if c["winner"] == "you" else f"{DIM}{c['user']:>5.1f}{RESET}"
        opp_col  = f"{RED}{c['opponent']:>5.1f}{RESET}" if c["winner"] == "opponent" else f"{DIM}{c['opponent']:>5.1f}{RESET}"
        arrow = f"{GREEN}◄{RESET}" if c["winner"] == "you" else (f"{RED}►{RESET}" if c["winner"] == "opponent" else "=")
        print(f"  {label}  You: {user_col}  {arrow}  Opp: {opp_col}")

    print()
    user_bst = comparison["user_bst"]
    opp_bst  = comparison["opponent_bst"]
    winner   = comparison["overall_winner"]

    if winner == "you":
        print(f"  {GREEN}{BOLD}✓ Your team wins on total BST! ({user_bst} vs {opp_bst}){RESET}")
    else:
        print(f"  {RED}{BOLD}✗ Opponent wins on total BST ({opp_bst} vs {user_bst}){RESET}")
