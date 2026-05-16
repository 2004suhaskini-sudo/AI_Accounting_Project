import streamlit as st
import pandas as pd
import os
import re
from datetime import datetime

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="AI Accounting System",
    layout="wide"
)

st.title("AI-Based Financial Transaction Analysis & Automated Journal Entry System")

transaction = st.text_input("Enter Accounting Transaction")


# ------------------------------------------------
# EXTRACT AMOUNT
# ------------------------------------------------

def extract_amount(text):

    numbers = re.findall(r'\d+(?:\.\d+)?', text)

    if numbers:
        return int(float(numbers[0]))

    return 0


# ------------------------------------------------
# AI ACCOUNTING ENGINE
# ------------------------------------------------

def generate_entry(text):

    text = text.lower()

    amount = extract_amount(text)

    # ------------------------------------------------
    # PAYMENT MODE
    # ------------------------------------------------

    if "credit" in text:
        payment_account = "Creditor Account"

    elif "bank" in text:
        payment_account = "Bank Account"

    elif "cash" in text:
        payment_account = "Cash/Bank Account"

    else:
        payment_account = "Cash/Bank Account"

    # ------------------------------------------------
    # CONTRA ENTRIES
    # ------------------------------------------------

    if "cash deposited" in text or "deposited into bank" in text:

        return {
            "Category": "Contra Entry",
            "Debit": "Bank Account",
            "Credit": "Cash Account",
            "Amount": amount
        }

    elif "cash withdrawn" in text or "withdrawn from bank" in text:

        return {
            "Category": "Contra Entry",
            "Debit": "Cash Account",
            "Credit": "Bank Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # BAD DEBTS
    # ------------------------------------------------

    elif "bad debt" in text or "written off" in text:

        return {
            "Category": "Bad Debts",
            "Debit": "Bad Debts Account",
            "Credit": "Debtor Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # PROVISION FOR DOUBTFUL DEBTS
    # ------------------------------------------------

    elif "provision" in text or "doubtful debt" in text:

        return {
            "Category": "Provision for Doubtful Debts",
            "Debit": "Profit & Loss Account",
            "Credit": "Provision for Doubtful Debts Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # DISCOUNT ALLOWED
    # ------------------------------------------------

    elif "discount allowed" in text:

        return {
            "Category": "Discount Allowed",
            "Debit": "Discount Allowed Account",
            "Credit": "Debtor Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # DISCOUNT RECEIVED
    # ------------------------------------------------

    elif "discount received" in text:

        return {
            "Category": "Discount Received",
            "Debit": "Creditor Account",
            "Credit": "Discount Received Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # PURCHASE RETURNS
    # ------------------------------------------------

    elif "purchase return" in text or "returned goods to supplier" in text:

        return {
            "Category": "Purchase Return",
            "Debit": "Creditor Account",
            "Credit": "Purchase Return Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # SALES RETURNS
    # ------------------------------------------------

    elif "sales return" in text or "goods returned by customer" in text:

        return {
            "Category": "Sales Return",
            "Debit": "Sales Return Account",
            "Credit": "Debtor/Cash Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # OUTSTANDING EXPENSES
    # ------------------------------------------------

    elif "outstanding expense" in text or "outstanding salary" in text:

        return {
            "Category": "Outstanding Expense",
            "Debit": "Expense Account",
            "Credit": "Outstanding Expense Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # PREPAID EXPENSES
    # ------------------------------------------------

    elif "prepaid expense" in text or "prepaid rent" in text:

        return {
            "Category": "Prepaid Expense",
            "Debit": "Prepaid Expense Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # OUTSTANDING INCOME
    # ------------------------------------------------

    elif "outstanding income" in text or "accrued income" in text:

        return {
            "Category": "Outstanding Income",
            "Debit": "Outstanding Income Account",
            "Credit": "Income Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # INCOME RECEIVED IN ADVANCE
    # ------------------------------------------------

    elif "income received in advance" in text or "unearned income" in text:

        return {
            "Category": "Income Received in Advance",
            "Debit": payment_account,
            "Credit": "Income Received in Advance Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # DEPRECIATION
    # ------------------------------------------------

    elif "depreciation" in text:

        if "machinery" in text:
            asset = "Machinery"

        elif "furniture" in text:
            asset = "Furniture"

        elif "vehicle" in text:
            asset = "Vehicle"

        else:
            asset = "Asset"

        return {
            "Category": f"Depreciation on {asset}",
            "Debit": "Depreciation Expense Account",
            "Credit": f"Accumulated Depreciation on {asset} Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # CAPITAL EXPENDITURE
    # ------------------------------------------------

    elif "capital expenditure" in text:

        return {
            "Category": "Capital Expenditure",
            "Debit": "Asset Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # REVENUE EXPENDITURE
    # ------------------------------------------------

    elif "revenue expenditure" in text:

        return {
            "Category": "Revenue Expenditure",
            "Debit": "Expense Account",
            "Credit": payment_account,
            "Amount": amount
        }
    
    # ------------------------------------------------
    # COMPOUND SALES
    # ------------------------------------------------

    elif (
        ("sale" in text or "sales" in text or "sold" in text)
        and
        ("partly" in text or "partly cash" in text)
    ):

        debit_account = "Cash/Bank Account + Debtor Account"

        return {
            "Category": "Compound Sales Transaction",
            "Debit": debit_account,
            "Credit": "Sales Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # NORMAL SALES
    # ------------------------------------------------

    elif "sale" in text or "sales" in text or "sold" in text:

        if "credit" in text:
            debit_account = "Debtor Account"

        elif "cash" in text:
            debit_account = "Cash Account"

        elif "bank" in text:
            debit_account = "Bank Account"

        else:
            debit_account = "Cash/Bank Account"

        return {
            "Category": "Sales Revenue",
            "Debit": debit_account,
            "Credit": "Sales Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # COMPOUND TRANSACTIONS
    # ------------------------------------------------

    elif (
        ("purchase" in text or "purchases" in text)
        and
        ("partly cash" in text or "balance on credit" in text)
    ):

        if any(word in text for word in [
            "machinery", "machine", "equipment", "plant"
        ]):

            debit_account = "Machinery Account"

        elif any(word in text for word in [
            "furniture", "table", "chair",
            "desk", "cabinet", "cupboard", "sofa"
        ]):

            debit_account = "Furniture Account"

        elif any(word in text for word in [
            "vehicle", "car", "truck", "van"
        ]):

            debit_account = "Vehicle Account"

        elif any(word in text for word in [
            "inventory", "stock", "goods", "raw material"
        ]):

            debit_account = "Inventory Account"

        else:

            debit_account = "Relevant Asset/Purchase Account"

        return {
            "Category": "Compound Purchase Transaction",
            "Debit": debit_account,
            "Credit": "Cash/Bank Account + Creditor Account",
            "Amount": amount
        }
    
    # ------------------------------------------------
    # PURCHASES
    # ------------------------------------------------

    elif "purchase" in text or "purchases" in text:

        return {
            "Category": "Purchase Transaction",
            "Debit": "Purchase Account",
            "Credit": payment_account,
            "Amount": amount
        }
    
    # ------------------------------------------------
    # EQUITY SHARES ISSUED AT PAR
    # ------------------------------------------------

    elif "equity share" in text and "issued" in text and "par" in text:

        return {
            "Category": "Issue of Equity Shares at Par",
            "Debit": "Bank Account",
            "Credit": "Equity Share Capital Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # EQUITY SHARES ISSUED AT PREMIUM
    # ------------------------------------------------

    elif "equity share" in text and "issued" in text and "premium" in text:

        return {
            "Category": "Issue of Equity Shares at Premium",
            "Debit": "Bank Account",
            "Credit": "Equity Share Capital Account + Securities Premium Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # EQUITY SHARES ISSUED AT DISCOUNT
    # ------------------------------------------------

    elif "equity share" in text and "issued" in text and "discount" in text:

        return {
            "Category": "Issue of Equity Shares at Discount",
            "Debit": "Bank Account + Discount on Issue of Shares Account",
            "Credit": "Equity Share Capital Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # PREFERENCE SHARES ISSUED AT PAR
    # ------------------------------------------------

    elif "preference share" in text and "issued" in text and "par" in text:

        return {
            "Category": "Issue of Preference Shares at Par",
            "Debit": "Bank Account",
            "Credit": "Preference Share Capital Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # PREFERENCE SHARES ISSUED AT PREMIUM
    # ------------------------------------------------

    elif "preference share" in text and "issued" in text and "premium" in text:

        return {
            "Category": "Issue of Preference Shares at Premium",
            "Debit": "Bank Account",
            "Credit": "Preference Share Capital Account + Securities Premium Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # PREFERENCE SHARES ISSUED AT DISCOUNT
    # ------------------------------------------------

    elif "preference share" in text and "issued" in text and "discount" in text:

        return {
            "Category": "Issue of Preference Shares at Discount",
            "Debit": "Bank Account + Discount on Issue of Shares Account",
            "Credit": "Preference Share Capital Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # REDEMPTION OF PREFERENCE SHARES AT PAR
    # ------------------------------------------------

    elif "preference share" in text and "redeemed" in text and "par" in text:

        return {
            "Category": "Redemption of Preference Shares at Par",
            "Debit": "Preference Share Capital Account",
            "Credit": "Bank Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # REDEMPTION OF PREFERENCE SHARES AT PREMIUM
    # ------------------------------------------------

    elif "preference share" in text and "redeemed" in text and "premium" in text:

        return {
            "Category": "Redemption of Preference Shares at Premium",
            "Debit": "Preference Share Capital Account + Premium on Redemption Account",
            "Credit": "Bank Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # REDEMPTION OF PREFERENCE SHARES AT DISCOUNT
    # ------------------------------------------------

    elif "preference share" in text and "redeemed" in text and "discount" in text:

        return {
            "Category": "Redemption of Preference Shares at Discount",
            "Debit": "Preference Share Capital Account",
            "Credit": "Bank Account + Capital Reserve Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # DEBENTURES ISSUED AT PAR
    # ------------------------------------------------

    elif "debenture" in text and "issued" in text and "par" in text:

        return {
            "Category": "Issue of Debentures at Par",
            "Debit": "Bank Account",
            "Credit": "Debentures Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # DEBENTURES ISSUED AT PREMIUM
    # ------------------------------------------------

    elif "debenture" in text and "issued" in text and "premium" in text:

        return {
            "Category": "Issue of Debentures at Premium",
            "Debit": "Bank Account",
            "Credit": "Debentures Account + Securities Premium Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # DEBENTURES ISSUED AT DISCOUNT
    # ------------------------------------------------

    elif "debenture" in text and "issued" in text and "discount" in text:

        return {
            "Category": "Issue of Debentures at Discount",
            "Debit": "Bank Account + Discount on Issue of Debentures Account",
            "Credit": "Debentures Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # REDEMPTION OF DEBENTURES AT PAR
    # ------------------------------------------------

    elif "debenture" in text and "redeemed" in text and "par" in text:

        return {
            "Category": "Redemption of Debentures at Par",
            "Debit": "Debentures Account",
            "Credit": "Bank Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # REDEMPTION OF DEBENTURES AT PREMIUM
    # ------------------------------------------------

    elif "debenture" in text and "redeemed" in text and "premium" in text:

        return {
            "Category": "Redemption of Debentures at Premium",
            "Debit": "Debentures Account + Premium on Redemption of Debentures Account",
            "Credit": "Bank Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # REDEMPTION OF DEBENTURES AT DISCOUNT
    # ------------------------------------------------

    elif "debenture" in text and "redeemed" in text and "discount" in text:

        return {
            "Category": "Redemption of Debentures at Discount",
            "Debit": "Debentures Account",
            "Credit": "Bank Account + Capital Reserve Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # CONSULTING / COMMISSION / SERVICE INCOME
    # ------------------------------------------------

    elif "consulting" in text:

        return {
            "Category": "Consulting Income",
            "Debit": payment_account,
            "Credit": "Consulting Income Account",
            "Amount": amount
        }

    elif "commission" in text:

        return {
            "Category": "Commission Income",
            "Debit": payment_account,
            "Credit": "Commission Income Account",
            "Amount": amount
        }

    elif "income" in text or "revenue" in text or "received" in text:

        return {
            "Category": "Business Income",
            "Debit": payment_account,
            "Credit": "Income Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # FURNITURE
    # ------------------------------------------------

    elif any(word in text for word in [
        "furniture", "table", "chair",
        "desk", "cabinet", "cupboard", "sofa"
    ]):

        return {
            "Category": "Furniture Purchase",
            "Debit": "Furniture Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # MACHINERY
    # ------------------------------------------------

    elif any(word in text for word in [
        "machinery", "machine", "equipment", "plant"
    ]):

        return {
            "Category": "Machinery Purchase",
            "Debit": "Machinery Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # VEHICLE
    # ------------------------------------------------

    elif any(word in text for word in [
        "vehicle", "car", "truck", "van"
    ]):

        return {
            "Category": "Vehicle Purchase",
            "Debit": "Vehicle Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # INVENTORY
    # ------------------------------------------------

    elif any(word in text for word in [
        "inventory", "stock", "goods", "raw material"
    ]):

        return {
            "Category": "Inventory Purchase",
            "Debit": "Inventory Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # SALARY
    # ------------------------------------------------

    elif "salary" in text or "wages" in text:

        return {
            "Category": "Salary Expense",
            "Debit": "Salary Expense Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # RENT
    # ------------------------------------------------

    elif "rent" in text:

        return {
            "Category": "Rent Expense",
            "Debit": "Rent Expense Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # UTILITIES
    # ------------------------------------------------

    elif any(word in text for word in [
        "electricity", "water", "internet", "telephone", "utility"
    ]):

        return {
            "Category": "Utility Expense",
            "Debit": "Utility Expense Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # OFFICE EXPENSE
    # ------------------------------------------------

    elif any(word in text for word in [
        "stationery", "office supplies", "paper", "printer"
    ]):

        return {
            "Category": "Office Expense",
            "Debit": "Office Expense Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # LOAN
    # ------------------------------------------------

    elif "loan" in text:

        return {
            "Category": "Loan Transaction",
            "Debit": "Bank Account",
            "Credit": "Loan Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # CAPITAL
    # ------------------------------------------------

    elif "capital" in text:

        return {
            "Category": "Capital Introduced",
            "Debit": payment_account,
            "Credit": "Capital Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # DRAWINGS
    # ------------------------------------------------

    elif "drawings" in text:

        return {
            "Category": "Drawings",
            "Debit": "Drawings Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # INTEREST
    # ------------------------------------------------

    elif "interest" in text:

        return {
            "Category": "Interest Expense",
            "Debit": "Interest Expense Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # GST
    # ------------------------------------------------

    elif "gst" in text or "vat" in text or "tax" in text:

        return {
            "Category": "GST Transaction",
            "Debit": "Relevant GST Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # ------------------------------------------------
    # DEFAULT
    # ------------------------------------------------

    else:

        return {
            "Category": "General Business Transaction",
            "Debit": "Relevant Debit Account",
            "Credit": "Relevant Credit Account",
            "Amount": amount
        }


# ------------------------------------------------
# EXTRA FEATURES ADDED
# ------------------------------------------------

# ------------------------------------------------
# BUTTON
# ------------------------------------------------

if st.button("Generate Entry"):

    result = generate_entry(transaction)

    st.subheader("AI Generated Journal Entry")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"Category: {result['Category']}")
        st.success(f"Debit: {result['Debit']}")

    with col2:
        st.warning(f"Credit: {result['Credit']}")
        st.error(f"Amount: {result['Amount']}")

    # ------------------------------------------------
    # JOURNAL ENTRY TABLE
    # ------------------------------------------------

    st.subheader("Journal Entry Format")

    journal_df = pd.DataFrame({
        "Particulars": [
            result["Debit"],
            result["Credit"]
        ],
        "Debit": [
            result["Amount"],
            ""
        ],
        "Credit": [
            "",
            result["Amount"]
        ]
    })

    st.table(journal_df)

    # ------------------------------------------------
    # SAVE TO EXCEL
    # ------------------------------------------------

    data = pd.DataFrame({

        "Date": [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ],

        "Transaction": [
            transaction
        ],

        "Category": [
            result["Category"]
        ],

        "Debit": [
            result["Debit"]
        ],

        "Credit": [
            result["Credit"]
        ],

        "Amount": [
            result["Amount"]
        ]
    })

    file = "transactions.xlsx"

    if os.path.exists(file):

        old = pd.read_excel(file)

        updated = pd.concat(
            [old, data],
            ignore_index=True
        )

        updated.to_excel(
            file,
            index=False
        )

    else:

        data.to_excel(
            file,
            index=False
        )

    st.success("Transaction Saved Successfully")

    # ------------------------------------------------
    # DASHBOARD
    # ------------------------------------------------

    st.subheader("Transaction Dashboard")

    df = pd.read_excel(file)

    st.dataframe(
        df,
        use_container_width=True
    )

    # ------------------------------------------------
    # METRICS
    # ------------------------------------------------

    st.subheader("Dashboard Metrics")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Transactions",
            len(df)
        )    
        
    with col2:
        inflow_categories = [
            "Sales Revenue",
            "Compound Sales Transaction",
            "Business Income",
            "Consulting Income",
            "Commission Income",
            "Capital Introduced",
            "Loan Transaction"
        ]

        df["Amount"] = pd.to_numeric(
            df["Amount"],
            errors="coerce"
        )

        inflow = df[
            df["Category"].isin(inflow_categories)
        ]["Amount"].sum()

        outflow = df[
            ~df["Category"].isin(inflow_categories)
        ]["Amount"].sum()

        net_balance = inflow - outflow

        st.metric(
            "Net Balance",
            net_balance
        )

    # ------------------------------------------------
    # CATEGORY ANALYSIS
    # ------------------------------------------------

    st.subheader("Transaction Category Analysis")

    category_count = df["Category"].value_counts()

    st.bar_chart(category_count)

    # ------------------------------------------------
    # DOWNLOAD EXCEL FILE
    # ------------------------------------------------

    st.subheader("Download Records")

    with open(file, "rb") as f:

        st.download_button(

            label="Download Excel File",

            data=f,

            file_name="transactions.xlsx",

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # ------------------------------------------------
    # FOOTER
    # ------------------------------------------------

    st.markdown("---")

    st.caption(
        "AI Accounting System | Automated Journal Entry Generator | Developed by SUHAS KINI"
    )