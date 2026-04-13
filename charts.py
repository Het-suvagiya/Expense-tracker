import customtkinter as ctk
from database import run_query

# Colors
PRIMARY = "#004ac6"
SURFACE = "#f7f9fb"
CARD_BG = "#ffffff"
TEXT_DARK = "#191c1e"
TEXT_GRAY = "#434655"
GREEN = "#006c49"
RED = "#ab0b1c"
SECONDARY = "#006c49"
TERTIARY = "#ab0b1c"

def create_charts_page(parent, user_id):
    """Create charts and visualizations page"""
    
    # Get data for visualizations
    monthly_data = run_query(
        """SELECT * FROM (
               SELECT 
                   TO_CHAR(EXP_DATE, 'MON') as month,
                   SUM(CASE WHEN EXP_TYPE='Expense' THEN AMOUNT ELSE 0 END) as expenses
               FROM EXPENSES
               WHERE USER_ID=:1 AND EXP_DATE >= TRUNC(ADD_MONTHS(SYSDATE, -5), 'MM')
               GROUP BY TO_CHAR(EXP_DATE, 'MON'), EXP_DATE
               ORDER BY EXP_DATE DESC
           ) WHERE ROWNUM <= 6""",
        [user_id]
    )
    
    categories = run_query(
        """SELECT * FROM (
               SELECT c.CAT_NAME, SUM(e.AMOUNT) as total
               FROM EXPENSES e
               JOIN CATEGORIES c ON e.CAT_ID = c.CAT_ID
               WHERE e.USER_ID=:1 AND e.EXP_TYPE='Expense' AND TRUNC(e.EXP_DATE, 'MM') = TRUNC(SYSDATE, 'MM')
               GROUP BY c.CAT_NAME
               ORDER BY total DESC
           ) WHERE ROWNUM <= 4""",
        [user_id]
    )
    
    # Header
    header = ctk.CTkFrame(parent, fg_color=SURFACE)
    header.pack(padx=24, pady=(20, 0), fill="x")
    
    title = ctk.CTkLabel(
        header,
        text="Precision Visuals",
        font=("Segoe UI", 18, "bold"),
        text_color=TEXT_DARK
    )
    title.pack(anchor="w")
    
    subtitle = ctk.CTkLabel(
        header,
        text="Portfolio Overview",
        font=("Segoe UI", 10),
        text_color=TEXT_GRAY
    )
    subtitle.pack(anchor="w")
    
    # Tabs
    tab_frame = ctk.CTkFrame(header, fg_color=SURFACE)
    tab_frame.pack(anchor="e", pady=12)
    
    for tab in ["Monthly", "Quarterly", "Annual"]:
        is_active = tab == "Monthly"
        tab_btn = ctk.CTkButton(
            tab_frame,
            text=tab,
            font=("Segoe UI", 10),
            fg_color=PRIMARY if is_active else CARD_BG,
            text_color="white" if is_active else TEXT_GRAY,
            border_width=0,
            hover_color="#003d99" if is_active else "#eef1f5"
        )
        tab_btn.pack(side="left", padx=12)
    
    # Content
    content = ctk.CTkFrame(parent, fg_color=SURFACE)
    content.pack(padx=24, pady=20, fill="both", expand=True)
    content.grid_columnconfigure(0, weight=1)
    content.grid_columnconfigure(1, weight=1)
    
    # Left: Category Allocation Pie Chart
    left = ctk.CTkFrame(content, fg_color=SURFACE)
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
    
    chart1_title = ctk.CTkLabel(
        left,
        text="Category Allocation",
        font=("Segoe UI", 14, "bold"),
        text_color=TEXT_DARK
    )
    chart1_title.pack(anchor="w", pady=(0, 12))
    
    chart1_subtitle = ctk.CTkLabel(
        left,
        text="Distribution of expenditure",
        font=("Segoe UI", 10),
        text_color=TEXT_GRAY
    )
    chart1_subtitle.pack(anchor="w")
    
    chart1_card = ctk.CTkFrame(left, fg_color=CARD_BG, corner_radius=12)
    chart1_card.pack(fill="both", expand=True, pady=(8, 0))
    
    # Pie chart visualization (simplified - using rectangles)
    chart1_content = ctk.CTkFrame(chart1_card, fg_color=CARD_BG)
    chart1_content.pack(padx=24, pady=24, fill="both", expand=True)
    
    # Create colored blocks for pie chart
    colors = [PRIMARY, GREEN, RED, "#ff9800"]
    if categories:
        total = sum([float(c['TOTAL'] or 0) for c in categories])
        for i, cat in enumerate(categories):
            pct = (float(cat['TOTAL'] or 0) / total * 100) if total > 0 else 0
            
            cat_row = ctk.CTkFrame(chart1_content, fg_color=CARD_BG)
            cat_row.pack(fill="x", pady=(4, 4))
            
            # Color box
            color_box = ctk.CTkFrame(
                cat_row,
                fg_color=colors[i % len(colors)],
                width=16,
                height=16,
                corner_radius=2
            )
            color_box.pack(side="left", padx=(0, 8))
            
            # Label
            cat_label = ctk.CTkLabel(
                cat_row,
                text=f"● {cat['CAT_NAME']}",
                font=("Segoe UI", 10),
                text_color=TEXT_DARK,
                width=100
            )
            cat_label.pack(side="left")
            
            pct_label = ctk.CTkLabel(
                cat_row,
                text=f"{pct:.0f}%",
                font=("Segoe UI", 10),
                text_color=TEXT_GRAY
            )
            pct_label.pack(side="right")
    
    # Total spending label
    total_label = ctk.CTkLabel(
        chart1_card,
        text="TOTAL SPENT",
        font=("Segoe UI", 12),
        text_color=TEXT_GRAY,
        anchor="center"
    )
    total_label.pack(pady=(0, 4))
    
    total_amount = sum([float(c['TOTAL'] or 0) for c in categories])
    amount_label = ctk.CTkLabel(
        chart1_card,
        text=f"₹{total_amount:,.2f}",
        font=("Segoe UI", 24, "bold"),
        text_color=TEXT_DARK
    )
    amount_label.pack(pady=(0, 12))
    
    # Right: Combined chart area
    right = ctk.CTkFrame(content, fg_color=SURFACE)
    right.grid(row=0, column=1, sticky="nsew")
    
    # Efficiency score
    efficiency = ctk.CTkFrame(right, fg_color=SURFACE)
    efficiency.pack(fill="x", pady=(0, 12))
    
    eff_card = ctk.CTkFrame(efficiency, fg_color=CARD_BG, corner_radius=12)
    eff_card.pack(fill="both", expand=True)
    
    eff_title = ctk.CTkLabel(
        eff_card,
        text="Efficiency Score",
        font=("Segoe UI", 14, "bold"),
        text_color=TEXT_DARK
    )
    eff_title.pack(padx=20, pady=(16, 8), anchor="w")
    
    eff_msg = ctk.CTkLabel(
        eff_card,
        text="You spent 12% less on non-essential categories compared to last month. Keep it up!",
        font=("Segoe UI", 10),
        text_color=TEXT_GRAY,
        wraplength=300
    )
    eff_msg.pack(padx=20, pady=(0, 12), anchor="w")
    
    eff_bar = ctk.CTkProgressBar(eff_card, fg_color="#e0e0e0", progress_color=SECONDARY)
    eff_bar.set(0.88)
    eff_bar.pack(padx=20, pady=(0, 8), fill="x")
    
    eff_pct = ctk.CTkLabel(
        eff_card,
        text="88%",
        font=("Segoe UI", 12, "bold"),
        text_color=SECONDARY
    )
    eff_pct.pack(padx=20, pady=(0, 20), anchor="w")
    
    # Progress to goal
    goal = ctk.CTkFrame(right, fg_color=SURFACE)
    goal.pack(fill="x")
    
    goal_card = ctk.CTkFrame(goal, fg_color=PRIMARY, corner_radius=12)
    goal_card.pack(fill="both", expand=True)
    
    goal_title = ctk.CTkLabel(
        goal_card,
        text="PROGRESS TO GOAL",
        font=("Segoe UI", 10),
        text_color="#dbe7ff"
    )
    goal_title.pack(padx=20, pady=(16, 4), anchor="w")
    
    goal_amount = ctk.CTkLabel(
        goal_card,
        text="₹4,200.50",
        font=("Segoe UI", 24, "bold"),
        text_color="white"
    )
    goal_amount.pack(padx=20, pady=(0, 4), anchor="w")
    
    goal_info = ctk.CTkButton(
        goal_card,
        text="View Details",
        font=("Segoe UI", 10),
        fg_color="#4f79df",
        hover_color="#6a8fe6",
        text_color="white",
        border_width=0,
        height=28
    )
    goal_info.pack(padx=20, pady=(0, 16), fill="x")
    
    # Bottom: Monthly spending comparison
    bottom = ctk.CTkFrame(parent, fg_color=SURFACE)
    bottom.pack(padx=24, pady=(0, 20), fill="both", expand=True)
    
    comp_title = ctk.CTkLabel(
        bottom,
        text="Monthly Spending Comparison",
        font=("Segoe UI", 14, "bold"),
        text_color=TEXT_DARK
    )
    comp_title.pack(anchor="w", pady=(0, 12))
    
    comp_subtitle = ctk.CTkLabel(
        bottom,
        text="Last 6 months performance analysis",
        font=("Segoe UI", 10),
        text_color=TEXT_GRAY
    )
    comp_subtitle.pack(anchor="w")
    
    chart_card = ctk.CTkFrame(bottom, fg_color=CARD_BG, corner_radius=12)
    chart_card.pack(fill="both", expand=True, pady=(8, 0))
    
    # Bar chart visualization
    chart_content = ctk.CTkFrame(chart_card, fg_color=CARD_BG)
    chart_content.pack(padx=24, pady=24, fill="both", expand=True)
    
    bars_frame = ctk.CTkFrame(chart_content, fg_color=CARD_BG, height=180)
    bars_frame.pack(fill="both", expand=True)
    bars_frame.pack_propagate(False)
    
    if monthly_data:
        chronological = list(reversed(monthly_data))
        max_val = max([float(m['EXPENSES'] or 0) for m in chronological])
        if max_val == 0: max_val = 1
        
        for i, data in enumerate(chronological):
            month_name = data['MONTH']
            val = float(data['EXPENSES'] or 0)
            pct = val / max_val
            
            bar_col = ctk.CTkFrame(bars_frame, fg_color=CARD_BG)
            bar_col.pack(side="left", fill="both", expand=True, padx=4)
            
            # Label anchored bottom
            month_label = ctk.CTkLabel(
                bar_col,
                text=month_name,
                font=("Segoe UI", 9),
                text_color=TEXT_GRAY
            )
            month_label.pack(side="bottom")
            
            # The fill frame wraps the colored bar pushing it bottom
            fill_frame = ctk.CTkFrame(bar_col, fg_color=CARD_BG)
            fill_frame.pack(side="bottom", fill="both", expand=True)
            
            bar_color = PRIMARY if i == len(chronological)-1 else "#c3d9f0"
            bar_height = max(10, int(150 * pct))
            
            bar_frame = ctk.CTkFrame(fill_frame, fg_color=bar_color, corner_radius=4, height=bar_height)
            bar_frame.pack(side="bottom", fill="x", pady=(0, 4))
    else:
        ctk.CTkLabel(bars_frame, text="No data available", text_color=TEXT_GRAY).pack(expand=True)
    
    # Legend
    legend_frame = ctk.CTkFrame(chart_card, fg_color=CARD_BG)
    legend_frame.pack(fill="x", padx=24, pady=(0, 16))
    
    fixed_label = ctk.CTkLabel(legend_frame, text="■ Fixed Costs", font=("Segoe UI", 10), text_color=TEXT_GRAY)
    fixed_label.pack(side="left", padx=(0, 16))
    
    variable_label = ctk.CTkLabel(legend_frame, text="■ Variable", font=("Segoe UI", 10), text_color=TEXT_GRAY)
    variable_label.pack(side="left")
    
    # Info panel
    info_frame = ctk.CTkFrame(parent, fg_color=SURFACE)
    info_frame.pack(padx=24, pady=(0, 20), fill="x")
    
    info_label = ctk.CTkLabel(
        info_frame,
        text="Last updated: 2 minutes ago   •   Export PDF Report   •   Raw CSV Data   •   LIVE SYNC ACTIVE",
        font=("Segoe UI", 9),
        text_color=TEXT_GRAY
    )
    info_label.pack(anchor="e")
