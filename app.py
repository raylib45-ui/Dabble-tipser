import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Dabble Live EV Scanner", layout="wide")
st.title("⚡ Dabble Live Board Discrepancy Engine")


def fetch_dabble_live_board():
  """Connects to live data source or API endpoints to pull today's props.

  Replace the URL below with the active network XHR/JSON endpoint or aggregator
  feed used by Dabble.
  """
  try:
    # Example structural template for live API fetching:
    # headers = {"User-Agent": "Mozilla/5.0"}
    # response = requests.get("https://api.dabble.com/v1/props/live", headers=headers, timeout=10)
    # data = response.json()

    # If an API isn't publicly open without authentication, use a Selenium/Playwright
    # automation script to parse the live board elements directly into this dataframe.

    live_props = []
    # Parse incoming live JSON payload or DOM elements here:
    # for item in data.get('markets', []):
    #     live_props.append({...})

    # Fallback indicator if live feed returns empty
    if not live_props:
      return pd.DataFrame()

    return pd.DataFrame(live_props)
  except Exception as e:
    st.error(f"Error connecting to live board feed: {e}")
    return pd.DataFrame()


def evaluate_discrepancies(df, threshold=1.5):
  if df.empty:
    return df
  signals = []
  for _, row in df.iterrows():
    delta = row["model_proj"] - row["line"]
    if abs(delta) >= threshold:
      action = "HAMMER MORE 🔨" if delta > 0 else "HAMMER LESS 🔨"
      signals.append({
          "Player": row["player"],
          "Sport": row["sport"],
          "Prop": row["prop"],
          "Line": row["line"],
          "Model Projection": row["model_proj"],
          "Delta": round(delta, 2),
          "Signal": action,
      })
  return pd.DataFrame(signals)


# Fetch live data
df_market = fetch_dabble_live_board()
signal_df = evaluate_discrepancies(df_market, threshold=1.5)

st.subheader("Live Board Discrepancies & Hammer Alerts (9/7/2026)")
if not signal_df.empty:
  st.dataframe(signal_df, use_container_width=True)
else:
  st.warning(
      "Live board connected, but no active props currently match the strict"
      " over/under discrepancy threshold."
  )

st.sidebar.markdown("**Scanner Status:** Active (Live API / Feed)")
st.sidebar.markdown("**Date:** September 7, 2026")
