import streamlit as st
import pandas as pd
import os
import re

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Accounting System",
    layout="wide"
)

st.title("AI-Based Financial Transaction Analysis & Automated Journal Entry System")

transaction = st.text_input("Enter Accounting Transaction")


# -----------------------------------
# AMOUNT EXTRACTION
# -----------------------------------

def extract_amount(text):

    numbers = re.findall(r'\d+', text)

    if numbers:
        return numbers[0]

    return "Unknown"


# -----------------------------------
# KEYWORD DATABASE
# -----------------------------------

income_keywords = [
    "income", "revenue", "earned", "received",
    "consulting", "commission", "service",
    "fees"
]

sales_keywords = [
    "sale", "sales", "sold"
]

salary_keywords = [
    "salary", "wages", "payroll", "employee payment"
]

rent_keywords = [
    "rent", "lease", "office rent", "building rent"
]

utility_keywords = [
    "electricity", "internet", "water",
    "wifi", "telephone", "utility"
]

furniture_keywords = [
    "furniture", "table", "chair",
    "desk", "sofa", "cabinet",
    "cupboard"
]

machinery_keywords = [
    "machinery", "machine", "equipment",
    "plant", "factory equipment"
]

inventory_keywords = [
    "inventory", "stock", "goods",
    "raw material", "product inventory"
]

office_keywords = [
    "office supplies", "stationery",
    "printer ink", "paper", "supplies"
]

vehicle_keywords = [
    "vehicle", "car", "truck",
    "van", "transport vehicle"
]

loan_keywords = [
    "loan", "bank loan", "borrowing"
]

capital_keywords = [
    "capital", "owner investment",
    "capital introduced"
]

drawings_keywords = [
    "drawings", "owner withdrawal"
]

depreciation_keywords = [
    "depreciation", "asset depreciation"
]

interest_keywords = [
    "interest", "finance cost"
]

gst_keywords = [
    "gst", "tax", "vat"
]


# -----------------------------------
# AI ACCOUNTING ENGINE
# -----------------------------------

def generate_entry(text):

    text = text.lower()

    amount = extract_amount(text)

    # -----------------------------------
    # PAYMENT MODE
    # -----------------------------------

    if "credit" in text:

        payment_account = "Creditor Account"

    elif "bank" in text:

        payment_account = "Bank Account"

    elif "cash" in text:

        payment_account = "Cash Account"

    else:

        payment_account = "Cash/Bank Account"

    # -----------------------------------
    # SALES REVENUE
    # IMPORTANT: ABOVE INVENTORY
    # -----------------------------------

    if any(word in text for word in sales_keywords):

        if "credit" in text:

            debit_account = "Debtor Account"

        elif "bank" in text:

            debit_account = "Bank Account"

        elif "cash" in text:

            debit_account = "Cash Account"

        else:

            debit_account = "Cash/Bank Account"

        return {
            "Category": "Sales Revenue",
            "Debit": debit_account,
            "Credit": "Sales Account",
            "Amount": amount
        }

    # -----------------------------------
    # CONSULTING / SERVICE INCOME
    # -----------------------------------

    elif any(word in text for word in income_keywords):

        if "consulting" in text:

            income_account = "Consulting Income Account"

        elif "commission" in text:

            income_account = "Commission Income Account"

        else:

            income_account = "Income Account"

        return {
            "Category": "Business Income",
            "Debit": payment_account,
            "Credit": income_account,
            "Amount": amount
        }

    # -----------------------------------
    # FURNITURE PURCHASE
    # -----------------------------------

    elif any(word in text for word in furniture_keywords):

        return {
            "Category": "Furniture Purchase",
            "Debit": "Furniture Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # -----------------------------------
    # MACHINERY PURCHASE
    # -----------------------------------

    elif any(word in text for word in machinery_keywords):

        return {
            "Category": "Machinery Purchase",
            "Debit": "Machinery Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # -----------------------------------
    # VEHICLE PURCHASE
    # -----------------------------------

    elif any(word in text for word in vehicle_keywords):

        return {
            "Category": "Vehicle Purchase",
            "Debit": "Vehicle Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # -----------------------------------
    # INVENTORY PURCHASE
    # -----------------------------------

    elif any(word in text for word in inventory_keywords):

        return {
            "Category": "Inventory Purchase",
            "Debit": "Inventory Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # -----------------------------------
    # SALARY EXPENSE
    # -----------------------------------

    elif any(word in text for word in salary_keywords):

        return {
            "Category": "Salary Expense",
            "Debit": "Salary Expense Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # -----------------------------------
    # RENT EXPENSE
    # -----------------------------------

    elif any(word in text for word in rent_keywords):

        return {
            "Category": "Rent Expense",
            "Debit": "Rent Expense Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # -----------------------------------
    # UTILITY EXPENSE
    # -----------------------------------

    elif any(word in text for word in utility_keywords):

        return {
            "Category": "Utility Expense",
            "Debit": "Utility Expense Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # -----------------------------------
    # OFFICE EXPENSE
    # -----------------------------------

    elif any(word in text for word in office_keywords):

        return {
            "Category": "Office Expense",
            "Debit": "Office Expense Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # -----------------------------------
    # LOAN
    # -----------------------------------

    elif any(word in text for word in loan_keywords):

        return {
            "Category": "Loan Transaction",
            "Debit": "Bank Account",
            "Credit": "Loan Account",
            "Amount": amount
        }

    # -----------------------------------
    # CAPITAL
    # -----------------------------------

    elif any(word in text for word in capital_keywords):

        return {
            "Category": "Capital Introduced",
            "Debit": payment_account,
            "Credit": "Capital Account",
            "Amount": amount
        }

    # -----------------------------------
    # DRAWINGS
    # -----------------------------------

    elif any(word in text for word in drawings_keywords):

        return {
            "Category": "Drawings",
            "Debit": "Drawings Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # -----------------------------------
    # DEPRECIATION
    # -----------------------------------

    elif any(word in text for word in depreciation_keywords):

        return {
            "Category": "Depreciation Expense",
            "Debit": "Depreciation Expense Account",
            "Credit": "Accumulated Depreciation Account",
            "Amount": amount
        }

    # -----------------------------------
    # INTEREST
    # -----------------------------------

    elif any(word in text for word in interest_keywords):

        return {
            "Category": "Interest Expense",
            "Debit": "Interest Expense Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # -----------------------------------
    # GST
    # -----------------------------------

    elif any(word in text for word in gst_keywords):

        return {
            "Category": "GST Transaction",
            "Debit": "Relevant GST Account",
            "Credit": payment_account,
            "Amount": amount
        }

    # -----------------------------------
    # DEFAULT
    # -----------------------------------

    else:

        return {
            "Category": "General Business Transaction",
            "Debit": "Relevant Debit Account",
            "Credit": "Relevant Credit Account",
            "Amount": amount
        }


# -----------------------------------
# BUTTON
# -----------------------------------

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

    # -----------------------------------
    # SAVE TO EXCEL
    # -----------------------------------

    data = pd.DataFrame({

        "Transaction": [transaction],

        "Category": [result["Category"]],

        "Debit": [result["Debit"]],

        "Credit": [result["Credit"]],

        "Amount": [result["Amount"]]
    })

    file = "transactions.xlsx"

    if os.path.exists(file):

        old = pd.read_excel(file)

        updated = pd.concat([old, data], ignore_index=True)

        updated.to_excel(file, index=False)

    else:

        data.to_excel(file, index=False)

    st.success("Transaction Saved Successfully")

    # -----------------------------------
    # DASHBOARD
    # -----------------------------------

    st.subheader("Transaction Dashboard")

    df = pd.read_excel(file)

    st.dataframe(df, use_container_width=True)

    st.metric("Total Transactions", len(df))