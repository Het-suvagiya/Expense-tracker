import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from database import run_query, run_command

# Colors
PRIMARY = "#004ac6"
SURFACE = "#f7f9fb"
CARD_BG = "#ffffff"
TEXT_DARK = "#191c1e"
TEXT_GRAY = "#434655"
GREEN = "#006c49"
RED = "#ab0b1c"


def _refresh_categories_page(parent, user_id):
    """Reload categories page content in place."""
    for widget in parent.winfo_children():
        widget.destroy()
    create_categories_page(parent, user_id)

def create_categories_page(parent, user_id):
    """Create categories management page"""
    
    # Get all categories with sum of expenses
    categories = run_query(
        """SELECT c.CAT_ID, c.CAT_NAME, c.ICON, c.COLOR, c.DESCRIPTION,
                  SUM(CASE WHEN e.EXP_TYPE='Expense' THEN e.AMOUNT ELSE 0 END) as total
           FROM CATEGORIES c
           LEFT JOIN EXPENSES e ON c.CAT_ID = e.CAT_ID AND e.USER_ID=:1
           GROUP BY c.CAT_ID, c.CAT_NAME, c.ICON, c.COLOR, c.DESCRIPTION
           ORDER BY total DESC""",
        [user_id]
    )
    
    # Header
    header = ctk.CTkFrame(parent, fg_color=SURFACE)
    header.pack(padx=24, pady=(20, 20), fill="x")
    
    title = ctk.CTkLabel(
        header,
        text="Structure Your Spending",
        font=("Segoe UI", 18, "bold"),
        text_color=TEXT_DARK
    )
    title.pack(anchor="w")
    
    subtitle = ctk.CTkLabel(
        header,
        text="Manage and refine how you classify every transaction for better insights.",
        font=("Segoe UI", 12),
        text_color=TEXT_GRAY
    )
    subtitle.pack(anchor="w", pady=(4, 12))
    
    add_btn = ctk.CTkButton(
        header,
        text="+ New Category",
        fg_color=PRIMARY,
        hover_color="#003d99",
        text_color="white",
        command=lambda: add_category_modal(parent, user_id)
    )
    add_btn.pack(side="right")
    
    # Categories grid
    grid_frame = ctk.CTkScrollableFrame(parent, fg_color=SURFACE)
    grid_frame.pack(padx=24, pady=(0, 20), fill="both", expand=True)
    
    if categories:
        # Display categories in a 3-column grid
        for i, cat in enumerate(categories):
            if i % 3 == 0:
                row_frame = ctk.CTkFrame(grid_frame, fg_color=SURFACE)
                row_frame.pack(fill="x", pady=(0, 16))
            
            cat_card = ctk.CTkFrame(row_frame, fg_color=CARD_BG, corner_radius=12)
            cat_card.pack(side="left", fill="both", expand=True, padx=(0, 16), ipadx=0)
            
            # Icon and name
            top = ctk.CTkFrame(cat_card, fg_color=CARD_BG)
            top.pack(fill="x", padx=16, pady=(16, 8))
            
            icon = ctk.CTkLabel(
                top,
                text=cat['ICON'],
                font=("Segoe UI", 32)
            )
            icon.pack(anchor="w")
            
            cat_name = ctk.CTkLabel(
                top,
                text=cat['CAT_NAME'],
                font=("Segoe UI", 14, "bold"),
                text_color=TEXT_DARK,
                wraplength=200
            )
            cat_name.pack(anchor="w", pady=(8, 0))
            
            cat_desc = ctk.CTkLabel(
                top,
                text=cat['DESCRIPTION'],
                font=("Segoe UI", 10),
                text_color=TEXT_GRAY,
                wraplength=200
            )
            cat_desc.pack(anchor="w", pady=(4, 0))
            
            # Total spent
            total_spent = float(cat['TOTAL'] or 0)
            amount = ctk.CTkLabel(
                top,
                text=f"₹{total_spent:,.2f}",
                font=("Segoe UI", 16, "bold"),
                text_color=PRIMARY,
                wraplength=200
            )
            amount.pack(anchor="w", pady=(8, 0))
            
            amount_label = ctk.CTkLabel(
                top,
                text="This Month",
                font=("Segoe UI", 9),
                text_color=TEXT_GRAY
            )
            amount_label.pack(anchor="w")
            
            # Action buttons
            actions = ctk.CTkFrame(cat_card, fg_color=CARD_BG)
            actions.pack(fill="x", padx=16, pady=(0, 16))
            
            edit_btn = ctk.CTkButton(
                actions,
                text="Edit",
                width=60,
                height=32,
                corner_radius=6,
                fg_color=PRIMARY,
                hover_color="#003d99",
                text_color="white",
                font=("Segoe UI", 10),
                command=lambda cid=cat['CAT_ID'], cname=cat['CAT_NAME']: edit_category_modal(parent, user_id, cid, cname)
            )
            edit_btn.pack(side="left", padx=(0, 6))
            
            delete_btn = ctk.CTkButton(
                actions,
                text="Delete",
                width=60,
                height=32,
                corner_radius=6,
                fg_color=RED,
                hover_color="#8b0000",
                text_color="white",
                font=("Segoe UI", 10),
                command=lambda cid=cat['CAT_ID']: delete_category(user_id, cid, parent)
            )
            delete_btn.pack(side="left")
    else:
        no_data = ctk.CTkLabel(
            grid_frame,
            text="No categories found",
            font=("Segoe UI", 12),
            text_color=TEXT_GRAY
        )
        no_data.pack(padx=16, pady=20)

def add_category_modal(parent, user_id):
    """Popup to add new category inside current page."""
    overlay = ctk.CTkFrame(parent, fg_color="#c6ccd6", corner_radius=0)
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    overlay.lift()

    modal = ctk.CTkFrame(overlay, fg_color="#fdfefe", corner_radius=16, width=500, height=470)
    modal.place(relx=0.5, rely=0.5, anchor="center")
    modal.pack_propagate(False)

    header = ctk.CTkFrame(modal, fg_color="#fdfefe")
    header.pack(fill="x", padx=20, pady=(18, 8))

    title = ctk.CTkLabel(
        header,
        text="Add Category",
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
    
    # Category name
    ctk.CTkLabel(form, text="Category Name *", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(14, 6))
    name_entry = ctk.CTkEntry(
        form,
        placeholder_text="e.g., Groceries",
        height=38,
        corner_radius=8,
        fg_color="#ffffff",
        border_width=1,
        border_color="#d4dbe7",
        text_color=TEXT_DARK,
        placeholder_text_color="#8b95a6",
        font=("Segoe UI", 12)
    )
    name_entry.pack(fill="x", padx=16, pady=(0, 10))
    
    # Icon
    ctk.CTkLabel(form, text="Icon *", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(0, 6))
    icon_entry = ctk.CTkEntry(
        form,
        placeholder_text="e.g., cart",
        height=38,
        corner_radius=8,
        fg_color="#ffffff",
        border_width=1,
        border_color="#d4dbe7",
        text_color=TEXT_DARK,
        placeholder_text_color="#8b95a6",
        font=("Segoe UI", 12)
    )
    icon_entry.pack(fill="x", padx=16, pady=(0, 10))
    
    # Color
    ctk.CTkLabel(form, text="Color (hex)", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(0, 6))
    color_entry = ctk.CTkEntry(
        form,
        placeholder_text="e.g., #004ac6",
        height=38,
        corner_radius=8,
        fg_color="#ffffff",
        border_width=1,
        border_color="#d4dbe7",
        text_color=TEXT_DARK,
        placeholder_text_color="#8b95a6",
        font=("Segoe UI", 12)
    )
    color_entry.pack(fill="x", padx=16, pady=(0, 10))
    
    # Description
    ctk.CTkLabel(form, text="Description", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(0, 6))
    desc_entry = ctk.CTkEntry(
        form,
        placeholder_text="e.g., Monthly food and dining",
        height=38,
        corner_radius=8,
        fg_color="#ffffff",
        border_width=1,
        border_color="#d4dbe7",
        text_color=TEXT_DARK,
        placeholder_text_color="#8b95a6",
        font=("Segoe UI", 12)
    )
    desc_entry.pack(fill="x", padx=16, pady=(0, 14))
    
    # Buttons
    btn_frame = ctk.CTkFrame(form, fg_color="#f3f6fb")
    btn_frame.pack(fill="x", padx=16, pady=(8, 16))
    
    def save_category():
        try:
            if not name_entry.get() or not icon_entry.get():
                CTkMessagebox(title="Error", message="Please fill required fields")
                return
            
            run_command(
                """INSERT INTO CATEGORIES (CAT_ID, CAT_NAME, ICON, COLOR, DESCRIPTION)
                   VALUES (categories_seq.NEXTVAL, :1, :2, :3, :4)""",
                [name_entry.get(), icon_entry.get(), color_entry.get(), desc_entry.get()]
            )
            
            CTkMessagebox(title="Success", message="Category added successfully!")
            overlay.destroy()
            _refresh_categories_page(parent, user_id)
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e))
    
    save_btn = ctk.CTkButton(
        btn_frame,
        text="Save Category",
        command=save_category,
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

def edit_category_modal(parent, user_id, cat_id, cat_name):
    """Modal to edit category"""
    cat_data = run_query("SELECT ICON, COLOR, DESCRIPTION FROM CATEGORIES WHERE CAT_ID=:1", [cat_id])
    if not cat_data:
        return
    current = cat_data[0]
    
    overlay = ctk.CTkFrame(parent, fg_color="#c6ccd6", corner_radius=0)
    overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    overlay.lift()

    modal = ctk.CTkFrame(overlay, fg_color="#fdfefe", corner_radius=16, width=500, height=470)
    modal.place(relx=0.5, rely=0.5, anchor="center")
    modal.pack_propagate(False)

    header = ctk.CTkFrame(modal, fg_color="#fdfefe")
    header.pack(fill="x", padx=20, pady=(18, 8))

    ctk.CTkLabel(header, text="Edit Category", font=("Segoe UI", 24, "bold"), text_color=TEXT_DARK).pack(side="left")
    ctk.CTkButton(header, text="X", width=34, height=34, corner_radius=17, fg_color="#eef1f6", hover_color="#e1e6ef", text_color=TEXT_GRAY, font=("Segoe UI", 12, "bold"), command=overlay.destroy).pack(side="right")

    form = ctk.CTkFrame(modal, fg_color="#f3f6fb", corner_radius=12)
    form.pack(fill="both", expand=True, padx=20, pady=(0, 16))
    
    ctk.CTkLabel(form, text="Category Name *", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(14, 6))
    name_entry = ctk.CTkEntry(form, height=38, corner_radius=8, fg_color="#ffffff", border_width=1, border_color="#d4dbe7", text_color=TEXT_DARK, font=("Segoe UI", 12))
    name_entry.insert(0, cat_name)
    name_entry.pack(fill="x", padx=16, pady=(0, 10))
    
    ctk.CTkLabel(form, text="Icon *", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(0, 6))
    icon_entry = ctk.CTkEntry(form, height=38, corner_radius=8, fg_color="#ffffff", border_width=1, border_color="#d4dbe7", text_color=TEXT_DARK, font=("Segoe UI", 12))
    icon_entry.insert(0, current['ICON'] or '')
    icon_entry.pack(fill="x", padx=16, pady=(0, 10))
    
    ctk.CTkLabel(form, text="Color (hex)", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(0, 6))
    color_entry = ctk.CTkEntry(form, height=38, corner_radius=8, fg_color="#ffffff", border_width=1, border_color="#d4dbe7", text_color=TEXT_DARK, font=("Segoe UI", 12))
    color_entry.insert(0, current['COLOR'] or '')
    color_entry.pack(fill="x", padx=16, pady=(0, 10))
    
    ctk.CTkLabel(form, text="Description", font=("Segoe UI", 12, "bold"), text_color=TEXT_DARK).pack(anchor="w", padx=16, pady=(0, 6))
    desc_entry = ctk.CTkEntry(form, height=38, corner_radius=8, fg_color="#ffffff", border_width=1, border_color="#d4dbe7", text_color=TEXT_DARK, font=("Segoe UI", 12))
    desc_entry.insert(0, current['DESCRIPTION'] or '')
    desc_entry.pack(fill="x", padx=16, pady=(0, 14))
    
    btn_frame = ctk.CTkFrame(form, fg_color="#f3f6fb")
    btn_frame.pack(fill="x", padx=16, pady=(8, 16))
    
    def update_category():
        try:
            if not name_entry.get() or not icon_entry.get():
                CTkMessagebox(title="Error", message="Please fill required fields")
                return
            
            run_command(
                "UPDATE CATEGORIES SET CAT_NAME=:1, ICON=:2, COLOR=:3, DESCRIPTION=:4 WHERE CAT_ID=:5",
                [name_entry.get(), icon_entry.get(), color_entry.get(), desc_entry.get(), cat_id]
            )
            
            CTkMessagebox(title="Success", message="Category updated!")
            overlay.destroy()
            _refresh_categories_page(parent, user_id)
        except Exception as e:
            CTkMessagebox(title="Error", message=str(e))
    
    ctk.CTkButton(btn_frame, text="Update Category", command=update_category, fg_color=PRIMARY, hover_color="#003d99", text_color="white", font=("Segoe UI", 12, "bold"), height=40, corner_radius=10, width=180).pack(side="right")
    ctk.CTkButton(btn_frame, text="Cancel", command=overlay.destroy, fg_color="#dfe3e8", hover_color="#d2d8de", text_color=TEXT_DARK, font=("Segoe UI", 12, "bold"), height=40, corner_radius=10, width=180).pack(side="right", padx=(0, 10))

def delete_category(user_id, cat_id, parent):
    """Delete a category"""
    response = CTkMessagebox(
        title="Delete",
        message="Are you sure? Expenses in this category will be affected.",
        icon="question",
        option_1="Yes",
        option_2="No"
    )
    
    if response.get() == "Yes":
        # Check if there are expenses
        expenses = run_query("SELECT COUNT(*) as cnt FROM EXPENSES WHERE CAT_ID=:1", [cat_id])
        if expenses and expenses[0]['CNT'] > 0:
            CTkMessagebox(title="Error", message="Cannot delete category with expenses")
            return
        
        run_command("DELETE FROM CATEGORIES WHERE CAT_ID=:1", [cat_id])
        CTkMessagebox(title="Success", message="Category deleted!")
        _refresh_categories_page(parent, user_id)
