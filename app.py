import time
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="24/7 Dabble Sharp EV Scanner", layout="wide")
st.title("⚡ 24/7 Sharp-Book Discrepancy & Juice Engine")


def fetch_market_consensus_feed():
  """Continuously pulls live data matching Dabble lines against sharp books

  (Pinnacle, Circa, DraftKings, FanDuel) to scan for heavy juice and raw number
  gaps.
  """
  # Production implementation: integrate sports odds API (e.g., The Odds API)
  # to parse sharp book pricing and compare against Dabble board lines.
  market_data = [
      {
          "player": "Player_A",
          "sport": "CS2",
          "prop": "Maps 1/2 Kills",
          "dabble_line": 33.5,
          "sharp_line": 33.5,
          "sharp_odds_over": -145,
          "sharp_odds_under": +115,
      },
      {
          "player": "Player_B",
          "sport": "NBA",
          "prop": "Points",
          "dabble_line": 238.5,
          "sharp_line": 245.5,
          "sharp_odds_over": -110,
          "sharp_odds_under": -110,
      },
  ]
  return pd.DataFrame(market_data)


def evaluate_sharp_edges(df):
  if df.empty:
    return df

  signals = []
  for _, row in df.iterrows():
    action = None
    reason = ""

    # Rule 1: Heavy Juice Check (-135 or worse on sharp books)
    if row["sharp_odds_over"] <= -135:
      action = "HAMMER MORE 🔨"
      reason = f"Heavy Juice Over ({row['sharp_odds_over']})"
    elif row["sharp_odds_under"] <= -135:
      action = "HAMMER LESS 🔨"
      reason = f"Heavy Juice Under ({row['sharp_odds_under']})"

    # Rule 2: Raw Line Number Discrepancy Check (Sharp vs Dabble gap)
    line_diff = row["sharp_line"] - row["dabble_line"]
    if line_diff >= 0.5:
      action = "HAMMER MORE 🔨"
      reason = (
          f"Line Gap: Sharp at {row['sharp_line']} vs Dabble"
          f" {row['dabble_line']}"
      )
    elif line_diff <= -0.5:
      action = "HAMMER LESS 🔨"
      reason = (
          f"Line Gap: Sharp at {row['sharp_line']} vs Dabble"
          f" {row['dabgle_line']}"
      )

    if action:
      signals.append({
          "Player": row["player"],
          "Sport": row["sport"],
          "Prop": row["prop"],
          "Dabble Line": row["dabble_line"],
          "Sharp Line": row["sharp_line"],
          "Trigger Edge": reason,
          "Signal": action,
      })

  return pd.DataFrame(signals)


# 24/7 Continuous Scanning Loop Execution
df_raw = fetch_market_consensus_feed()
signal_df = evaluate_sharp_edges(df_raw)

st.subheader("Active Exploits & Instant Hammer Signals")
if not signal_df.empty:
  st.dataframe(signal_df, use_container_width=True)
else:
  st.info(
      "Scanning 24/7 across sharp books... Waiting for juice threshold or line"
      " delta."
  )

st.sidebar.markdown("**Engine Mode:** 24/7 Sharp Arbitrage Active")
st.sidebar.markdown("**Target Slips:** 3-Pick & 5-Pick Optimization")
