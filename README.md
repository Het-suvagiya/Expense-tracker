# 💰 ExpenseDesk - Personal Expense Manager

A modern, professional Python-based expense tracking application with a beautiful GUI built using CustomTkinter and Oracle 11g XE database.

## 📋 Features

- **Dashboard** - Overview of balance, spending, and recent transactions
- **Expenses Management** - Add, view, edit, and delete expenses
- **Categories** - Organize expenses by category with customizable icons and colors
- **Reports** - Detailed spending analysis and performance insights
- **Budget Tracking** - Set and monitor budgets for different categories
- **Charts & Visualizations** - Visual breakdown of spending patterns
- **Authentication** - Secure login system with user management

## 🛠️ System Requirements

- **Python** 3.8 or higher
- **Oracle Database 11g XE** (configured and running)
- **Operating System** - Windows, macOS, or Linux

## 📦 Installation

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

**Key Dependencies:**
- `customtkinter` - Modern GUI framework
- `cx_Oracle` - Oracle database connection
- `CTkMessagebox` - Message dialogs

### 2. Setup Oracle Database

Make sure Oracle 11g XE is installed and running on your system.

Update database credentials in `database.py`:
```python
ORACLE_HOST = "localhost"      # Your Oracle host
ORACLE_PORT = 1521            # Oracle port
ORACLE_SID = "xe"             # Your Oracle SID
ORACLE_USER = "system"        # Oracle username
ORACLE_PASSWORD = "admin"     # Oracle password
```

### 3. Initialize Database

Run the database setup script (execute once):

```bash
python create_tables.py
```

This will create all necessary tables and insert sample data:
- Users table with default admin account
- Categories with common expense types
- Budget and Expenses tables

## 🚀 Running the Application

Start the application from the root directory:

```bash
python main.py
```

Or directly from login:
```bash
python login.py
```

## 🔐 Default Login Credentials

- **Username:** `admin`
- **Password:** `admin123`

## 📁 Project Structure

```
ExpenseDesk/
├── main.py                 # Application entry point
├── login.py               # Login screen
├── app.py                 # Main window with sidebar
├── database.py            # Database connection functions
├── create_tables.py       # Database initialization script
├── dashboard.py           # Dashboard page
├── expenses.py            # Expenses management
├── categories.py          # Categories management
├── reports.py             # Reports and analysis
├── budget.py              # Budget management
├── charts.py              # Charts and visualizations
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎨 Design System

The application follows "The Precision Ledger" design system with:

- **Colors:**
  - Primary: #004ac6 (Blue)
  - Surface: #f7f9fb (Light gray)
  - Card: #ffffff (White)
  - Text Dark: #191c1e (Near black)
  - Text Gray: #434655 (Gray)
  - Green: #006c49 (Income/Health)
  - Red: #ab0b1c (Expense/Warning)

- **Typography:**
  - Headings: Segoe UI Bold (14-18pt)
  - Body: Segoe UI Regular (10-12pt)
  - Monospace: For numerical values

- **Components:**
  - Rounded corners (8-12px) for modern look
  - No visible borders - using tonal shifts instead
  - Smooth transitions and hover effects

## 📊 Database Schema

### USERS Table
- USER_ID (Primary Key)
- USERNAME
- PASSWORD
- FULL_NAME

### CATEGORIES Table
- CAT_ID (Primary Key)
- CAT_NAME
- ICON
- COLOR
- DESCRIPTION

### EXPENSES Table
- EXP_ID (Primary Key)
- USER_ID (Foreign Key)
- CAT_ID (Foreign Key)
- AMOUNT
- EXP_DATE
- DESCRIPTION
- EXP_TYPE (Expense/Income)
- STATUS (Completed/Pending)

### BUDGETS Table
- BUDGET_ID (Primary Key)
- USER_ID (Foreign Key)
- CAT_ID (Foreign Key)
- BUDGET_AMOUNT
- MONTH_YEAR

## 🚧 Current Features

✅ User authentication
✅ Dashboard with summary cards
✅ Expense tracking and management
✅ Category management
✅ Reports and analysis
✅ Budget allocation
✅ Charts and visualizations
✅ Responsive UI design

## 📝 Usage Guide

### Adding an Expense
1. Go to "Expenses" page
2. Click "+ Add New Expense"
3. Select category, enter amount and description
4. Choose type (Expense or Income)
5. Click Save

### Creating a Budget
1. Go to "Budget" page
2. Set budget amounts for each category
3. Monitor your spending vs. budget in real-time

### Viewing Reports
1. Go to "Reports" page
2. Select time period (Monthly, Quarterly, Annual)
3. View category distribution and spending insights

## 🔧 Troubleshooting

**Connection Error to Oracle:**
- Ensure Oracle 11g XE is running
- Check the database credentials in `database.py`
- Verify Oracle listener is active

**Module Import Errors:**
- Install all dependencies: `pip install -r requirements.txt`
- Ensure you're using Python 3.8+

**GUI Display Issues:**
- Try updating CustomTkinter: `pip install --upgrade customtkinter`

## 🤝 Contributing

Feel free to fork, modify, and enhance this project!

## 📄 License

This project is provided as-is for educational purposes.

## 👨‍💻 Developer Notes

- All page modules (dashboard, expenses, etc.) follow the same pattern for consistency
- Database queries use parameterized statements to prevent SQL injection
- The sidebar is fixed at 240px width for consistency
- All colors and styles are defined as constants for easy theme modification

## 📞 Support

For issues or questions, please refer to the inline code comments or create an issue.

---

**Built with ❤️ using Python, CustomTkinter, and Oracle Database**
