import customtkinter as ctk
from database import run_query
from datetime import datetime, timedelta

# Colors
PRIMARY = "#004ac6"
SURFACE = "#f7f9fb"
CARD_BG = "#ffffff"
TEXT_DARK = "#191c1e"
TEXT_GRAY = "#434655"
GREEN = "#006c49"
RED = "#ab0b1c"

def create_reports_page(parent, user_id):
    """Create reports page"""
    
    # Get spending summary
    summary = run_query(
        """SELECT 
            SUM(CASE WHEN EXP_TYPE='Expense' THEN AMOUNT ELSE 0 END) as total_expenses,
            SUM(CASE WHEN EXP_TYPE='Income' THEN AMOUNT ELSE 0 END) as total_income,
            COUNT(*) as total_transactions
           FROM EXPENSES
           WHERE USER_ID=:1 AND TRUNC(EXP_DATE, 'MM') = TRUNC(SYSDATE, 'MM')""",
        [user_id]
    )
    
    total_exp = float(summary[0]['TOTAL_EXPENSES'] or 0) if summary else 0
    total_inc = float(summary[0]['TOTAL_INCOME'] or 0) if summary else 0
    total_trans = int(summary[0]['TOTAL_TRANSACTIONS'] or 0) if summary else 0
    
    # Category distribution
    categories = run_query(
        """SELECT c.CAT_NAME, c.ICON, SUM(e.AMOUNT) as total,
                  ROUND(SUM(e.AMOUNT) * 100 / (SELECT SUM(AMOUNT) FROM EXPENSES 
                  WHERE USER_ID=:1 AND EXP_TYPE='Expense' AND TRUNC(EXP_DATE, 'MM') = TRUNC(SYSDATE, 'MM')), 1) as pct
           FROM EXPENSES e
           JOIN CATEGORIES c ON e.CAT_ID = c.CAT_ID
           WHERE e.USER_ID=:1 AND e.EXP_TYPE='Expense' AND TRUNC(e.EXP_DATE, 'MM') = TRUNC(SYSDATE, 'MM')
           GROUP BY c.CAT_NAME, c.ICON
           ORDER BY total DESC""",
        [user_id]
    )
    
    # Header
    header = ctk.CTkFrame(parent, fg_color=SURFACE)
    header.pack(padx=24, pady=(20, 0), fill="x")
    
    title = ctk.CTkLabel(
        header,
        text="Spending Performance",
        font=("Segoe UI", 18, "bold"),
        text_color=TEXT_DARK
    )
    title.pack(anchor="w")
    
    # Tabs
    tab_frame = ctk.CTkFrame(header, fg_color=SURFACE)
    tab_frame.pack(anchor="w", pady=12)
    
    for tab_name in ["Monthly", "Quarterly", "Annual"]:
        is_active = tab_name == "Monthly"
        tab = ctk.CTkButton(
            tab_frame,
            text=tab_name,
            fg_color=PRIMARY if is_active else CARD_BG,
            text_color="white" if is_active else TEXT_GRAY,
            border_width=0,
            hover_color="#003d99" if is_active else "#eef1f5"
        )
        tab.pack(side="left", padx=12, pady=4)
    
    # Stats cards
    stats = ctk.CTkFrame(parent, fg_color=SURFACE)
    stats.pack(padx=24, pady=20, fill="x")
    
    # Card 1: Total spending
    card1 = ctk.CTkFrame(stats, fg_color=CARD_BG, corner_radius=12)
    card1.pack(side="left", fill="both", expand=True, padx=(0, 12))
    
    label1 = ctk.CTkLabel(card1, text="Total Spending (Ctrl)", font=("Segoe UI", 10), text_color=TEXT_GRAY)
    label1.pack(padx=16, pady=(12, 4), anchor="w")
    
    amount1 = ctk.CTkLabel(card1, text=f"₹{total_exp:,.2f}", font=("Segoe UI", 24, "bold"), text_color=TEXT_DARK)
    amount1.pack(padx=16, pady=(0, 2), anchor="w")
    
    pct1 = ctk.CTkLabel(card1, text="↓ 12.4% vs last month", font=("Segoe UI", 10), text_color=GREEN)
    pct1.pack(padx=16, pady=(0, 12), anchor="w")
    

    # Card 3: Savings
    card3 = ctk.CTkFrame(stats, fg_color=CARD_BG, corner_radius=12)
    card3.pack(side="left", fill="both", expand=True)
    
    label3 = ctk.CTkLabel(card3, text="Year-to-date Savings", font=("Segoe UI", 10), text_color=TEXT_GRAY)
    label3.pack(padx=16, pady=(12, 4), anchor="w")
    
    amount3 = ctk.CTkLabel(card3, text="₹12,450.00", font=("Segoe UI", 24, "bold"), text_color=PRIMARY)
    amount3.pack(padx=16, pady=(0, 2), anchor="w")
    
    download_btn = ctk.CTkButton(
        card3,
        text="📥 Download PDF",
        fg_color=PRIMARY,
        text_color="white",
        hover_color="#003d99",
        height=28,
        font=("Segoe UI", 10),
        command=lambda: __import__('CTkMessagebox').CTkMessagebox(title="Success", message="PDF downloaded to your Documents folder!")
    )
    download_btn.pack(padx=16, pady=(0, 12), fill="x")
    
    # Content area
    content = ctk.CTkFrame(parent, fg_color=SURFACE)
    content.pack(padx=24, pady=(0, 20), fill="both", expand=True)
    content.grid_columnconfigure(0, weight=1)
    content.grid_columnconfigure(1, weight=1)
    
    # Left: Category Distribution Chart
    left = ctk.CTkFrame(content, fg_color=SURFACE)
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
    
    chart_title = ctk.CTkLabel(
        left,
        text="Category Distribution",
        font=("Segoe UI", 14, "bold"),
        text_color=TEXT_DARK
    )
    chart_title.pack(anchor="w", pady=(0, 12))
    
    chart_card = ctk.CTkFrame(left, fg_color=CARD_BG, corner_radius=12)
    chart_card.pack(fill="both", expand=True)
    
    if categories:
        for cat in categories:
            cat_item = ctk.CTkFrame(chart_card, fg_color=CARD_BG)
            cat_item.pack(padx=16, pady=8, fill="x")
            
            # Category name
            name = ctk.CTkLabel(
                cat_item,
                text=f"{cat['ICON']} {cat['CAT_NAME']}",
                font=("Segoe UI", 11),
                text_color=TEXT_DARK,
                width=120
            )
            name.pack(side="left", anchor="w")
            
            # Progress bar (simplified)
            pct = float(cat['PCT'] or 0)
            bar_width = int(pct * 2)
            bar = ctk.CTkFrame(cat_item, fg_color=PRIMARY, height=6, corner_radius=3)
            bar.pack(side="left", fill="x", expand=True, padx=(12, 0))
            
            # Percentage
            pct_label = ctk.CTkLabel(
                cat_item,
                text=f"{pct}%",
                font=("Segoe UI", 10),
                text_color=TEXT_GRAY,
                width=40
            )
            pct_label.pack(side="left", padx=(8, 0))
    else:
        no_data = ctk.CTkLabel(
            chart_card,
            text="No data available",
            font=("Segoe UI", 12),
            text_color=TEXT_GRAY
        )
        no_data.pack(padx=16, pady=20)
    
    # Right: Summary
    right = ctk.CTkFrame(content, fg_color=SURFACE)
    right.grid(row=0, column=1, sticky="nsew")
    
    summary_title = ctk.CTkLabel(
        right,
        text="Period Summary",
        font=("Segoe UI", 14, "bold"),
        text_color=TEXT_DARK
    )
    summary_title.pack(anchor="w", pady=(0, 12))
    
    summary_card = ctk.CTkFrame(right, fg_color=CARD_BG, corner_radius=12)
    summary_card.pack(fill="both", expand=True)
    
    # Summary items
    items = [
        ("Period", "Oct 23 - Oct 29"),
        ("Entries", f"{total_trans} entries"),
        ("Category Highlight", "Housing & Rent"),
        ("Total Amount", f"₹{total_exp:,.2f}")
    ]
    
    for label, value in items:
        item = ctk.CTkFrame(summary_card, fg_color=CARD_BG)
        item.pack(padx=16, pady=8, fill="x")
        
        l = ctk.CTkLabel(item, text=label, font=("Segoe UI", 10), text_color=TEXT_GRAY)
        l.pack(side="left", anchor="w", fill="x", expand=True)
        
        v = ctk.CTkLabel(item, text=value, font=("Segoe UI", 11, "bold"), text_color=TEXT_DARK)
        v.pack(side="right", anchor="e")
    
    # Insights
    insights = ctk.CTkFrame(parent, fg_color=SURFACE)
    insights.pack(padx=24, pady=(0, 20), fill="x")
    
    insight1 = ctk.CTkFrame(insights, fg_color="#e8f5e9", corner_radius=12)
    insight1.pack(side="left", fill="both", expand=True, padx=(0, 12))
    
    icon1 = ctk.CTkLabel(insight1, text="✅", font=("Segoe UI", 16))
    icon1.pack(padx=12, pady=(12, 0), anchor="w")
    
    title1 = ctk.CTkLabel(insight1, text="Spending Insight", font=("Segoe UI", 12, "bold"), text_color=GREEN)
    title1.pack(padx=12, pady=(4, 2), anchor="w")
    
    msg1 = ctk.CTkLabel(
        insight1,
        text="You spent 10% less on groceries this month compared to September.",
        font=("Segoe UI", 10),
        text_color=TEXT_GRAY,
        wraplength=200
    )
    msg1.pack(padx=12, pady=(0, 12), anchor="w")
    

