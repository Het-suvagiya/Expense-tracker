import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from database import run_query, run_command
from datetime import datetime

# Colors
PRIMARY = "#004ac6"
SURFACE = "#f7f9fb"
CARD_BG = "#ffffff"
TEXT_DARK = "#191c1e"
TEXT_GRAY = "#434655"
GREEN = "#006c49"
RED = "#ab0b1c"


def _refresh_expenses_page(parent, user_id):
    """Reload expenses page content in place."""
    for widget in parent.winfo_children():
        widget.destroy()
    create_expenses_page(parent, user_id)

def create_expenses_page(parent, user_id):
    """Create expenses page"""
    
    # Get all expenses
    expenses = run_query(
        """SELECT e.EXP_ID, e.DESCRIPTION, e.AMOUNT, e.EXP_DATE, e.EXP_TYPE, 
                  c.CAT_NAME, c.ICON, c.COLOR, e.STATUS
           FROM EXPENSES e
           JOIN CATEGORIES c ON e.CAT_ID = c.CAT_ID
           WHERE e.USER_ID=:1
           ORDER BY e.EXP_DATE DESC""",
        [user_id]
    )
    
    # Get month-to-date sum
    month_sum = run_query(
        """SELECT SUM(CASE WHEN EXP_TYPE='Expense' THEN AMOUNT ELSE 0 END) as expenses,
                  SUM(CASE WHEN EXP_TYPE='Income' THEN AMOUNT ELSE 0 END) as income,
                  COUNT(*) as count
           FROM EXPENSES
           WHERE USER_ID=:1 AND TRUNC(EXP_DATE, 'MM') = TRUNC(SYSDATE, 'MM')""",
        [user_id]
    )
    
    month_expenses = float(month_sum[0]['EXPENSES'] or 0) if month_sum else 0
    income = float(month_sum[0]['INCOME'] or 0) if month_sum else 0
    
    # Header with stats
    header = ctk.CTkFrame(parent, fg_color=SURFACE)
    header.pack(padx=24, pady=(12, 12), fill="x")
    
    # Stats cards
    stats_frame = ctk.CTkFrame(header, fg_color=SURFACE)
    stats_frame.pack(fill="x")
    
    # Card 1: Month to date
    card1 = ctk.CTkFrame(stats_frame, fg_color=CARD_BG, corner_radius=12)
    card1.pack(side="left", fill="both", expand=True, padx=(0, 12), pady=(0, 0))
    
    label1 = ctk.CTkLabel(card1, text="MONTH TO DATE", font=("Segoe UI", 10), text_color=TEXT_GRAY)
    label1.pack(padx=16, pady=(12, 4), anchor="w")
    
    amount1 = ctk.CTkLabel(card1, text=f"₹{month_expenses:,.2f}", font=("Segoe UI", 20, "bold"), text_color=TEXT_DARK)
    amount1.pack(padx=16, pady=(0, 12), anchor="w")
    

    
    # Card 3: Largest expense
    card3 = ctk.CTkFrame(stats_frame, fg_color=CARD_BG, corner_radius=12)
    card3.pack(side="left", fill="both", expand=True, pady=(0, 0))
    
    label3 = ctk.CTkLabel(card3, text="LARGEST EXPENSE", font=("Segoe UI", 10), text_color=TEXT_GRAY)
    label3.pack(padx=16, pady=(12, 4), anchor="w")
    
    largest = max([float(e['AMOUNT']) for e in expenses if e['EXP_TYPE'] == 'Expense'], default=0)
    amount3 = ctk.CTkLabel(card3, text=f"₹{largest:,.2f}", font=("Segoe UI", 20, "bold"), text_color=RED)
    amount3.pack(padx=16, pady=(0, 12), anchor="w")
    
    # Add expense button
    button_frame = ctk.CTkFrame(header, fg_color=SURFACE)
    button_frame.pack(fill="x", pady=(12, 0))
    
    add_btn = ctk.CTkButton(
        button_frame,
        text="+ Add New Expense",
        command=lambda: add_expense_modal(parent, user_id),
        fg_color=PRIMARY,
        hover_color="#003d99",
        text_color="white",
        font=("Segoe UI", 12, "bold")
    )
    add_btn.pack(side="right")
    
    # Expenses table/list
    table_frame = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=12)
    table_frame.pack(padx=24, pady=(0, 12), fill="both", expand=True)
    
    # Table header
    header_frame = ctk.CTkFrame(table_frame, fg_color="#f5f5f5", corner_radius=0)
    header_frame.pack(fill="x", padx=0, pady=0)
    
    header_labels = ["DATE", "CATEGORY", "DESCRIPTION", "AMOUNT", "STATUS", "ACTIONS"]
    col_widths = [100, 150, 250, 120, 120, 100]
    
    for label, width in zip(header_labels, col_widths):
        h = ctk.CTkLabel(
            header_frame,
            text=label,
            font=("Segoe UI", 10, "bold"),
            text_color=TEXT_GRAY,
            width=width
        )
        h.pack(side="left", padx=12, pady=12)
    
    # Scrollable content
    content = ctk.CTkScrollableFrame(table_frame, fg_color=CARD_BG)
    content.pack(fill="both", expand=True, padx=0, pady=0)
    
    if expenses:
        for exp in expenses:
            row = ctk.CTkFrame(content, fg_color=CARD_BG, corner_radius=0)
            row.pack(fill="x", padx=0, pady=0)
            
            # Date
            date_label = ctk.CTkLabel(
                row,
                text=str(exp['EXP_DATE'])[:10],
                font=("Segoe UI", 10),
                text_color=TEXT_DARK,
                width=100
            )
            date_label.pack(side="left", padx=12, pady=8)
            
            # Category
            cat_label = ctk.CTkLabel(
                row,
                text=f"{exp['ICON']} {exp['CAT_NAME']}",
                font=("Segoe UI", 10),
                text_color=TEXT_DARK,
                width=150
            )
            cat_label.pack(side="left", padx=12, pady=8)
            
            # Description
            desc_label = ctk.CTkLabel(
                row,
                text=(exp['DESCRIPTION'] or '')[:30],
                font=("Segoe UI", 10),
                text_color=TEXT_GRAY,
                width=250
            )
            desc_label.pack(side="left", padx=12, pady=8)
            
            # Amount
            amount_color = GREEN if exp['EXP_TYPE'] == 'Income' else TEXT_DARK
            amount_label = ctk.CTkLabel(
                row,
                text=f"₹{float(exp['AMOUNT']):,.2f}",
                font=("Segoe UI", 10, "bold"),
                text_color=amount_color,
                width=120
            )
            amount_label.pack(side="left", padx=12, pady=8)
            
            # Status
            status_color = GREEN if exp['STATUS'] == 'Completed' else TEXT_GRAY
            status_label = ctk.CTkLabel(
                row,
                text=exp['STATUS'],
                font=("Segoe UI", 10),
                text_color=status_color,
                width=120
            )
            status_label.pack(side="left", padx=12, pady=8)
            
            # Actions
            actions = ctk.CTkFrame(row, fg_color=CARD_BG)
            actions.pack(side="left", padx=12, pady=8)
            
            edit_btn = ctk.CTkButton(
                actions,
                text="✏",
                width=30,
                height=30,
                corner_radius=6,
                fg_color=PRIMARY,
                hover_color="#003d99",
                text_color="white",
                font=("Segoe UI", 12),
                command=lambda eid=exp['EXP_ID']: edit_expense_modal(parent, user_id, eid)
            )
            edit_btn.pack(side="left", padx=(0, 4))
            
            del_btn = ctk.CTkButton(
                actions,
                text="🗑",
                width=30,
                height=30,
                corner_radius=6,
                fg_color=RED,
                hover_color="#8b0000",
                text_color="white",
                font=("Segoe UI", 10),
                command=lambda eid=exp['EXP_ID']: delete_expense(user_id, eid, parent)
            )
            del_btn.pack(side="left")
    else:
        no_data = ctk.CTkLabel(
            content,
            text="No expenses yet. Add your first expense!",
            font=("Segoe UI", 12),
            text_color=TEXT_GRAY
        )
        no_data.pack(padx=16, pady=20)

def add_expense_modal(parent, user_id):
    """Popup to add new expense inside current page."""
    overlay = ctk.CTkFrame(parent, fg_color="#c6ccd6", corner_radius=0)
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    overlay.lift()

    modal = ctk.CTkFrame(overlay, fg_color="#fdfefe", corner_radius=16, width=560, height=500)
    modal.place(relx=0.5, rely=0.5, anchor="center")
    modal.pack_propagate(False)

    header = ctk.CTkFrame(modal, fg_color="#fdfefe")
    header.pack(fill="x", padx=20, pady=(18, 8))

    title = ctk.CTkLabel(
        header,
        text="Add Expense",
        font=("Segoe UI", 24, "bold"),
        text_color=TEXT_DARK
    )
    title.pack(side="left")

    close_btn = ctk.CTkButton(
        header,
        text="X",
        width=34,
        height=34,
        corner_radius=17,
        fg_color="#eef1f6",
        hover_color="#e1e6ef",
        text_color=TEXT_GRAY,
        font=("Segoe UI", 12, "bold"),
        command=overlay.destroy
    )
    close_btn.pack(side="right")

    # Form frame
    form = ctk.CTkFrame(modal, fg_color="#f3f6fb", corner_radius=12)
    form.pack(fill="both", expand=True, padx=20, pady=(0, 16))
    
    # Category
    ctk.CTkLabel(form, text="Category *", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(14, 6))
    categories = run_query("SELECT CAT_ID, CAT_NAME, ICON FROM CATEGORIES ORDER BY CAT_NAME")
    cat_options = [f"{c['ICON']} {c['CAT_NAME']}" for c in categories]
    cat_var = ctk.StringVar(value=cat_options[0] if cat_options else "")
    cat_menu = ctk.CTkComboBox(
        form,
        values=cat_options,
        variable=cat_var,
        state="readonly",
        height=38,
        corner_radius=8,
        fg_color="#ffffff",
        border_width=1,
        border_color="#d4dbe7",
        button_color="#e9eff8",
        button_hover_color="#dce6f5",
        dropdown_fg_color="#ffffff",
        dropdown_text_color=TEXT_DARK,
        dropdown_hover_color="#edf2ff",
        text_color=TEXT_DARK,
        font=("Segoe UI", 12)
    )
    cat_menu.pack(fill="x", padx=16, pady=(0, 10))
    
    # Amount
    ctk.CTkLabel(form, text="Amount *", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(0, 6))
    amount_entry = ctk.CTkEntry(
        form,
        placeholder_text="0.00",
        height=38,
        corner_radius=8,
        fg_color="#ffffff",
        border_width=1,
        border_color="#d4dbe7",
        text_color=TEXT_DARK,
        placeholder_text_color="#8b95a6",
        font=("Segoe UI", 12)
    )
    amount_entry.pack(fill="x", padx=16, pady=(0, 10))
    
    # Description
    ctk.CTkLabel(form, text="Description", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(0, 6))
    desc_entry = ctk.CTkEntry(
        form,
        placeholder_text="What is this for?",
        height=38,
        corner_radius=8,
        fg_color="#ffffff",
        border_width=1,
        border_color="#d4dbe7",
        text_color=TEXT_DARK,
        placeholder_text_color="#8b95a6",
        font=("Segoe UI", 12)
    )
    desc_entry.pack(fill="x", padx=16, pady=(0, 10))
    
    # Type
    ctk.CTkLabel(form, text="Type", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(0, 6))
    type_var = ctk.StringVar(value="Expense")
    type_menu = ctk.CTkComboBox(
        form,
        values=["Expense", "Income"],
        variable=type_var,
        state="readonly",
        height=38,
        corner_radius=8,
        fg_color="#ffffff",
        border_width=1,
        border_color="#d4dbe7",
        button_color="#e9eff8",
        button_hover_color="#dce6f5",
        dropdown_fg_color="#ffffff",
        dropdown_text_color=TEXT_DARK,
        dropdown_hover_color="#edf2ff",
        text_color=TEXT_DARK,
        font=("Segoe UI", 12)
    )
    type_menu.pack(fill="x", padx=16, pady=(0, 14))
    
    # Buttons
    btn_frame = ctk.CTkFrame(form, fg_color="#f3f6fb")
    btn_frame.pack(fill="x", padx=16, pady=(8, 16))
    
    def save_expense():
        try:
            cat_name = cat_var.get().split(" ", 1)[1] if " " in cat_var.get() else cat_var.get()
            cat = next((c for c in categories if c['CAT_NAME'] == cat_name), None)
            
            if not cat or not amount_entry.get():
                CTkMessagebox(title="Error", message="Please fill all fields")
                return
            
            run_command(
                """INSERT INTO EXPENSES (EXP_ID, USER_ID, CAT_ID, AMOUNT, EXP_DATE, 
                   DESCRIPTION, EXP_TYPE, STATUS) 
                   VALUES (expenses_seq.NEXTVAL, :1, :2, :3, SYSDATE, :4, :5, 'Completed')""",
                [user_id, cat['CAT_ID'], float(amount_entry.get()), desc_entry.get(), type_var.get()]
            )
            
            CTkMessagebox(title="Success", message="Expense added successfully!")
            overlay.destroy()
            _refresh_expenses_page(parent, user_id)
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e))
    
    save_btn = ctk.CTkButton(
        btn_frame,
        text="Save Expense",
        command=save_expense,
        fg_color=PRIMARY,
        hover_color="#003d99",
        text_color="white",
        font=("Segoe UI", 12, "bold"),
        height=40,
        corner_radius=10,
        width=180
    )
    save_btn.pack(side="right")
    
    cancel_btn = ctk.CTkButton(
        btn_frame,
        text="Cancel",
        command=overlay.destroy,
        fg_color="#dfe3e8",
        hover_color="#d2d8de",
        text_color=TEXT_DARK,
        font=("Segoe UI", 12, "bold"),
        height=40,
        corner_radius=10,
        width=180
    )
    cancel_btn.pack(side="right", padx=(0, 10))

def edit_expense_modal(parent, user_id, exp_id):
    """Modal to edit expense"""
    exp_data = run_query("SELECT CAT_ID, AMOUNT, DESCRIPTION, EXP_TYPE FROM EXPENSES WHERE EXP_ID=:1 AND USER_ID=:2", [exp_id, user_id])
    if not exp_data:
        return
    current = exp_data[0]
    
    overlay = ctk.CTkFrame(parent, fg_color="#c6ccd6", corner_radius=0)
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    overlay.lift()

    modal = ctk.CTkFrame(overlay, fg_color="#fdfefe", corner_radius=16, width=560, height=500)
    modal.place(relx=0.5, rely=0.5, anchor="center")
    modal.pack_propagate(False)

    header = ctk.CTkFrame(modal, fg_color="#fdfefe")
    header.pack(fill="x", padx=20, pady=(18, 8))

    ctk.CTkLabel(header, text="Edit Expense", font=("Segoe UI", 24, "bold"), text_color=TEXT_DARK).pack(side="left")
    ctk.CTkButton(header, text="X", width=34, height=34, corner_radius=17, fg_color="#eef1f6", hover_color="#e1e6ef", text_color=TEXT_GRAY, font=("Segoe UI", 12, "bold"), command=overlay.destroy).pack(side="right")

    form = ctk.CTkFrame(modal, fg_color="#f3f6fb", corner_radius=12)
    form.pack(fill="both", expand=True, padx=20, pady=(0, 16))
    
    # Category
    ctk.CTkLabel(form, text="Category *", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(14, 6))
    categories = run_query("SELECT CAT_ID, CAT_NAME, ICON FROM CATEGORIES ORDER BY CAT_NAME")
    cat_options = [f"{c['ICON']} {c['CAT_NAME']}" for c in categories]
    cat_var = ctk.StringVar()
    for cat in categories:
        if cat['CAT_ID'] == current['CAT_ID']:
            cat_var.set(f"{cat['ICON']} {cat['CAT_NAME']}")
            break

    cat_menu = ctk.CTkComboBox(form, values=cat_options, variable=cat_var, state="readonly", height=38, corner_radius=8, fg_color="#ffffff", border_width=1, border_color="#d4dbe7", button_color="#e9eff8", text_color=TEXT_DARK, font=("Segoe UI", 12))
    cat_menu.pack(fill="x", padx=16, pady=(0, 10))
    
    # Amount
    ctk.CTkLabel(form, text="Amount *", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(0, 6))
    amount_entry = ctk.CTkEntry(form, height=38, corner_radius=8, fg_color="#ffffff", border_width=1, border_color="#d4dbe7", text_color=TEXT_DARK, font=("Segoe UI", 12))
    amount_entry.insert(0, str(current['AMOUNT']))
    amount_entry.pack(fill="x", padx=16, pady=(0, 10))
    
    # Description
    ctk.CTkLabel(form, text="Description", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(0, 6))
    desc_entry = ctk.CTkEntry(form, height=38, corner_radius=8, fg_color="#ffffff", border_width=1, border_color="#d4dbe7", text_color=TEXT_DARK, font=("Segoe UI", 12))
    desc_entry.insert(0, current['DESCRIPTION'] or '')
    desc_entry.pack(fill="x", padx=16, pady=(0, 10))
    
    # Type
    ctk.CTkLabel(form, text="Type", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(0, 6))
    type_var = ctk.StringVar(value=current['EXP_TYPE'] or "Expense")
    type_menu = ctk.CTkComboBox(form, values=["Expense", "Income"], variable=type_var, state="readonly", height=38, corner_radius=8, fg_color="#ffffff", border_width=1, border_color="#d4dbe7", button_color="#e9eff8", text_color=TEXT_DARK, font=("Segoe UI", 12))
    type_menu.pack(fill="x", padx=16, pady=(0, 14))
    
    btn_frame = ctk.CTkFrame(form, fg_color="#f3f6fb")
    btn_frame.pack(fill="x", padx=16, pady=(8, 16))
    
    def update_expense():
        try:
            cat_name = cat_var.get().split(" ", 1)[1] if " " in cat_var.get() else cat_var.get()
            cat = next((c for c in categories if c['CAT_NAME'] == cat_name), None)
            
            if not cat or not amount_entry.get():
                CTkMessagebox(title="Error", message="Please fill all fields")
                return
            
            run_command(
                "UPDATE EXPENSES SET CAT_ID=:1, AMOUNT=:2, DESCRIPTION=:3, EXP_TYPE=:4 WHERE EXP_ID=:5",
                [cat['CAT_ID'], float(amount_entry.get()), desc_entry.get(), type_var.get(), exp_id]
            )
            
            CTkMessagebox(title="Success", message="Expense updated!")
            overlay.destroy()
            _refresh_expenses_page(parent, user_id)
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e))
    
    ctk.CTkButton(btn_frame, text="Update Expense", command=update_expense, fg_color=PRIMARY, hover_color="#003d99", text_color="white", font=("Segoe UI", 12, "bold"), height=40, corner_radius=10, width=180).pack(side="right")
    ctk.CTkButton(btn_frame, text="Cancel", command=overlay.destroy, fg_color="#dfe3e8", hover_color="#d2d8de", text_color=TEXT_DARK, font=("Segoe UI", 12, "bold"), height=40, corner_radius=10, width=180).pack(side="right", padx=(0, 10))

def delete_expense(user_id, exp_id, parent):
    """Delete an expense"""
    response = CTkMessagebox(
        title="Delete",
        message="Are you sure you want to delete this expense?",
        icon="question",
        option_1="Yes",
        option_2="No"
    )
    
    if response.get() == "Yes":
        run_command("DELETE FROM EXPENSES WHERE EXP_ID=:1 AND USER_ID=:2", [exp_id, user_id])
        CTkMessagebox(title="Success", message="Expense deleted!")
        _refresh_expenses_page(parent, user_id)
