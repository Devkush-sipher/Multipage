import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json
from datetime import datetime

# File paths
BASE_DIR = os.path.dirname(__file__)
EXPENSES_FILE = os.path.join(BASE_DIR, 'expenses.csv')
CATEGORIES_FILE = os.path.join(BASE_DIR, 'categories.json')
SUBCATEGORIES_FILE = os.path.join(BASE_DIR, 'subcategories.json')
SAVINGS_FILE = os.path.join(BASE_DIR, 'savings.csv')
BALANCE_FILE = os.path.join(BASE_DIR, 'balance.json')
INVESTMENT_TYPES_FILE = os.path.join(BASE_DIR, 'investment_types.json')

# ----------- Data Loaders & Savers -------------

def load_json(path, default):
    if os.path.exists(path):
        with open(path, 'r') as f:
            return json.load(f)
    return default

def save_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def load_categories():
    # returns list of categories
    return load_json(CATEGORIES_FILE, ['Food', 'Transport', 'Entertainment', 'Utilities', 'Debts', 'Other'])

def save_categories(categories):
    save_json(CATEGORIES_FILE, categories)

def load_subcategories():
    # dict: {category: [subcat1, subcat2,...]}
    return load_json(SUBCATEGORIES_FILE, {})

def save_subcategories(subcats):
    save_json(SUBCATEGORIES_FILE, subcats)

def load_investment_types():
    return load_json(INVESTMENT_TYPES_FILE, ['FD', 'Savings Account', 'Stocks', 'Crypto', 'Bonds', 'Real Estate'])

def save_investment_types(types):
    save_json(INVESTMENT_TYPES_FILE, types)

def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        return pd.read_csv(EXPENSES_FILE)
    return pd.DataFrame(columns=['Date', 'Category', 'Subcategory', 'Amount', 'Notes', 'Status'])

def save_expenses(df):
    df.to_csv(EXPENSES_FILE, index=False)

def load_savings():
    if os.path.exists(SAVINGS_FILE):
        return pd.read_csv(SAVINGS_FILE)
    return pd.DataFrame(columns=['Date', 'InvestmentType', 'Amount', 'City', 'Area', 'Notes'])

def save_savings(df):
    df.to_csv(SAVINGS_FILE, index=False)

def load_balance():
    return load_json(BALANCE_FILE, {"base_balance": 0.0})

def save_balance(data):
    save_json(BALANCE_FILE, data)

# ----------- Data Initialization -------------

categories = load_categories()
subcategories = load_subcategories()
investment_types = load_investment_types()
df_exp = load_expenses()
df_save = load_savings()
balance_data = load_balance()

# Ensure datetime format
df_exp['Date'] = pd.to_datetime(df_exp['Date'], errors='coerce')
df_exp = df_exp[df_exp['Date'].notna()]
df_save['Date'] = pd.to_datetime(df_save['Date'], errors='coerce')
df_save = df_save[df_save['Date'].notna()]

# Calculate balances
savings_account_total = df_save[df_save['InvestmentType'] == 'Savings Account']['Amount'].sum()
paid_debts_total = df_exp[(df_exp['Status'] == 'Paid') & (df_exp['Category'] == 'Debts')]['Amount'].sum()

bank_balance = balance_data.get('base_balance', 0) + savings_account_total - paid_debts_total
total_investments = df_save['Amount'].sum() - savings_account_total
net_worth = bank_balance + total_investments

balance_data['base_balance'] = balance_data.get('base_balance', 0)
save_balance(balance_data)

# Streamlit config
st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("💰 Financial Dashboard")

# ----------- Sidebar: Base balance & Manage Categories/Subcategories/Investment Types -------------

st.sidebar.header("Setup Base Bank Balance")
base_balance_input = st.sidebar.number_input("Base Balance (₹)", min_value=0.0, value=balance_data.get('base_balance', 0.0), step=1000.0, format="%.2f")
if base_balance_input != balance_data.get('base_balance', 0.0):
    balance_data['base_balance'] = base_balance_input
    save_balance(balance_data)
    st.rerun()

st.sidebar.markdown("---")

# Manage Categories
with st.sidebar.expander("Manage Expense Categories and Subcategories"):
    st.subheader("Categories")
    new_cat = st.text_input("Add New Category")
    if st.button("Add Category"):
        if new_cat and new_cat not in categories:
            categories.append(new_cat)
            save_categories(categories)
            subcategories[new_cat] = []
            save_subcategories(subcategories)
            st.success(f"Added category '{new_cat}'")
        elif new_cat in categories:
            st.warning(f"Category '{new_cat}' already exists")

    st.subheader("Subcategories")
    selected_cat = st.selectbox("Select Category to Manage Subcategories", options=categories)
    current_subcats = subcategories.get(selected_cat, [])
    new_subcat = st.text_input("Add New Subcategory")
    if st.button("Add Subcategory"):
        if new_subcat and new_subcat not in current_subcats:
            current_subcats.append(new_subcat)
            subcategories[selected_cat] = current_subcats
            save_subcategories(subcategories)
            st.success(f"Added subcategory '{new_subcat}' to '{selected_cat}'")
        elif new_subcat in current_subcats:
            st.warning(f"Subcategory '{new_subcat}' already exists in '{selected_cat}'")

    if current_subcats:
        st.write(f"Subcategories under '{selected_cat}':")
        for sc in current_subcats:
            if st.button(f"Delete Subcategory: {sc}"):
                current_subcats.remove(sc)
                subcategories[selected_cat] = current_subcats
                save_subcategories(subcategories)
                st.success(f"Deleted subcategory '{sc}'")
                st.rerun()

st.sidebar.markdown("---")

# Manage Investment Types
with st.sidebar.expander("Manage Investment Types"):
    new_inv_type = st.text_input("Add New Investment Type")
    if st.button("Add Investment Type"):
        if new_inv_type and new_inv_type not in investment_types:
            investment_types.append(new_inv_type)
            save_investment_types(investment_types)
            st.success(f"Added investment type '{new_inv_type}'")
        elif new_inv_type in investment_types:
            st.warning(f"Investment type '{new_inv_type}' already exists")
    if investment_types:
        for inv_type in investment_types:
            if st.button(f"Delete Investment Type: {inv_type}"):
                investment_types.remove(inv_type)
                save_investment_types(investment_types)
                st.success(f"Deleted investment type '{inv_type}'")
                st.rerun()

st.sidebar.markdown("---")

# ----------- Show Balances -------------

st.markdown(f"### 🏦 Bank Balance: ₹{bank_balance:,.2f}")
st.markdown(f"### 📈 Estimated Net Worth: ₹{net_worth:,.2f}")

# ----------- Tabs -------------

tabs = st.tabs(["Expenses", "Savings & Investments"])

with tabs[0]:
    st.header("📉 Expense Tracker")

    # Filters
    with st.expander("Filters"):
        date_filter = st.date_input("Date Range", [datetime(2000,1,1), datetime.today()])
        status_filter = st.selectbox("Status", ["All", "Paid", "Pending"])
        category_filter = st.multiselect("Filter by Category", categories)
        # Subcategory filter depends on selected categories
        filtered_subcats = []
        if category_filter:
            for cat in category_filter:
                filtered_subcats.extend(subcategories.get(cat, []))
        subcategory_filter = st.multiselect("Filter by Subcategory", filtered_subcats)

    start_date, end_date = date_filter
    filtered_exp = df_exp[
        (df_exp['Date'] >= pd.to_datetime(start_date)) &
        (df_exp['Date'] <= pd.to_datetime(end_date))
    ]

    if status_filter != "All":
        filtered_exp = filtered_exp[filtered_exp['Status'] == status_filter]
    if category_filter:
        filtered_exp = filtered_exp[filtered_exp['Category'].isin(category_filter)]
    if subcategory_filter:
        filtered_exp = filtered_exp[filtered_exp['Subcategory'].isin(subcategory_filter)]

    # Add Expense
    st.subheader("Add New Expense")
    with st.form("expense_form", clear_on_submit=True):
        # Sync default date with device time
        date = st.date_input("Date", value=datetime.now())
        category = st.selectbox("Category", categories)
        # Show subcategory dropdown dynamically based on selected category
        subs = subcategories.get(category, [])
        if subs:
            subcat = st.selectbox("Subcategory", subs)
        else:
            subcat = st.text_input("Subcategory (Optional)")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        notes = st.text_input("Notes")
        status = st.selectbox("Status", ["Paid", "Pending"])
        submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_row = {
            'Date': pd.to_datetime(date),
            'Category': category,
            'Subcategory': subcat if subcat else "",
            'Amount': amount,
            'Notes': notes,
            'Status': status
        }
        df_exp = pd.concat([df_exp, pd.DataFrame([new_row])], ignore_index=True)
        save_expenses(df_exp)
        st.success("Expense added!")
        st.rerun()

    # Show expenses with inline editing & delete buttons
    st.subheader("Expenses Table")
    if filtered_exp.empty:
        st.info("No expenses match the current filters.")
    else:
        for idx, row in filtered_exp.sort_values(by='Date', ascending=False).iterrows():
            cols = st.columns([2, 2, 2, 2, 3, 1, 1])
            cols[0].write(row['Date'].date())
            cols[1].write(row['Category'])
            cols[2].write(row['Subcategory'])
            # Inline editable amount
            new_amt = cols[3].number_input(f"Amount_{idx}", min_value=0.0, value=float(row['Amount']), key=f"exp_amt_{idx}")
            notes_val = cols[4].text_input(f"Notes_{idx}", value=row['Notes'], key=f"exp_notes_{idx}")
            status_val = cols[5].selectbox(f"Status_{idx}", options=["Paid", "Pending"], index=0 if row['Status']=='Paid' else 1, key=f"exp_status_{idx}")
            if new_amt != row['Amount'] or notes_val != row['Notes'] or status_val != row['Status']:
                df_exp.at[idx, 'Amount'] = new_amt
                df_exp.at[idx, 'Notes'] = notes_val
                df_exp.at[idx, 'Status'] = status_val
                save_expenses(df_exp)
                st.success(f"Expense updated (ID: {idx})")
                st.rerun()

            # Delete button
            if cols[6].button(f"Delete_{idx}"):
                df_exp = df_exp.drop(idx).reset_index(drop=True)
                save_expenses(df_exp)
                st.success(f"Deleted expense (ID: {idx})")
                st.rerun()

    # Pending expenses list with mark as paid
    st.subheader("Pending Expenses")
    pending_exp = df_exp[df_exp['Status'] == 'Pending']
    if pending_exp.empty:
        st.info("No pending expenses.")
    else:
        for idx, row in pending_exp.iterrows():
            st.write(f"{row['Date'].date()} | ₹{row['Amount']} | {row['Category']} | {row['Subcategory']} | {row['Notes']}")
            if st.button(f"Mark Paid: {idx}", key=f"mark_paid_{idx}"):
                df_exp.at[idx, 'Status'] = 'Paid'
                save_expenses(df_exp)
                st.success("Marked as Paid")
                st.rerun()

    # Pie charts for Paid and Pending Expenses by Category
    paid_exp = df_exp[df_exp['Status'] == 'Paid']
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Paid Expenses by Category")
        if not paid_exp.empty:
            fig1 = px.pie(paid_exp, names='Category', values='Amount')
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("No paid expenses to show.")
    with col2:
        st.markdown("### Pending Expenses by Category")
        pending_exp = df_exp[df_exp['Status'] == 'Pending']
        if not pending_exp.empty:
            fig2 = px.pie(pending_exp, names='Category', values='Amount')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No pending expenses to show.")

with tabs[1]:
    st.header("📈 Savings & Investments")

    # Filters for savings
    with st.expander("Filters"):
        save_date_filter = st.date_input("Savings Date Range", [datetime(2000,1,1), datetime.today()])
        save_inv_filter = st.multiselect("Investment Types", options=investment_types, default=investment_types)

    s_start, s_end = save_date_filter
    df_filtered_save = df_save[
        (df_save['Date'] >= pd.to_datetime(s_start)) &
        (df_save['Date'] <= pd.to_datetime(s_end))
    ]
    if save_inv_filter:
        df_filtered_save = df_filtered_save[df_filtered_save['InvestmentType'].isin(save_inv_filter)]

    # Add Investment
    st.subheader("Add Investment")
    with st.form("savings_form", clear_on_submit=True):
        s_date = st.date_input("Date", value=datetime.now(), key="s_date")
        s_type = st.selectbox("Investment Type", investment_types)
        s_amount = st.number_input("Amount", min_value=0.0, format="%.2f", key="s_amount")
        s_notes = st.text_input("Notes", key="s_notes")

        s_city = ""
        s_area = ""
        if s_type == "Real Estate":
            s_city = st.text_input("City", key="s_city")
            s_area = st.text_input("Area", key="s_area")

        s_submit = st.form_submit_button("Add Investment")

    if s_submit:
        new_inv = {
            'Date': pd.to_datetime(s_date),
            'InvestmentType': s_type,
            'Amount': s_amount,
            'City': s_city if s_type == "Real Estate" else "",
            'Area': s_area if s_type == "Real Estate" else "",
            'Notes': s_notes
        }
        df_save = pd.concat([df_save, pd.DataFrame([new_inv])], ignore_index=True)
        save_savings(df_save)
        st.success("Investment added!")
        st.rerun()

    # Investments table with inline edit and delete
    st.subheader("Investments Table")
    if df_filtered_save.empty:
        st.info("No investments match the current filters.")
    else:
        for idx, row in df_filtered_save.sort_values(by='Date', ascending=False).iterrows():
            cols = st.columns([2, 2, 2, 2, 2, 1])
            cols[0].write(row['Date'].date())
            cols[1].write(row['InvestmentType'])
            new_amt = cols[2].number_input(f"Inv_Amount_{idx}", min_value=0.0, value=float(row['Amount']), key=f"inv_amt_{idx}")
            notes_val = cols[3].text_input(f"Inv_Notes_{idx}", value=row['Notes'], key=f"inv_notes_{idx}")
            city_val = row['City']
            area_val = row['Area']
            if row['InvestmentType'] == "Real Estate":
                city_val = cols[4].text_input(f"City_{idx}", value=row['City'], key=f"inv_city_{idx}")
                area_val = cols[5].text_input(f"Area_{idx}", value=row['Area'], key=f"inv_area_{idx}")
            else:
                cols[4].write("")
                cols[5].write("")

            # Save changes if any
            if new_amt != row['Amount'] or notes_val != row['Notes'] or city_val != row['City'] or area_val != row['Area']:
                df_save.at[idx, 'Amount'] = new_amt
                df_save.at[idx, 'Notes'] = notes_val
                if row['InvestmentType'] == "Real Estate":
                    df_save.at[idx, 'City'] = city_val
                    df_save.at[idx, 'Area'] = area_val
                save_savings(df_save)
                st.success(f"Investment updated (ID: {idx})")
                st.rerun()

            # Delete button
            if cols[-1].button(f"Delete_Inv_{idx}"):
                df_save = df_save.drop(idx).reset_index(drop=True)
                save_savings(df_save)
                st.success(f"Deleted investment (ID: {idx})")
                st.rerun()

    # Pie chart for investments by type
    if not df_filtered_save.empty:
        fig3 = px.pie(df_filtered_save, names='InvestmentType', values='Amount', title="Investments by Type")
        st.plotly_chart(fig3, use_container_width=True)


