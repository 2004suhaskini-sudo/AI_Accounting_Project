import streamlit as st
import pandas as pd
import os

st.title("AI Expense & Journal Entry Automation System")

transaction = st.text_input("Enter Accounting Transaction")

# AI Logic
def generate_entry(text):

    text = text.lower()

    if "salary" in text:
        return {
            "Category": "Salary Expense",
            "Debit": "Salary Account",
            "Credit": "Bank Account",
            "Amount": "50000"
        }

    elif "rent" in text:
        return {
            "Category": "Rent Expense",
            "Debit": "Rent Account",
            "Credit": "Bank Account",
            "Amount": "20000"
        }

    elif "electricity" in text:
        return {
            "Category": "Utility Expense",
            "Debit": "Electricity Expense Account",
            "Credit": "Bank Account",
            "Amount": "8000"
        }

    elif "furniture" in text:
        return {
            "Category": "Asset Purchase",
            "Debit": "Furniture Account",
            "Credit": "Cash Account",
            "Amount": "25000"
        }

    else:
        return {
            "Category": "General Expense",
            "Debit": "Expense Account",
            "Credit": "Cash/Bank Account",
            "Amount": "Unknown"
        }

# Button
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