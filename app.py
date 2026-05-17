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
user_name = st.text_input("Enter Your Name")


# ------------------------------------------------
# EXTRACT AMOUNT
# ------------------------------------------------

def extract_amount(text):

    numbers = re.findall(r'\d[\d,]*(?:\.\d+)?', text)

    if numbers:
        return int(float(numbers[0].replace(",", "")))

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

        if "sale" in text or "sales" in text or "sold" in text:
            payment_account = "Debtor Account"

        else:
            payment_account = "Creditor Account"

    elif "bank" in text:

        payment_account = "Bank Account"

    elif "cash" in text:

        payment_account = "Cash Account"

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

    elif any(word in text for word in [
        "purchase return",
        "returned goods to supplier",
        "goods returned to supplier",
        "returned purchased goods"
    ]):

        return {
            "Category": "Purchase Return",
            "Debit": "Supplier Account",
            "Credit": "Purchase Return Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # SALES RETURNS
    # ------------------------------------------------

    elif any(word in text for word in [
        "sales return",
        "goods returned by customer",
        "customer returned goods",
        "goods returned by debtor"
    ]):

        return {
            "Category": "Sales Return",
            "Debit": "Sales Return Account",
            "Credit": "Customer Account",
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

        debit_account = [
            "Cash/Bank Account",
            "Debtor Account"
        ]

        return {
            "Category": "Compound Sales Transaction",
            "Debit": debit_account,
            "Credit": "Sales Account",
            "Amount": amount
        }

    # ------------------------------------------------
    # COMPOUND TRANSACTIONS
    # ------------------------------------------------

    elif (
        (
            "purchase" in text or
            "purchases" in text or
            "purchased" in text or
            "bought" in text
        )
        and
        (
            "partly cash" in text or
            "balance on credit" in text
        )
    ):

        # ------------------------------------------------
        # IDENTIFY ASSET ACCOUNT
        # ------------------------------------------------

        if any(word in text for word in [
            "machinery",
            "machine",
            "equipment",
            "plant"
        ]):

            debit_account = "Machinery Account"

        elif any(word in text for word in [
            "furniture",
            "table",
            "chair",
            "desk",
            "cabinet",
            "cupboard",
            "sofa"
        ]):

            debit_account = "Furniture Account"

        elif any(word in text for word in [
            "vehicle",
            "car",
            "truck",
            "van"
        ]):

            debit_account = "Vehicle Account"

        elif any(word in text for word in [
            "inventory",
            "stock",
            "goods",
            "raw material"
        ]):

            debit_account = "Inventory Account"

        else:

            debit_account = "Relevant Asset/Purchase Account"

        # ------------------------------------------------
        # EXTRACT TOTAL & CASH AMOUNT
        # ------------------------------------------------

        numbers = re.findall(
            r'\d[\d,]*(?:\.\d+)?',
            text
        )

        numbers = [
            int(num.replace(",", ""))
            for num in numbers
        ]

        total_amount = (
            numbers[0]
            if len(numbers) > 0
            else 0
        )

        cash_amount = (
            numbers[1]
            if len(numbers) > 1
            else 0
        )

        credit_amount = (
            total_amount - cash_amount
        )

        # ------------------------------------------------
        # RETURN ENTRY
        # ------------------------------------------------

        return {

            "Category": "Compound Purchase Transaction",

            "Debit": [
                {
                    "Account": debit_account,
                    "Amount": total_amount
                }
            ],

            "Credit": [
                {
                    "Account": "Cash/Bank Account",
                    "Amount": cash_amount
                },
                {
                    "Account": "Creditor Account",
                    "Amount": credit_amount
                }
            ],

            "Amount": total_amount
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
    # COMPOUND INCOME
    # ------------------------------------------------

    elif (
        "consulting" in text
        and "commission" in text
        and "interest" in text
    ):

        numbers = re.findall(
            r'\d[\d,]*(?:\.\d+)?',
            text
        )

        numbers = [
            int(num.replace(",", ""))
            for num in numbers
        ]

        consulting_amount = numbers[0]

        commission_amount = numbers[1]

        interest_amount = numbers[2]

        total_amount = (
            consulting_amount +
            commission_amount +
            interest_amount
        )

        return {

            "Category": "Compound Income Transaction",

            "Debit": [
                {
                    "Account": payment_account,
                    "Amount": total_amount
                }
            ],

            "Credit": [
                {
                    "Account": "Consulting Income Account",
                    "Amount": consulting_amount
                },
                {
                    "Account": "Commission Income Account",
                    "Amount": commission_amount
                },
                {
                    "Account": "Interest Income Account",
                    "Amount": interest_amount
                }
            ],

            "Amount": total_amount
        }
    
    # ------------------------------------------------
    # CONSULTING / COMMISSION / SERVICE INCOME
    # ------------------------------------------------

    elif "consulting" in text:

        if any(word in text for word in [
            "received",
            "receive",
            "got",
            "earned",
            "income",
            "received through"
        ]):

            return {
                "Category": "Consulting Income",
                "Debit": payment_account,
                "Credit": "Consulting Income Account",
                "Amount": amount
            }

        else:

            return {
                "Category": "Consulting Expense",
                "Debit": "Consulting Expense Account",
                "Credit": payment_account,
                "Amount": amount
            }

    elif "commission" in text:

        if any(word in text for word in [
            "received",
            "receive",
            "got",
            "earned",
            "income",
            "received through"
        ]):

            return {
                "Category": "Commission Income",
                "Debit": payment_account,
                "Credit": "Commission Income Account",
                "Amount": amount
            }

        else:

            return {
                "Category": "Commission Expense",
                "Debit": "Commission Expense Account",
                "Credit": payment_account,
                "Amount": amount
            }

    elif "income" in text or "revenue" in text:

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

        if "sold" in text or "sale" in text:

            return {
                "Category": "Furniture Sale",
                "Debit": payment_account,
                "Credit": "Furniture Account",
                "Amount": amount
            }

        else:

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

        if "sold" in text or "sale" in text:

            return {
                "Category": "Machinery Sale",
                "Debit": payment_account,
                "Credit": "Machinery Account",
                "Amount": amount
            }

        else:

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

        if "sold" in text or "sale" in text:

            return {
                "Category": "Vehicle Sale",
                "Debit": payment_account,
                "Credit": "Vehicle Account",
                "Amount": amount
            }

        else:

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

        if (
            "purchase" in text or
            "purchased" in text or
            "bought" in text
        ):

            return {
                "Category": "Inventory Purchase",
                "Debit": "Inventory Account",
                "Credit": payment_account,
                "Amount": amount
            }

        elif (
            "sale" in text or
            "sales" in text or
            "sold" in text
        ):

            return {
                "Category": "Sales Revenue",
                "Debit": payment_account,
                "Credit": "Sales Account",
                "Amount": amount
            }
        
    # ------------------------------------------------
    # PURCHASES
    # ------------------------------------------------

    elif any(word in text for word in [
            "purchase",
            "purchases",
            "purchased",
            "bought"
    ]):

        return {
            "Category": "Purchase Transaction",
            "Debit": "Purchase Account",
            "Credit": payment_account,
            "Amount": amount
        }
    
    # ------------------------------------------------
    # COMPOUND EXPENSES
    # ------------------------------------------------

    elif (
        "salary" in text
        and ("electricity" in text or "utility" in text)
        and "rent" in text
    ):

        numbers = re.findall(
            r'\d[\d,]*(?:\.\d+)?',
            text
        )

        numbers = [
            int(num.replace(",", ""))
            for num in numbers
        ]

        salary_amount = numbers[0]

        utility_amount = numbers[1]

        rent_amount = numbers[2]

        total_amount = (
            salary_amount +
            utility_amount +
            rent_amount
        )

        return {

            "Category": "Compound Expense Transaction",

            "Debit": [
                {
                    "Account": "Salary Expense Account",
                    "Amount": salary_amount
                },
                {
                    "Account": "Utility Expense Account",
                    "Amount": utility_amount
                },
                {
                    "Account": "Rent Expense Account",
                    "Amount": rent_amount
                }
            ],

            "Credit": [
                {
                    "Account": payment_account,
                    "Amount": total_amount
                }
            ],

            "Amount": total_amount
        }
    
    # ------------------------------------------------
    # SALARY
    # ------------------------------------------------

    elif "salary" in text or "wages" in text:

        if any(word in text for word in [
            "received",
            "receive",
            "received from",
            "got"
        ]):

            return {
                "Category": "Salary Income",
                "Debit": payment_account,
                "Credit": "Salary Income Account",
                "Amount": amount
            }

        else:

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

        if any(word in text for word in [
            "received",
            "receive",
            "got",
            "earned",
            "income"
        ]):

            return {
                "Category": "Rent Income",
                "Debit": payment_account,
                "Credit": "Rent Income Account",
                "Amount": amount
            }

        else:

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
    # CAPITAL
    # ------------------------------------------------

    elif "capital" in text:

        if any(word in text for word in [
            "withdraw",
            "withdrawn",
            "returned",
            "paid back"
        ]):

            return {
                "Category": "Drawings",
                "Debit": "Drawings Account",
                "Credit": payment_account,
                "Amount": amount
            }

        else:

            return {
                "Category": "Capital Introduced",
                "Debit": payment_account,
                "Credit": "Capital Account",
                "Amount": amount
            }

    # ------------------------------------------------
    # DRAWINGS
    # ------------------------------------------------

    elif any(word in text for word in [
        "drawings",
        "withdrew",
        "withdrawn for personal use",
        "personal use",
        "owner withdrew",
        "proprietor withdrew"
    ]):

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

        if any(word in text for word in [
            "received",
            "receive",
            "got",
            "earned",
            "income"
        ]):

            return {
                "Category": "Interest Income",
                "Debit": payment_account,
                "Credit": "Interest Income Account",
                "Amount": amount
            }

        else:

            return {
                "Category": "Interest Expense",
                "Debit": "Interest Expense Account",
                "Credit": payment_account,
                "Amount": amount
            }

    # ------------------------------------------------
    # GST / TAX
    # ------------------------------------------------

    elif "gst" in text or "vat" in text or "tax" in text:

        if any(word in text for word in [
            "received",
            "refund",
            "input gst",
            "input vat"
        ]):

            return {
                "Category": "GST Receivable",
                "Debit": "GST Receivable Account",
                "Credit": payment_account,
                "Amount": amount
            }

        else:

            return {
                "Category": "GST Payable",
                "Debit": "Tax Expense Account",
                "Credit": "GST Payable Account",
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

    debit_display = result["Debit"]
    credit_display = result["Credit"]

    if isinstance(debit_display, list):

        debit_display = ", ".join(
            [
                f"{acc['Account']} ({acc['Amount']})"
                if isinstance(acc, dict)
                else str(acc)

                for acc in debit_display
            ]
        )

    if isinstance(credit_display, list):

        credit_display = ", ".join(
            [
                f"{acc['Account']} ({acc['Amount']})"
                if isinstance(acc, dict)
                else str(acc)

                for acc in credit_display
            ]
        )

    with col1:

        st.info(f"Category: {result['Category']}")

        st.success(f"Debit: {debit_display}")

    with col2:

        st.warning(f"Credit: {credit_display}")

        st.error(f"Amount: {result['Amount']}")

    # ------------------------------------------------
    # JOURNAL ENTRY TABLE
    # ------------------------------------------------

    st.subheader("Journal Entry Format")

    debit_accounts = result["Debit"]
    credit_accounts = result["Credit"]

    if not isinstance(debit_accounts, list):
        debit_accounts = [debit_accounts]

    if not isinstance(credit_accounts, list):
        credit_accounts = [credit_accounts]

    particulars = []
    debit_column = []
    credit_column = []

    # ------------------------------------------------
    # DEBIT ENTRIES
    # ------------------------------------------------

    for acc in debit_accounts:

        if isinstance(acc, dict):

            particulars.append(acc["Account"])

            debit_column.append(acc["Amount"])

            credit_column.append("")

        else:

            particulars.append(acc)

            debit_column.append(result["Amount"])

            credit_column.append("")

    # ------------------------------------------------
    # CREDIT ENTRIES
    # ------------------------------------------------

    for acc in credit_accounts:

        if isinstance(acc, dict):

            particulars.append(acc["Account"])

            debit_column.append("")

            credit_column.append(acc["Amount"])

        else:

            particulars.append(acc)

            debit_column.append("")

            credit_column.append(result["Amount"])

    # ------------------------------------------------
    # CREATE DATAFRAME
    # ------------------------------------------------

    journal_df = pd.DataFrame({

        "Particulars": particulars,
        "Debit": debit_column,
        "Credit": credit_column

    })

    st.dataframe(
        journal_df,
        use_container_width=True
    )

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

            ", ".join(

                [
                    acc["Account"]
                    if isinstance(acc, dict)
                    else str(acc)

                    for acc in result["Debit"]
                ]

            )

            if isinstance(result["Debit"], list)

            else result["Debit"]

        ],

        "Credit": [

            ", ".join(

                [
                    acc["Account"]
                    if isinstance(acc, dict)
                    else str(acc)

                    for acc in result["Credit"]
                ]

            )

            if isinstance(result["Credit"], list)

            else result["Credit"]

        ],

        "Amount": [
            result["Amount"]
        ]

    })

    # ------------------------------------------------
    # UNIQUE FILE FOR EACH USER
    # ------------------------------------------------

    safe_user = user_name.strip().replace(" ", "_")

    file = f"transactions_{safe_user}.xlsx"

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

    def color_amount(row):

        inflow_keywords = [
            "income",
            "sales revenue",
            "compound sales transaction",
            "capital introduced",
            "capital contribution",
            "commission",
            "consulting",
            "received",
            "profit",
            "discount received",
            "purchase return",
            "gst receivable"
        ]

        category = str(row["Category"]).lower()

        if any(word in category for word in inflow_keywords):

            color = "lightgreen"

        else:

            color = "red"

        styles = [""] * len(row)

        amount_index = row.index.get_loc("Amount")

        styles[amount_index] = (
            f"color: {color}; font-weight: bold"
        )

        return styles

    styled_df = df.style.apply(
        color_amount,
        axis=1
    )

    st.dataframe(
        styled_df,
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

        inflow_keywords = [
            "income",
            "sales revenue",
            "compound sales transaction",
            "capital introduced",
            "capital contribution",
            "commission",
            "consulting",
            "received",
            "profit",
            "discount received",
            "purchase return",
            "gst receivable"
        ]

        df["Amount"] = pd.to_numeric(
            df["Amount"],
            errors="coerce"
        )

        inflow = df[
            df["Category"].str.lower().apply(
                lambda x: any(
                    word in x
                    for word in inflow_keywords
                )
            )
        ]["Amount"].sum()

        outflow = df[
            ~df["Category"].str.lower().apply(
                lambda x: any(
                    word in x
                    for word in inflow_keywords
                )
            )
        ]["Amount"].sum()

        net_balance = inflow - outflow

        st.metric(
            "Net Balance",
            net_balance
        )

    # ------------------------------------------------
    # CATEGORY ANALYSIS
    # ------------------------------------------------

    st.subheader("Advanced Transaction Analysis")

    # Category-wise Total Amount

    category_amount = df.groupby(
        "Category"
    )["Amount"].sum()

    st.write("Category-wise Transaction Amount")

    st.bar_chart(category_amount)

    # Top 5 Categories

    st.write("Top 5 Transaction Categories")

    top_categories = category_amount.sort_values(
        ascending=False
    ).head(5)

    st.bar_chart(top_categories)

    # Income vs Expense

    inflow_keywords = [
        "income",
        "sales revenue",
        "compound sales transaction",
        "capital introduced",
        "capital contribution",
        "commission",
        "consulting",
        "received",
        "profit",
        "discount received",
        "purchase return",
        "gst receivable"
    ]

    income_total = df[
        df["Category"].str.lower().apply(
            lambda x: any(
                word in x
                for word in inflow_keywords
            )
        )
    ]["Amount"].sum()

    expense_total = df[
        ~df["Category"].str.lower().apply(
            lambda x: any(
                word in x
                for word in inflow_keywords
            )
        )
    ]["Amount"].sum()

    comparison_df = pd.DataFrame({
        "Type": ["Income", "Expense"],
        "Amount": [income_total, expense_total]
    })

    st.write("Income vs Expense Analysis")

    st.bar_chart(
        comparison_df.set_index("Type")
    )

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