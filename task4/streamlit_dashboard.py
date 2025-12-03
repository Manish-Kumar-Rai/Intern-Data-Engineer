import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from Data_processing import analyze_folder, plot_revenue

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(page_title="Book Sales Dashboard", layout="wide")
st.title("📊 Book Sales Analytics Dashboard")


# Sidebar folder selection
st.sidebar.header("Select Dataset")
folder_options = {
    "DATA1": os.path.join(BASE_DIR, "data/DATA1"),
    "DATA2": os.path.join(BASE_DIR, "data/DATA2"),
    "DATA3": os.path.join(BASE_DIR, "data/DATA3")
}

selected_name = st.sidebar.selectbox("Choose dataset folder:", list(folder_options.keys()))
folder_path = folder_options[selected_name]

if not os.path.exists(folder_path):
    st.error(f"Folder not found: {folder_path}")
    st.stop()

# Run analysis (cached)
@st.cache_data
def run_analysis(path):
    return analyze_folder(path)

with st.spinner(f"Analyzing {selected_name}..."):
    results = run_analysis(folder_path)

# Display Top 5 Revenue Days & Key Metrics
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 5 Revenue Days")
    top5 = results["top5_days"].copy()
    top5.index = pd.to_datetime(top5.index).strftime("%Y-%m-%d")
    top5_df = top5.reset_index()
    top5_df.columns = ["Date", "Revenue (USD)"]
    st.dataframe(
        top5_df.style.format({"Revenue (USD)": "{:,.1f}"}),
        height=250,
        use_container_width=True
    )

    st.subheader("Key Metrics")
    st.metric("Unique Real Users", f"{results['unique_users']:,}")
    st.metric("Unique Author Sets", f"{results['unique_author_sets']:,}")

with col2:
    st.subheader("Most Popular Author Set")
    author_tuple = results["most_popular_author_set"]
    author_str = ", ".join(author_tuple) if author_tuple else "N/A"
    st.success(author_str)

    st.subheader("Best Buyer (All Aliases)")
    aliases = results["best_buyer_aliases"]
    if aliases:
        st.code(f"[{', '.join(map(str, sorted(aliases)))}]", language="text")
    else:
        st.info("No buyer data")

# Daily Revenue Bar Chart
st.subheader("Daily Revenue Over Time")
daily_series = results["daily_revenue"].copy()
daily_series.index = pd.to_datetime(daily_series.index)
daily_series_sorted = daily_series.sort_index()

fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(daily_series_sorted.index, daily_series_sorted.values,
              color='steelblue', edgecolor='black')

# Light background
ax.set_facecolor('#f9f9f9')
ax.grid(axis='y', linestyle='--', alpha=0.3)

# Labels and title
ax.set_title(f"Daily Revenue - {selected_name}", fontsize=16, pad=20)
ax.set_ylabel("Revenue (USD)", fontsize=12)
ax.set_xlabel("Date", fontsize=12)
plt.xticks(rotation=45)

# Annotate top 5 revenue days
top5_dates = daily_series_sorted.sort_values(ascending=False).head(5)
for bar, date in zip(bars, daily_series_sorted.index):
    if date in top5_dates.index:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                 f"{bar.get_height():.2f}", ha='center', va='bottom',
                 fontsize=9, fontweight='bold', color='darkred')

plt.tight_layout()
st.pyplot(fig)

# Optional: Save plot button
if st.button("Save Chart to plots/ folder"):
    plot_revenue(results["daily_revenue"], folder_path)
    st.success(f"Chart saved → plots/{os.path.basename(folder_path)}_daily_revenue.png")

st.caption("Created By Manish Rai")
