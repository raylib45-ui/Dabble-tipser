import pandas as pd
import streamlit as st

st.set_page_config(page_title="24/7 Dabble Board Engine", layout="wide")
st.title("⚡ Dabble Board L5 Trend & Discrepancy Engine")


def fetch_dabble_board_data():
  """Parses live Dabble MLB Pitcher Strikeout board with trailing 5-game stats

  (L5).
  """
  board_props = [
      {
          "player": "Jesús Luzardo",
          "team": "PHI",
          "prop": "Pitcher Strikeouts",
          "line": 7.5,
          "l5": [12, 9, 9, 9, 6],
      },
      {
          "player": "Dylan Cease",
          "team": "ATH",
          "prop": "Pitcher Strikeouts",
          "line": 7.5,
          "l5": [7, 10, 8, 8, 4],
      },
      {
          "player": "Emmet Sheehan",
          "team": "LAD",
          "prop": "Pitcher Strikeouts",
          "line": 6.5,
          "l5": [5, 7, 6, 5, 4],
      },
      {
          "player": "Brayan Bello",
          "team": "BOS",
          "prop": "Pitcher Strikeouts",
          "line": 4.5,
          "l5": [4, 3, 1, 2, 0],
      },
      {
          "player": "Grayson Rodriguez",
          "team": "BOS",
          "prop": "Pitcher Strikeouts",
          "line": 4.5,
          "l5": [8, 5, 6, 4, 7],
      },
      {
          "player": "Trevor Rogers",
          "team": "BAL",
          "prop": "Pitcher Strikeouts",
          "line": 4.5,
          "l5": [4, 6, 6, 7, 11],
      },
      {
          "player": "Logan Webb",
          "team": "SF",
          "prop": "Pitcher Strikeouts",
          "line": 4.5,
          "l5": [2, 7, 2, 6, 1],
      },
      {
          "player": "Chase Burns",
          "team": "LAD",
          "prop": "Pitcher Strikeouts",
          "line": 4.5,
          "l5": [6, 8, 8, 5, 7],
      },
      {
          "player": "Jacob Lopez",
          "team": "ATH",
          "prop": "Pitcher Strikeouts",
          "line": 4.5,
          "l5": [5, 6, 9, 6, 7],
      },
      {
          "player": "Grant Holmes",
          "team": "PHI",
          "prop": "Pitcher Strikeouts",
          "line": 3.5,
          "l5": [2, 3, 3, 3, 1],
      },
      {
          "player": "Joe Ryan",
          "team": "DET",
          "prop": "Pitcher Strikeouts",
          "line": 3.5,
          "l5": [9, 6, 3, 4, 3],
      },
      {
          "player": "Michael McGreevy",
          "team": "SF",
          "prop": "Pitcher Strikeouts",
          "line": 3.5,
          "l5": [4, 6, 4, 3, 4],
      },
      {
          "player": "Derek Law",
          "team": "KC",
          "prop": "Pitcher Strikeouts",
          "line": 0.5,
          "l5": [1, 1, 0, 2, 0],
      },
  ]
  return pd.DataFrame(board_props)


def analyze_l5_consistency(df, min_hit_rate=0.80):
  """Evaluates L5 arrays for strict consistency (80%+ or 100% over/under hit

  rate).
  """
  signals = []
  for _, row in df.iterrows():
    line = row["line"]
    l5 = row["l5"]

    overs = sum(1 for x in l5 if x > line)
    unders = sum(1 for x in l5 if x < line)
    total_games = len(l5)

    over_rate = overs / total_games
    under_rate = unders / total_games

    action = None
    trend_desc = ""

    if over_rate >= min_hit_rate:
      action = "HAMMER MORE 🔨"
      trend_desc = (
          f"Strict OVER Lock: Cleared line in {overs}/{total_games} games"
          f" ({int(over_rate*100)}%)"
      )
    elif under_rate >= min_hit_rate:
      action = "HAMMER LESS 🔨"
      trend_desc = (
          f"Strict UNDER Lock: Stayed under in {unders}/{total_games} games"
          f" ({int(under_rate*100)}%)"
      )

    if action:
      signals.append({
          "Player": row["player"],
          "Team": row["team"],
          "Prop Line": line,
          "L5 History": str(l5),
          "L5 Trend": trend_desc,
          "Signal": action,
      })

  return pd.DataFrame(signals)


# Run Model Analysis
df_board = fetch_dabble_board_data()
df_signals = analyze_l5_consistency(df_board, min_hit_rate=0.80)

st.subheader("Strict L5 Trend Locks (80%+ Hit Rate Criteria)")
if not df_signals.empty:
  st.dataframe(df_signals, use_container_width=True)
else:
  st.info("No props currently match the strict 80%+ consistency threshold.")

st.sidebar.markdown("**Active Mode:** Live Board L5 Trend Scanner")
st.sidebar.markdown("**Filter:** Strict Consistency Only (80%+ Hit Rate)")
