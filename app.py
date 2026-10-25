"""
Student Expense Tracker
=======================
A beginner-friendly web application for college students to record daily
expenses, monitor monthly budgets, and analyze spending patterns.

Technologies: Python 3, Streamlit, Pandas, Matplotlib, CSV File I/O
Author: Python Mentor & Student Team
"""

import os
from datetime import datetime, date
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# ==========================================
# CONSTANTS & CONFIGURATION
# ==========================================
CSV_FILE = "expenses.csv"
CATEGORIES = ["Food", "Travel", "Education", "Shopping", "Entertainment", "Other"]
CSV_COLUMNS = ["Date", "Category", "Amount", "Description"]

# Page setup: must be the very first Streamlit call
st.set_page_config(
    page_title="Student Expense Tracker",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom light styling to ensure clean layout
st.markdown(
    """
    <style>
    .metric-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .metric-title {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0f172a;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================
# DATA HELPER FUNCTIONS
# ==========================================
def load_expenses() -> pd.DataFrame:
    """
    Loads expense records from the local CSV file.
    If the file does not exist or is empty, returns an empty DataFrame
    with the required column structure.
    """
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=CSV_COLUMNS)

    try:
        df = pd.read_csv(CSV_FILE)
        # Ensure all required columns are present
        for col in CSV_COLUMNS:
            if col not in df.columns:
                df[col] = "" if col != "Amount" else 0.0

        # Data cleaning and type conversion
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0.0)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date

        # Drop invalid rows with missing dates or zero/negative amounts
        df = df.dropna(subset=["Date"])
        df = df[df["Amount"] > 0]
        return df
    except Exception as e:
        st.error(f"Error reading {CSV_FILE}: {e}")
        return pd.DataFrame(columns=CSV_COLUMNS)


def save_expenses(df: pd.DataFrame) -> None:
    """
    Saves the given DataFrame to the local CSV file.
    Formats dates consistently as YYYY-MM-DD.
    """
    # Ensure columns match standard format
    export_df = df[CSV_COLUMNS].copy()
    export_df["Date"] = pd.to_datetime(export_df["Date"]).dt.strftime("%Y-%m-%d")
    export_df.to_csv(CSV_FILE, index=False)


# ==========================================
# SIDEBAR: NAVIGATION & BUDGET CONTROLS
# ==========================================
st.sidebar.title("🎓 Student Tracker")
st.sidebar.caption("Track daily spending & manage campus life budget.")

# 1. Monthly Budget Input
st.sidebar.header("💰 Budget Settings")
if "monthly_budget" not in st.session_state:
    st.session_state["monthly_budget"] = 500.0  # default budget ($500)

monthly_budget = st.sidebar.number_input(
    "Set Monthly Budget ($)",
    min_value=10.0,
    max_value=50000.0,
    value=float(st.session_state["monthly_budget"]),
    step=25.0,
    help="Set your target spending limit for the current calendar month."
)
st.session_state["monthly_budget"] = monthly_budget

# 2. Add New Expense Form
st.sidebar.header("➕ Add New Expense")
with st.sidebar.form(key="expense_form", clear_on_submit=True):
    input_amount = st.number_input(
        "Amount ($)",
        min_value=0.0,
        value=0.0,
        step=1.0,
        format="%.2f",
        help="Enter the amount spent (must be greater than 0)."
    )

    input_category = st.selectbox(
        "Category",
        options=CATEGORIES,
        index=0,
        help="Choose the expense category."
    )

    input_date = st.date_input(
        "Date",
        value=date.today(),
        help="Date when the expense occurred."
    )

    input_desc = st.text_input(
        "Description",
        placeholder="e.g., Physics Textbook, Subway sandwich",
        max_chars=80,
        help="Brief note about the expense."
    )

    submit_button = st.form_submit_button("Record Expense", use_container_width=True)

    if submit_button:
        # Input Validation
        if input_amount <= 0:
            st.sidebar.error("❌ Amount must be greater than $0.00!")
        else:
            current_df = load_expenses()
            new_record = pd.DataFrame([{
                "Date": input_date,
                "Category": input_category,
                "Amount": round(float(input_amount), 2),
                "Description": input_desc.strip() if input_desc.strip() else "No description"
            }])
            updated_df = pd.concat([current_df, new_record], ignore_index=True)
            save_expenses(updated_df)
            st.sidebar.success(f"✅ Added ${input_amount:.2f} to {input_category}!")
            st.rerun()

# 3. Privacy & Storage Notice in Sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(
    "🔒 **Local Storage Notice**:\n"
    "Data is saved directly to `expenses.csv` on your computer. "
    "Files are stored in plain text and are not encrypted."
)


# ==========================================
# MAIN DASHBOARD CONTENT
# ==========================================
st.title("📊 Student Expense Tracker")
st.markdown(
    "Welcome to your personal college budgeting assistant. "
    "Record expenses from the sidebar to review spending metrics and visual charts below."
)

# Load existing expenses
df_all = load_expenses()

# Current Month Calculations for Budget
today = date.today()
current_month = today.month
current_year = today.year

if not df_all.empty:
    # Extract month and year for filtering
    df_all_dates = pd.to_datetime(df_all["Date"])
    this_month_mask = (df_all_dates.dt.month == current_month) & (df_all_dates.dt.year == current_year)
    this_month_expenses = df_all[this_month_mask]
    total_spent_this_month = this_month_expenses["Amount"].sum()
else:
    this_month_expenses = pd.DataFrame(columns=CSV_COLUMNS)
    total_spent_this_month = 0.0

remaining_budget = monthly_budget - total_spent_this_month
percent_budget_used = (total_spent_this_month / monthly_budget) * 100 if monthly_budget > 0 else 0.0

# ------------------------------------------
# BUDGET ALERTS & PROGRESS
# ------------------------------------------
if percent_budget_used >= 100:
    st.error(
        f"🚨 **Budget Exceeded!** You have spent **${total_spent_this_month:.2f}** this month, "
        f"which is **${abs(remaining_budget):.2f}** over your **${monthly_budget:.2f}** limit!"
    )
elif percent_budget_used >= 80:
    st.warning(
        f"⚠️ **Budget Warning:** You have used **{percent_budget_used:.1f}%** of your monthly budget. "
        f"Only **${remaining_budget:.2f}** remaining!"
    )
else:
    st.success(
        f"✨ **Budget on Track:** You have used **{percent_budget_used:.1f}%** of your monthly budget. "
        f"**${remaining_budget:.2f}** remaining."
    )

# Visual Progress Bar
clamped_progress = min(max(percent_budget_used / 100.0, 0.0), 1.0)
st.progress(clamped_progress, text=f"Monthly Budget Progress: {percent_budget_used:.1f}% used")

st.markdown("---")

# ------------------------------------------
# SUMMARY CARDS
# ------------------------------------------
# Determine highest spending category for this month (or overall if this month is empty)
if not this_month_expenses.empty:
    top_cat = this_month_expenses.groupby("Category")["Amount"].sum().idxmax()
    top_cat_amount = this_month_expenses.groupby("Category")["Amount"].sum().max()
    top_cat_str = f"{top_cat} (${top_cat_amount:.2f})"
elif not df_all.empty:
    top_cat = df_all.groupby("Category")["Amount"].sum().idxmax()
    top_cat_amount = df_all.groupby("Category")["Amount"].sum().max()
    top_cat_str = f"{top_cat} (${top_cat_amount:.2f})"
else:
    top_cat_str = "None yet"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">This Month's Spending</div>
            <div class="metric-value">${total_spent_this_month:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    remaining_color = "#dc2626" if remaining_budget < 0 else "#16a34a"
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Remaining Budget</div>
            <div class="metric-value" style="color: {remaining_color};">
                ${remaining_budget:.2f}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Top Category</div>
            <div class="metric-value" style="font-size: 1.25rem;">{top_cat_str}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    total_count = len(df_all)
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">Total Records</div>
            <div class="metric-value">{total_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)


# ------------------------------------------
# EMPTY STATE / DATA DISPLAY
# ------------------------------------------
if df_all.empty:
    st.info(
        "👋 **No expenses recorded yet!**\n\n"
        "Use the form in the left sidebar to add your first expense (e.g., Books, Groceries, Subway pass). "
        "Your metrics, charts, and table will appear right here automatically."
    )
else:
    # ------------------------------------------
    # FILTERS SECTION
    # ------------------------------------------
    st.subheader("🔍 Filter Expenses")

    min_date = min(df_all["Date"])
    max_date = max(df_all["Date"])

    f_col1, f_col2 = st.columns([1, 1])

    with f_col1:
        date_range = st.date_input(
            "Filter by Date Range",
            value=(min_date, max_date),
            help="Select start and end dates to filter transactions."
        )

    with f_col2:
        selected_categories = st.multiselect(
            "Filter by Category",
            options=CATEGORIES,
            default=CATEGORIES,
            help="Select one or more categories to display."
        )

    # Apply filters
    filtered_df = df_all.copy()

    # Apply date range filter safely
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_d, end_d = date_range
        filtered_df = filtered_df[(filtered_df["Date"] >= start_d) & (filtered_df["Date"] <= end_d)]
    elif isinstance(date_range, tuple) and len(date_range) == 1:
        filtered_df = filtered_df[filtered_df["Date"] >= date_range[0]]

    # Apply category filter
    if selected_categories:
        filtered_df = filtered_df[filtered_df["Category"].isin(selected_categories)]
    else:
        filtered_df = filtered_df.iloc[0:0]  # empty if nothing selected

    st.caption(f"Showing {len(filtered_df)} of {len(df_all)} total recorded transactions.")

    # ------------------------------------------
    # CHARTS: PIE & BAR CHARTS
    # ------------------------------------------
    st.subheader("📈 Spending Visualizations")

    if filtered_df.empty:
        st.warning("No expenses match the selected filters. Please adjust date range or categories.")
    else:
        chart_col1, chart_col2 = st.columns(2)

        # 1. Pie Chart: Spending by Category
        with chart_col1:
            st.markdown("##### Spending by Category")
            category_totals = filtered_df.groupby("Category")["Amount"].sum()

            fig1, ax1 = plt.subplots(figsize=(6, 5))
            colors = ["#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6", "#64748b"]

            wedges, texts, autotexts = ax1.pie(
                category_totals.values,
                labels=category_totals.index,
                autopct="%1.1f%%",
                startangle=140,
                colors=colors[:len(category_totals)],
                wedgeprops={"edgecolor": "white", "linewidth": 1.5}
            )
            for autotext in autotexts:
                autotext.set_color("white")
                autotext.set_fontsize(10)
                autotext.set_weight("bold")

            ax1.axis("equal")
            plt.tight_layout()
            st.pyplot(fig1)

        # 2. Bar Chart: Daily Spending Trend
        with chart_col2:
            st.markdown("##### Daily Spending")
            daily_totals = filtered_df.groupby("Date")["Amount"].sum().reset_index()
            daily_totals = daily_totals.sort_values("Date")

            fig2, ax2 = plt.subplots(figsize=(6, 5))
            dates_str = [d.strftime("%b %d") for d in daily_totals["Date"]]
            bars = ax2.bar(dates_str, daily_totals["Amount"], color="#3b82f6", edgecolor="#1d4ed8")

            ax2.set_xlabel("Date", fontsize=10, labelpad=8)
            ax2.set_ylabel("Total Spent ($)", fontsize=10, labelpad=8)
            ax2.grid(axis="y", linestyle="--", alpha=0.4)
            plt.xticks(rotation=45, ha="right", fontsize=9)

            for bar in bars:
                height = bar.get_height()
                ax2.annotate(
                    f"${height:.0f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=8
                )

            plt.tight_layout()
            st.pyplot(fig2)

    st.markdown("---")

    # ------------------------------------------
    # EXPENSE TABLE & DELETION
    # ------------------------------------------
    st.subheader("📋 Expense History")

    display_df = filtered_df.copy()
    display_df = display_df.sort_values(by="Date", ascending=False).reset_index(drop=True)

    formatted_table = display_df.copy()
    formatted_table["Amount"] = formatted_table["Amount"].apply(lambda x: f"${x:,.2f}")
    formatted_table["Date"] = pd.to_datetime(formatted_table["Date"]).dt.strftime("%Y-%m-%d")

    st.dataframe(
        formatted_table,
        use_container_width=True,
        hide_index=False
    )

    # Expense Deletion Tool
    with st.expander("🗑️ Delete an Expense Record"):
        st.write("Select an entry to permanently remove it from your records:")

        if not df_all.empty:
            options = []
            for idx, row in df_all.iterrows():
                label = f"#{idx + 1} | {row['Date']} | {row['Category']} | ${row['Amount']:.2f} ({row['Description']})"
                options.append((idx, label))

            selected_idx, selected_label = st.selectbox(
                "Select Expense to Delete",
                options=options,
                format_func=lambda x: x[1]
            )

            col_del, _ = st.columns([1, 4])
            with col_del:
                if st.button("Confirm Delete", type="primary", use_container_width=True):
                    updated_all = df_all.drop(index=selected_idx).reset_index(drop=True)
                    save_expenses(updated_all)
                    st.success(f"Deleted record {selected_label}!")
                    st.rerun()
