# 🎮 Pokémon Team Builder & Battle Analyzer

A command-line Python project that fetches live data from [PokéAPI](https://pokeapi.co) to analyze your Pokémon team's strengths, weaknesses, and battle potential.

Built as a passion project to practice my API integration in Python.

---

## Features

- 🔍 **Fetch any Pokémon** by name — types, stats, abilities
- 📊 **Team stat overview** — totals, averages, and visual stat bars
- 🛡️ **Type weakness analysis** — see which types threaten your team most
- ⚔️ **Random opponent battle** — compare your team vs a randomly generated opponent
- 🎨 **Colorized terminal output** with ANSI stat bars

---

## Project Structure

```
pokemon_analyzer/
├── main.py            # Entry point — CLI flow
├── pokemon_api.py     # API calls & response parsing
├── type_chart.py      # Full type effectiveness chart + defense calculator
├── team_analysis.py   # Stat aggregation & battle comparison logic
├── display.py         # All terminal UI / formatting
└── README.md
```

---

## Setup & Run

```bash
# 1. Clone or download the project
cd pokemon_analyzer

# 2. Install the only dependency
pip install requests

# 3. Run it
python main.py
```

No API key required — PokéAPI is free and open.

---

## Example Output

```
══════════════════════════════════════════════════
  POKÉMON TEAM BUILDER & BATTLE ANALYZER
══════════════════════════════════════════════════

── BUILD YOUR TEAM ──────────────────────────────
  Enter up to 6 Pokémon names (press Enter to stop)
  Your Pokémon 1/6: charizard
  ✓ Added Charizard [Fire / Flying]
  Your Pokémon 2/6: lapras
  ✓ Added Lapras [Water / Ice]
  ...

── TYPE ANALYSIS ────────────────────────────────
  ⚠  Major weaknesses: Rock (4/6), Electric (3/6)
  ✓  Strong resistances: Fire (3/6), Grass (3/6)
  🛡  Immunities: Ground (1/6)
```

---

## Optional Upgrades (next steps)

| Feature | How |
|---|---|
| Save/load teams | `json` module — read/write a `teams.json` file |
| Web UI | [Streamlit](https://streamlit.io) — ~50 lines to convert |
| Damage calculator | Add move data from `/api/v2/move/{name}` |
| Export to CSV | `csv` module — export team stats table |
| Team suggestions | Filter PokéAPI by type to suggest coverage picks |

---

## Tech Used

- **Python 3.10+**
- **requests** — HTTP library for API calls
- **PokéAPI** — free, no-auth Pokémon data API
- ANSI escape codes for terminal colors

---

## What I Learned

- Consuming and parsing a real REST API with Python
- Designing clean module separation (API layer, logic layer, UI layer)
- Implementing a matrix-based type effectiveness system
- Building a usable CLI with clear, formatted output
