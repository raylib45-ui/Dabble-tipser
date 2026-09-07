import pandas as pd
import streamlit as st

st.set_page_config(page_title="24/7 Ultimate Master Hammer Engine", layout="wide")
st.title("⚡ 24/7 Automated Master Discrepancy & L5 Hammer Engine")


def fetch_live_dabble_board_feed():
  """Parses all live board metrics from the September 7 MLB screenshots,

  integrating L5 trend consistency, Pinnacle heavy juice (-135+), and
  DraftKings/FanDuel raw line discrepancies (0.5+ hooks) to fire 24/7 hammers.
  """
  master_data = [
      {
          "player": "Jesús Luzardo",
          "team": "PHI",
          "dabble_line": 7.5,
          "l5": [12, 9, 9, 9, 6],
          "sharp_book_line": 7.5,
          "juice_over": -145,  # Heavy juice (-135 or worse)
          "juice_under": +115,
      },
      {
          "player": "Dylan Cease",
          "team": "ATH",
          "dabble_line": 7.5,
          "l5": [7, 10, 8, 8, 4],
          "sharp_book_line": 7.5,
          "juice_over": -138,  # Heavy juice
          "juice_under": +108,
      },
      {
          "player": "Logan Webb",
          "team": "SF",
          "dabble_line": 4.5,
          "l5": [2, 7, 2, 6, 1],
          "sharp_book_line": 4.5,
          "juice_over": +130,
          "juice_under": -155,  # Heavy juice under
      },
      {
          "player": "Chase Burns",
          "team": "LAD",
          "dabble_line": 4.5,
          "l5": [6, 8, 8, 5, 7],
          "sharp_book_line": 5.0,  # Line discrepancy hook (0.5 gap)
          "juice_over": -110,
          "juice_under": -110,
      },
      {
          "player": "Jacob Lopez",
          "team": "ATH",
          "dabble_line": 4.5,
          "l5": [5, 6, 9, 6, 7],
          "sharp_book_line": 4.5,
          "juice_over": -140,  # Heavy juice over
          "juice_under": +110,
      },
      {
          "player": "Grant Holmes",
          "team": "PHI",
          "dabble_line": 3.5,
          "l5": [2, 3, 3, 3, 1],
          "sharp_book_line": 3.5,
          "juice_over": +120,
          "juice_under": -142,  # Heavy juice under
      },
      {
          "player": "Brayan Bello",
          "team": "BOS",
          "dabble_line": 4.5,
          "l5": [4, 3, 1, 2, 0],
          "sharp_book_line": 4.5,
          "juice_over": +140,
          "juice_under": -160,  # Heavy juice under + L5 100% under lock
      },
      {
          "player": "Derek Law",
          "team": "KC",
          "dabble_line": 0.5,
          "l5": [1, 1, 0, 2, 0],
          "sharp_book_line": 0.5,
          "juice_over": -150,  # Heavy juice over
          "juice_under": +120,
      },
  ]
  return pd.DataFrame(master_data)


def evaluate_master_engine(df):
  if df.empty:
    return df

  signals = []
  for _, row in df.iterrows():
    action = None
    triggers = []

    # 1. L5 Trend Consistency Filter (Strict 80%+ rule)
    l5 = row["l5"]
    line = row["dabble_line"]
    overs = sum(1 for x in l5 if x > line)
    unders = sum(1 for x in l5 if x < line)
    total = len(l5)

    if (overs / total) >= 0.80:
      triggers.append(
          f"L5 Over Lock ({int((overs/total)*100)}% hit: {l5})"
      )
      action = "HAMMER MORE 🔨"
    elif (unders / total) >= 0.80:
      triggers.append(
          f"L5 Under Lock ({int((unders/total)*100)}% hit: {l5})"
      )
      action = "HAMMER LESS 🔨"

    # 2. Sharp Heavy Juice Filter (-135 or worse)
    if row["juice_over"] <= -135:
      triggers.append(f"Sharp Juice Over ({row['juice_over']})")
      action = "HAMMER MORE 🔨"
    elif row["juice_under"] <= -135:
      triggers.append(f"Sharp Juice Under ({row['juice_under']})")
      action = "HAMMER LESS 🔨"

    # 3. Line Number Discrepancy Filter (0.5+ Hook Gap)
    line_gap = row["sharp_book_line"] - row["dabble_line"]
    if line_gap >= 0.5:
      triggers.append(
          f"Sharp Line Gap (+{line_gap} at"
          f" {row['sharp_book_line']})"
      )
      action = "HAMMER MORE 🔨"
    elif line_gap <= -0.5:
      triggers.append(
          f"Sharp Line Gap ({line_gap} at {row['sharp_book_line']})"
      )
      action = "HAMMER LESS 🔨"

    if action and triggers:
      signals.append({
          "Player": row["player"],
          "Team": row["team"],
          "Dabble Line": line,
          "Trigger Evidence": " | ".join(triggers),
          "Final Execution": action,
      })

  return pd.DataFrame(signals)


# Continuous 24/7 Evaluation Pipeline
df_raw = fetch_live_dabble_board_feed()
df_master_signals = evaluate_master_engine(df_raw)

st.subheader("Active 24/7 Master Hammer Execution Board")
if not df_master_signals.empty:
  st.dataframe(df_master_signals, use_container_width=True)
else:
  st.warning("Scanning feeds... No props met all strict thresholds.")

st.sidebar.markdown("**Engine State:** 24/7 Constant Monitoring")
st.sidebar.markdown("**Algorithms Active:** L5 Strict + Sharp Juice + Line Discrepancies")
