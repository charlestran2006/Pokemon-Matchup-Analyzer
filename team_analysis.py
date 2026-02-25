"""
team_analysis.py
Functions to compute team-wide statistics and generate battle comparisons.
"""

from type_chart import analyze_team_types

STAT_NAMES = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
STAT_LABELS = {
    "hp": "HP",
    "attack": "Attack",
    "defense": "Defense",
    "special-attack": "Sp. Atk",
    "special-defense": "Sp. Def",
    "speed": "Speed",
}


def compute_team_stats(team: list[dict]) -> dict:
    """
    Compute total and average base stats for the entire team.
    Returns a dict with 'totals', 'averages', and 'bst_total'.
    """
    totals = {stat: 0 for stat in STAT_NAMES}
    averages = {}

    for pokemon in team:
        for stat in STAT_NAMES:
            totals[stat] += pokemon["stats"].get(stat, 0)

    count = len(team)
    for stat in STAT_NAMES:
        averages[stat] = round(totals[stat] / count, 1) if count else 0

    # Base Stat Total = sum of all stats for the full team
    bst_total = sum(totals.values())

    return {
        "totals": totals,
        "averages": averages,
        "bst_total": bst_total,
    }


def compare_teams(user_team: list[dict], opponent_team: list[dict]) -> dict:
    """
    Compare user team vs opponent team across stats.
    Returns a summary of who leads in each category.
    """
    user_stats = compute_team_stats(user_team)
    opp_stats = compute_team_stats(opponent_team)

    comparison = {}
    for stat in STAT_NAMES:
        user_avg = user_stats["averages"][stat]
        opp_avg = opp_stats["averages"][stat]
        diff = round(user_avg - opp_avg, 1)
        comparison[stat] = {
            "user": user_avg,
            "opponent": opp_avg,
            "diff": diff,
            "winner": "you" if diff > 0 else ("opponent" if diff < 0 else "tie"),
        }

    return {
        "user_bst": user_stats["bst_total"],
        "opponent_bst": opp_stats["bst_total"],
        "stat_comparison": comparison,
        "overall_winner": "you" if user_stats["bst_total"] > opp_stats["bst_total"] else "opponent",
    }


def generate_type_summary(team: list[dict]) -> str:
    """
    Generate a plain-English summary of team type strengths/weaknesses.
    e.g. "Your team is weak to Electric (3/6) and immune to Ghost (1/6)."
    """
    analysis = analyze_team_types(team)
    team_size = len(team)
    lines = []

    # Biggest weaknesses (3+ members weak)
    big_weaknesses = sorted(
        [(t, c) for t, c in analysis["weaknesses"].items() if c >= 3],
        key=lambda x: -x[1]
    )
    if big_weaknesses:
        weak_str = ", ".join(f"{t.capitalize()} ({c}/{team_size})" for t, c in big_weaknesses)
        lines.append(f"⚠  Major weaknesses: {weak_str}")

    # Minor weaknesses
    minor_weaknesses = sorted(
        [(t, c) for t, c in analysis["weaknesses"].items() if c < 3],
        key=lambda x: -x[1]
    )
    if minor_weaknesses:
        weak_str = ", ".join(f"{t.capitalize()}" for t, c in minor_weaknesses)
        lines.append(f"   Minor weaknesses: {weak_str}")

    # Resistances (2+ members)
    good_resists = sorted(
        [(t, c) for t, c in analysis["resistances"].items() if c >= 2],
        key=lambda x: -x[1]
    )
    if good_resists:
        res_str = ", ".join(f"{t.capitalize()} ({c}/{team_size})" for t, c in good_resists)
        lines.append(f"✓  Strong resistances: {res_str}")

    # Immunities
    if analysis["immunities"]:
        imm_str = ", ".join(
            f"{t.capitalize()} ({c}/{team_size})"
            for t, c in sorted(analysis["immunities"].items(), key=lambda x: -x[1])
        )
        lines.append(f"🛡  Immunities: {imm_str}")

    return "\n".join(lines) if lines else "Balanced type coverage — no major gaps detected."
