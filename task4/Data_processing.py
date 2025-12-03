import os
import re
import sys
import pandas as pd
import numpy as np
import yaml
import matplotlib.pyplot as plt
from dateutil import parser
from collections import defaultdict
from typing import List, Dict, Any
from tabulate import tabulate
from textwrap import fill

EUR_TO_USD = 1.2


# LOAD BOOKS.YAML
def load_books(path: str) -> pd.DataFrame:
    with open(path, "r", encoding="utf-8") as f:
        books = yaml.safe_load(f)

    df = pd.DataFrame(books)
    df.columns = [c.replace(":", "") for c in df.columns]

    df["author_list"] = df["author"].apply(
        lambda x: tuple(sorted([a.strip() for a in str(x).split(",")])))
    return df

# CLEAN PRICE
def parse_price(x: Any) -> float:
    if pd.isna(x):
        return np.nan

    s = str(x).strip().replace("USD", "").replace("usd", "").replace("¢", ".") \
        .replace("$", "").replace("€", "").replace(" ", "")

    try:
        val = float(s)
    except:
        match = re.findall(r"[0-9\.]+", s)
        val = float(match[0]) if match else np.nan

    return val * EUR_TO_USD if "€" in str(x) else val

#CLEAN TIMESTAMP
def parse_timestamp(x: Any) -> pd.Timestamp:
    if pd.isna(x):
        return pd.NaT
    s = str(x).replace("A.M.", "AM").replace("P.M.", "PM").replace(";", " ").replace(",", " ")
    try:
        return parser.parse(s)
    except:
        return pd.NaT

# LOAD ORDERS
def load_orders(path: str) -> pd.DataFrame:
    df = pd.read_parquet(path)
    df["unit_price_clean"] = df["unit_price"].apply(parse_price)
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["timestamp_clean"] = df["timestamp"].apply(parse_timestamp)
    df["date"] = df["timestamp_clean"].dt.date
    df["paid_price"] = df["quantity"] * df["unit_price_clean"]
    return df

# 5. LOAD USERS
def load_users(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

# 6. USER RECONCILIATION
def reconcile_users(users: pd.DataFrame) -> List[List[int]]:
    fields = ["name", "address", "phone", "email"]
    groups_dict = defaultdict(list)

    for _, row in users.iterrows():
        for i in range(len(fields)):
            key = tuple(row[fields[j]] if j != i else None for j in range(len(fields)))
            groups_dict[key].append(row["id"])

    return list(groups_dict.values())

# MERGE BOOKS & ORDERS
def compute_author_sets(books: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    merged = orders.merge(
        books[["id", "author_list"]],
        left_on="book_id",
        right_on="id",
        how="left",
        suffixes=("", "_book")
    )
    return merged

# FULL ANALYSIS PIPELINE
def analyze_folder(folder_path: str) -> Dict[str, Any]:
    books = load_books(os.path.join(folder_path, "books.yaml"))
    users = load_users(os.path.join(folder_path, "users.csv"))
    orders = load_orders(os.path.join(folder_path, "orders.parquet"))
    orders2 = compute_author_sets(books, orders)
    daily_rev = orders2.groupby("date")["paid_price"].sum().sort_values(ascending=False)

    # Alias groups
    user_groups = reconcile_users(users)
    unique_users_count = len(user_groups)
    unique_author_sets = orders2["author_list"].nunique()

    # Most popular author set
    if not orders2.empty:
        pop_author_set = (
            orders2.groupby("author_list")["quantity"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )
    else:
        pop_author_set = ()

    # Top Customer Group (PAYING)
    if not orders2.empty:
        # Compute spending per user_id
        spending = orders2.groupby("user_id")["paid_price"].sum()

        # Map user_id → alias group
        groups = reconcile_users(users)

        # Compute group spending
        group_spending = {}
        for members in groups:
            total = sum(spending.get(uid, 0) for uid in members)
            group_spending[tuple(members)] = total

        # Find highest spending group
        top_group = max(group_spending, key=group_spending.get)
        top_customer = sorted(list(top_group))
    else:
        top_customer = []

    return {
        "top5_days": daily_rev.head(5),
        "unique_users": unique_users_count,
        "unique_author_sets": unique_author_sets,
        "most_popular_author_set": pop_author_set,
        "top_customer": top_customer,
        "daily_revenue": daily_rev
    }

# PLOT DAILY REVENUE
def plot_revenue(daily_rev: pd.Series, folder_path: str, save_dir: str = "plots") -> None:
    plt.figure(figsize=(12, 6))

    # Sort by date
    daily_rev_sorted = daily_rev.sort_index()

    # Create blue bars
    bars = plt.bar(daily_rev_sorted.index, daily_rev_sorted.values, color='steelblue', edgecolor='black')

    # Light background and grid
    plt.gca().set_facecolor('#f9f9f9')  # Light gray background
    plt.grid(axis='y', linestyle='--', alpha=0.5)

    # Labels and title
    folder_name = os.path.basename(os.path.normpath(folder_path))
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Revenue (USD)", fontsize=12)
    plt.title(f"Daily Revenue (USD) - {folder_name}", fontsize=14)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')

    # Annotate top 5 revenue days
    top5 = daily_rev_sorted.sort_values(ascending=False).head(5)
    for bar, date in zip(bars, daily_rev_sorted.index):
        if date in top5.index:
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(),
                     f"{bar.get_height():.2f}", ha='center', va='bottom',
                     fontsize=9, fontweight='bold', color='darkred')

    plt.tight_layout()

    # Save plot
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{folder_name}_daily_revenue.png")
    plt.savefig(save_path, dpi=300)
    plt.close()


def wrap_text_list(items, width=80, indent="    "):
    if not items:
        return "None"
    text = ", ".join(map(str, items))
    return fill(text, width=width, subsequent_indent=indent)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Data_processing.py <data_folder1> [<data_folder2> ...]")
        sys.exit(1)

    folders = sys.argv[1:]

    for folder_name in folders:
        results = analyze_folder(folder_name)

        file_name = os.path.basename(os.path.normpath(folder_name))

        print(f"\n=== RESULTS FOR {file_name} ===\n")

        # Table: Top 5 Revenue Days
        top5_df = results["top5_days"].reset_index()
        top5_df.columns = ["Date", "Revenue (USD)"]
        print(tabulate(top5_df, headers="keys", tablefmt="fancy_grid", showindex=False))

        # Summary table
        pop_authors = ", ".join(results["most_popular_author_set"]) if results["most_popular_author_set"] else "None"
        best_aliases = ", ".join(map(str, results["top_customer"])) if results["top_customer"] else "None"


        wrapped_aliases = wrap_text_list(results["top_customer"], width=100)
        wrapped_authors = ", ".join(results["most_popular_author_set"]) if results["most_popular_author_set"] else "None"

        summary = [
            ["Unique users", results["unique_users"]],
            ["Unique author sets", results["unique_author_sets"]],
            ["Most popular author set", wrapped_authors],
            ["Top Customer aliases", wrapped_aliases]
        ]

        print("\n" + tabulate(summary, headers=["Metric", "Value"], tablefmt="fancy_grid"))

        # Plot
        if not results["daily_revenue"].empty:
            plot_revenue(results["daily_revenue"], folder_name)
            print(f"\nSaved plot to plots/{file_name}_daily_revenue.png\n")
