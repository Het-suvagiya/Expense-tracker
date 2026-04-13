<div align="center">

# 💰 ExpenseDesk
**Personal Finance & Expense Manager**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-brightgreen.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![Oracle 11g](https://img.shields.io/badge/Database-Oracle_11g-red.svg)](https://www.oracle.com/database/)

A modern, professional Python-based expense tracking application equipped with a visually stunning graphical user interface (GUI) built using **CustomTkinter** and powered by an **Oracle 11g XE** database.

</div>

---

## ✨ Key Features

- 📊 **Dynamic Dashboard** - Get a bird's-eye view of your current balance, monthly spending, and recent transactions.
- 💸 **Expense Tracking** - Add, view, edit, and safely delete your financial records.
- 📁 **Categories** - Organize your spending systematically.
- 📈 **Performance Reports** - Receive insights, summaries, and savings data.
- 📉 **Precision Charts** - Beautifully scaled, reactive bar charts mapping out your last 6 months of data.

---

## 🛠️ System Requirements

Before you begin, ensure you have the following installed:
- **Python** (version 3.8 or higher)
- **Oracle Database 11g XE** (installed, running, and accessible)

---

## 🚀 Installation & Setup Steps

Follow these exact steps to run the application securely on your local machine:

### 1. Install Dependencies
Open your terminal inside the project directory and install the required modules:
```bash
pip install -r requirements.txt
```
> *Dependencies include `customtkinter` for the UI, `cx_Oracle` for the database connection, and `CTkMessagebox` for native popups.*

### 2. Configure Your Database
Ensure that Oracle 11g XE is active. Open `database.py` and verify your credentials match your database server:
```python
ORACLE_HOST = "localhost"      
ORACLE_PORT = 1521            
ORACLE_SID = "xe"             
ORACLE_USER = "username"        # Your Oracle username
ORACLE_PASSWORD = "password"     # Your Oracle password
```

### 3. Initialize the Oracle Tables
Run the database bootstrapping script. You only need to do this **once** to build the architecture (Users, Categories, Expenses tables):
```bash
python create_tables.py
```
*If everything is configured correctly, your terminal will print out specific `✓ table created` messages.*

### 4. Launch the Application!
Start the front-end application by running the core python file:
```bash
python app.py
```

---

## 📁 Repository Structure

```text
ExpenseDesk/
├── app.py                 # Core application entry point and UI Shell
├── database.py            # Active Oracle connection handlers
├── create_tables.py       # Database architectural initialization
├── dashboard.py           # Home view rendering
├── expenses.py            # Expense list view and modifiers
├── categories.py          # Category definition views
├── reports.py             # Performance metric views 
├── charts.py              # Visual graphing views
├── requirements.txt       # Necessary Python modules
└── README.md              # Documentation
```

---

## 📊 Database Architecture

The system utilizes an enterprise-grade structure within Oracle 11g:

**`USERS` Table** 
> *Stores authenticated footprints.*
- `USER_ID`, `USERNAME`, `PASSWORD`, `FULL_NAME`

**`CATEGORIES` Table**
> *Stores dynamically colorful folder elements.*
- `CAT_ID`, `CAT_NAME`, `ICON`, `COLOR`, `DESCRIPTION`

**`EXPENSES` Table**
> *Maps transactions across dates to specific user origins.*
- `EXP_ID`, `USER_ID`, `CAT_ID`, `AMOUNT`, `EXP_DATE`, `DESCRIPTION`, `EXP_TYPE`, `STATUS`

---

## 🎨 Design Philosophy (`The Precision Ledger`)

The application embraces a minimalist and seamless layout:
- **Tonal Shifts:** Visually bypasses hard borders by using layered background transitions.
- **Fluid Layouts:** Removes rigid metric sizes, allowing components to dynamically scale across the native screen.
- **Micro-interactions:** Integrated hover effects tracking cursor movements across sidebar buttons and inputs.
- **Modern Typography:** Heavily utilizing scalable `Segoe UI`.

---

## 🔧 Troubleshooting

#### Cannot connect to Oracle (`ORA-12154` or Timeout)
- Open `Services.msc` (Windows) and ensure **OracleServiceXE** and **OracleXETNSListener** are running.
- Ensure your password is correct inside `database.py`.

#### Module Not Found (`ImportError`)
- Verify you are inside your virtual environment (if you are utilizing one) before installing requirements via `pip`.

#### Visual Bugs / Squished UI
- Make sure you are using the latest package release of `customtkinter`. `pip install --upgrade customtkinter`

---
<div align="center">
Built with ❤️ tracking finances intelligently 
</div>
