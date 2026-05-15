import streamlit as st
import pandas as pd
import os
import re

st.title("AI Expense & Journal Entry Automation System")

transaction = st.text_input("Enter Accounting Transaction")


# Extract Amount Automatically
def extract_amount(text):

    numbers = re.findall(r'\d+', text)

    if numbers:
        return numbers[0]
    else:
        return "Unknown"


# AI Accounting Logic
def generate_entry(text):

    text = text.lower()

    amount = extract_amount(text)

    # INCOME
    if any(word in text for word in ["income", "received", "revenue", "earned", "service"]):

        return {
            "Category": "Income",
            "Debit": "Cash/Bank Account",
            "Credit": "Income Account",
            "Amount": amount
        }

    # SALARY
    elif "salary" in text:

        return {
            "Category": "Salary Expense",
            "Debit": "Salary Expense Account",
            "Credit": "Cash/Bank Account",
            "Amount": amount
        }

    # RENT
    elif "rent" in text:

        return {
            "Category": "Rent Expense",
            "Debit": "Rent Expense Account",
            "Credit": "Cash/Bank Account",
            "Amount": amount
        }

    # ELECTRICITY / UTILITIES
    elif any(word in text for word in ["electricity", "utility", "water", "internet"]):

        return {
            "Category": "Utility Expense",
            "Debit": "Utility Expense Account",
            "Credit": "Cash/Bank Account",
            "Amount": amount
        }

    # FURNITURE
    elif "furniture" in text:

        return {
            "Category": "Furniture Purchase",
            "Debit": "Furniture Account",
            "Credit": "Cash/Bank Account",
            "Amount": amount
        }

    # MACHINERY
    elif "machinery" in text:

        return {
            "Category": "Machinery Purchase",
            "Debit": "Machinery Account",
            "Credit": "Cash/Creditor Account",
            "Amount": amount
        }

    # INVENTORY / STOCK
    elif any(word in text for word in ["inventory", "stock", "goods"]):

        return {
            "Category": "Inventory Purchase",
            "Debit": "Inventory Account",
            "Credit": "Cash/Creditor Account",
            "Amount": amount
        }

    # OFFICE EXPENSE
    elif any(word in text for word in ["office", "stationery", "supplies"]):

        return {
            "Category": "Office Expense",
            "Debit": "Office Expense Account",
            "Credit": "Cash/Bank Account",
            "Amount": amount
        }

    # SALES
    elif any(word in text for word in ["sold", "sales"]):

        return {
            "Category": "Sales Revenue",
            "Debit": "Cash/Bank Account",
            "Credit": "Sales Account",
            "Amount": amount
        }

    # LOAN
    elif "loan" in text:

        return {
            "Category": "Loan Transaction",
            "Debit": "Cash/Bank Account",
            "Credit": "Loan Account",
            "Amount": amount
        }

    # COMMISSION
    elif "commission" in text:

        return {
            "Category": "Commission Income",
            "Debit": "Cash/Bank Account",
            "Credit": "Commission Income Account",
            "Amount": amount
        }

    # DEFAULT
    else:

        return {
            "Category": "General Expense",
            "Debit": "Expense Account",
            "Credit": "Cash/Bank Account",
            "Amount": amount
        }


# BUTTON
if st.button("Generate Entry"):

    result = generate_entry(transaction)

    st.subheader("AI Generated Journal Entry")

    st.write("Category:", result["Category"])
    st.write("Debit:", result["Debit"])
    st.write("Credit:", result["Credit"])
    st.write("Amount:", result["Amount"])

    # Save to Excel
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

        new = pd.concat([old, data], ignore_index=True)

        new.to_excel(file, index=False)

    else:

        data.to_excel(file, index=False)

    st.success("Saved Successfully")

    st.subheader("Transaction Dashboard")

    st.dataframe(pd.read_excel(file))