import customtkinter as ctk
from database import run_query
from datetime import datetime

# Colors
PRIMARY = "#004ac6"
SURFACE = "#f7f9fb"
SIDEBAR_BG = "#f2f4f6"
CARD_BG = "#ffffff"
TEXT_DARK = "#191c1e"
TEXT_GRAY = "#434655"
GREEN = "#006c49"
RED = "#ab0b1c"
DARK_BANNER = "#0f172a"

def create_dashboard(parent, user_id):
    """Create dashboard page"""
    
    # Get current month data
    expenses = run_query(
        """SELECT SUM(AMOUNT) as total, EXP_TYPE 
           FROM EXPENSES 
           WHERE USER_ID=:1 AND TRUNC(EXP_DATE, 'MM') = TRUNC(SYSDATE, 'MM')
           GROUP BY EXP_TYPE""",
        [user_id]
    )
    
    total_expenses = 0
    total_income = 0
    
    for exp in expenses:
        if exp['EXP_TYPE'] == 'Expense':
            total_expenses += float(exp['TOTAL'] or 0)
        else:
            total_income += float(exp['TOTAL'] or 0)
    
    # Get category summary
    categories = run_query(
        """SELECT c.CAT_NAME, c.ICON, c.COLOR, SUM(e.AMOUNT) as total
           FROM EXPENSES e
           JOIN CATEGORIES c ON e.CAT_ID = c.CAT_ID
           WHERE e.USER_ID=:1 AND e.EXP_TYPE='Expense' AND TRUNC(e.EXP_DATE, 'MM') = TRUNC(SYSDATE, 'MM')
           GROUP BY c.CAT_NAME, c.ICON, c.COLOR
           ORDER BY total DESC""",
        [user_id]
    )
    
    # Get recent transactions
    recent = run_query(
        """SELECT * FROM (
               SELECT e.DESCRIPTION, e.AMOUNT, e.EXP_DATE, e.EXP_TYPE, c.CAT_NAME, c.ICON
               FROM EXPENSES e
               JOIN CATEGORIES c ON e.CAT_ID = c.CAT_ID
               WHERE e.USER_ID=:1
               ORDER BY e.EXP_DATE DESC
           ) WHERE ROWNUM <= 5""",
        [user_id]
    )
    
    # Top summary cards
    summary_frame = ctk.CTkFrame(parent, fg_color=SURFACE)
    summary_frame.pack(padx=24, pady=(20, 0), fill="x")
    
    # Current balance frame (blue card)
    balance_card = ctk.CTkFrame(summary_frame, fg_color="#2563eb", corner_radius=12)
    balance_card.pack(side="left", fill="both", expand=True, padx=(0, 12))
    
    balance_label = ctk.CTkLabel(
        balance_card,
        text="CURRENT BALANCE",
        font=("Segoe UI", 10),
        text_color="#dbe7ff"
    )
    balance_label.pack(padx=20, pady=(12, 4), anchor="w")
    
    balance_amount = ctk.CTkLabel(
        balance_card,
        text=f"₹{total_income - total_expenses:,.2f}",
        font=("Segoe UI", 28, "bold"),
        text_color="white"
    )
    balance_amount.pack(padx=20, pady=(0, 12), anchor="w")
    
    # Monthly spent frame
    spent_card = ctk.CTkFrame(summary_frame, fg_color=CARD_BG, corner_radius=12)
    spent_card.pack(side="left", fill="both", expand=True, padx=(0, 12))
    
    spent_label = ctk.CTkLabel(
        spent_card,
        text="MONTHLY SPENT",
        font=("Segoe UI", 10),
        text_color=TEXT_GRAY
    )
    spent_label.pack(padx=20, pady=(12, 4), anchor="w")
    
    spent_amount = ctk.CTkLabel(
        spent_card,
        text=f"₹{total_expenses:,.2f}",
        font=("Segoe UI", 20, "bold"),
        text_color=TEXT_DARK
    )
    spent_amount.pack(padx=20, pady=(0, 12), anchor="w")
    

    
    # Two column layout
    content = ctk.CTkFrame(parent, fg_color=SURFACE)
    content.pack(padx=24, pady=20, fill="both", expand=True)
    content.grid_columnconfigure(0, weight=1)
    content.grid_columnconfigure(1, weight=1)
    
    # Left column: Category breakdown
    left_col = ctk.CTkFrame(content, fg_color=SURFACE)
    left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
    
    cat_title = ctk.CTkLabel(
        left_col,
        text="Category Breakdown",
        font=("Segoe UI", 14, "bold"),
        text_color=TEXT_DARK
    )
    cat_title.pack(padx=0, pady=(0, 12), anchor="w")
    
    cat_frame = ctk.CTkFrame(left_col, fg_color=CARD_BG, corner_radius=12)
    cat_frame.pack(fill="both", expand=True)
    
    if categories:
        for cat in categories:
            cat_item = ctk.CTkFrame(cat_frame, fg_color=CARD_BG)
            cat_item.pack(padx=16, pady=10, fill="x")
            
            icon_label = ctk.CTkLabel(
                cat_item,
                text=cat['ICON'],
                font=("Segoe UI", 14),
                width=40
            )
            icon_label.pack(side="left", padx=(0, 12))
            
            info_frame = ctk.CTkFrame(cat_item, fg_color=CARD_BG)
            info_frame.pack(side="left", fill="both", expand=True)
            
            cat_name = ctk.CTkLabel(
                info_frame,
                text=cat['CAT_NAME'],
                font=("Segoe UI", 12, "bold"),
                text_color=TEXT_DARK
            )
            cat_name.pack(anchor="w")
            
            cat_amount = ctk.CTkLabel(
                info_frame,
                text=f"₹{float(cat['TOTAL'] or 0):,.2f}",
                font=("Segoe UI", 11),
                text_color=TEXT_GRAY
            )
            cat_amount.pack(anchor="w")
    else:
        no_data = ctk.CTkLabel(
            cat_frame,
            text="No expense data yet",
            font=("Segoe UI", 12),
            text_color=TEXT_GRAY
        )
        no_data.pack(padx=16, pady=20)
    
    # Right column: Recent transactions
    right_col = ctk.CTkFrame(content, fg_color=SURFACE)
    right_col.grid(row=0, column=1, sticky="nsew")
    
    trans_title = ctk.CTkLabel(
        right_col,
        text="Recent Activity",
        font=("Segoe UI", 14, "bold"),
        text_color=TEXT_DARK
    )
    trans_title.pack(padx=0, pady=(0, 12), anchor="w")
    
    trans_frame = ctk.CTkFrame(right_col, fg_color=CARD_BG, corner_radius=12)
    trans_frame.pack(fill="both", expand=True)
    
    if recent:
        for trans in recent:
            trans_item = ctk.CTkFrame(trans_frame, fg_color=CARD_BG)
            trans_item.pack(padx=16, pady=10, fill="x")
            
            icon_label = ctk.CTkLabel(
                trans_item,
                text=trans['ICON'],
                font=("Segoe UI", 12),
                width=40
            )
            icon_label.pack(side="left", padx=(0, 12))
            
            info_frame = ctk.CTkFrame(trans_item, fg_color=CARD_BG)
            info_frame.pack(side="left", fill="both", expand=True)
            
            desc = ctk.CTkLabel(
                info_frame,
                text=(trans['DESCRIPTION'] or '')[:40],
                font=("Segoe UI", 11, "bold"),
                text_color=TEXT_DARK
            )
            desc.pack(anchor="w")
            
            date_text = ctk.CTkLabel(
                info_frame,
                text=f"{trans['CAT_NAME']} • {trans['EXP_DATE']}",
                font=("Segoe UI", 10),
                text_color=TEXT_GRAY
            )
            date_text.pack(anchor="w")
            
            amount_color = GREEN if trans['EXP_TYPE'] == 'Income' else TEXT_DARK
            amount_label = ctk.CTkLabel(
                trans_item,
                text=f"₹{float(trans['AMOUNT']):,.2f}",
                font=("Segoe UI", 11, "bold"),
                text_color=amount_color
            )
            amount_label.pack(side="right")
    else:
        no_data = ctk.CTkLabel(
            trans_frame,
            text="No transactions yet",
            font=("Segoe UI", 12),
            text_color=TEXT_GRAY
        )
        no_data.pack(padx=16, pady=20)
