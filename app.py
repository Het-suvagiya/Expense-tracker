import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from database import run_query, run_command
import dashboard
import expenses
import categories
import reports
import charts

ctk.set_default_color_theme("blue")

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

class MainApp(ctk.CTk):
    def __init__(self, user_id, full_name):
        try:
            super().__init__()
            
            self.user_id = user_id
            self.full_name = full_name
            
            # Window setup
            self.title("ExpenseDesk")
            self.geometry("1280x780")
            self.resizable(True, True)
            self.configure(fg_color=SURFACE)
            
            # Center on screen
            self.update_idletasks()
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            x = (screen_w - 1280) // 2
            y = (screen_h - 780) // 2
            self.geometry(f"1280x780+{x}+{y}")
            
            # Configure grid layout
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=0)
            self.grid_columnconfigure(1, weight=1)
            
            # Create sidebar
            self.create_sidebar()
            
            # Create main content area
            self.create_content_area()
            
            # Load dashboard by default
            self.load_page("Dashboard")
            
            print("MainApp initialized successfully")
        except Exception as e:
            print(f"Error initializing MainApp: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def create_sidebar(self):
        """Create the navigation sidebar"""
        sidebar = ctk.CTkFrame(self, width=240, fg_color=SIDEBAR_BG)
        sidebar.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        sidebar.grid_propagate(False)
        
        # Sidebar title
        title_label = ctk.CTkLabel(
            sidebar,
            text="ExpenseDesk",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT_DARK
        )
        title_label.pack(padx=20, pady=(24, 2))
        
        # Sidebar subtitle
        subtitle_label = ctk.CTkLabel(
            sidebar,
            text="Personal Finance",
            font=("Segoe UI", 10),
            text_color=TEXT_GRAY
        )
        subtitle_label.pack(padx=20, pady=(0, 20))
        
        # Navigation items
        nav_items = [
            ("📊", "Dashboard", "Dashboard"),
            ("💸", "Expenses", "Expenses"),
            ("📁", "Categories", "Categories"),
            ("📈", "Reports", "Reports"),
            ("📉", "Charts", "Charts")
        ]
        
        self.nav_buttons = {}
        
        for icon, label, page in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=f"{icon}  {label}",
                width=220,
                height=44,
                anchor="w",
                corner_radius=8,
                font=("Segoe UI", 13),
                fg_color="transparent",
                text_color=TEXT_GRAY,
                hover_color="#e8eaed",
                command=lambda p=page: self.load_page(p)
            )
            btn.pack(padx=10, pady=4)
            self.nav_buttons[page] = btn
        
        # Bottom separator
        separator = ctk.CTkFrame(sidebar, height=1, fg_color="#e0e3e5")
        separator.pack(padx=10, pady=20, fill="x")
        
        # Settings button
        settings_btn = ctk.CTkButton(
            sidebar,
            text="⚙  Settings",
            width=220,
            height=44,
            anchor="w",
            corner_radius=8,
            font=("Segoe UI", 13),
            fg_color="transparent",
            text_color=TEXT_GRAY,
            hover_color="#e8eaed",
            command=lambda: CTkMessagebox(title="Settings", message="Settings page coming soon!")
        )
        settings_btn.pack(padx=10, pady=4)
    
    def create_content_area(self):
        """Create the main content area"""
        content_column = ctk.CTkFrame(self, fg_color=SURFACE)
        content_column.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        content_column.grid_rowconfigure(1, weight=1)
        content_column.grid_columnconfigure(0, weight=1)
        
        # Top bar
        top_bar = ctk.CTkFrame(content_column, height=64, fg_color=CARD_BG)
        top_bar.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        top_bar.grid_propagate(False)
        top_bar.grid_columnconfigure(1, weight=1)
        
        # Page title
        self.page_title_label = ctk.CTkLabel(
            top_bar,
            text="Dashboard",
            font=("Segoe UI", 18, "bold"),
            text_color=TEXT_DARK
        )
        self.page_title_label.grid(row=0, column=0, padx=24, pady=12, sticky="w")
        
        
        # Main content frame (individual pages manage their own scrolling)
        self.content_frame = ctk.CTkFrame(
            content_column,
            fg_color=SURFACE
        )
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
    
    def load_page(self, page_name):
        """Load a page into the content area"""
        try:
            # Clear content frame
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # Update page title
            self.page_title_label.configure(text=page_name)
            
            # Update active button styling
            for btn_name, btn_widget in self.nav_buttons.items():
                if btn_name == page_name:
                    btn_widget.configure(
                        fg_color="#e8ecf5",
                        text_color=PRIMARY,
                        font=("Segoe UI", 13, "bold")
                    )
                else:
                    btn_widget.configure(
                        fg_color="transparent",
                        text_color=TEXT_GRAY,
                        font=("Segoe UI", 13)
                    )
            
            # Load page content
            if page_name == "Dashboard":
                dashboard.create_dashboard(self.content_frame, self.user_id)
            elif page_name == "Expenses":
                expenses.create_expenses_page(self.content_frame, self.user_id)
            elif page_name == "Categories":
                categories.create_categories_page(self.content_frame, self.user_id)
            elif page_name == "Reports":
                reports.create_reports_page(self.content_frame, self.user_id)
            elif page_name == "Charts":
                charts.create_charts_page(self.content_frame, self.user_id)
        except Exception as e:
            print(f"Error loading page {page_name}: {e}")
            import traceback
            traceback.print_exc()
            # Show error in content area
            error_label = ctk.CTkLabel(
                self.content_frame,
                text=f"Error loading {page_name}:\n{str(e)}",
                text_color=RED,
                font=("Segoe UI", 12)
            )
            error_label.pack(padx=20, pady=20)
    
    def logout(self):
        """Logout and return to login screen"""
        response = CTkMessagebox(
            title="Logout",
            message="Are you sure you want to logout?",
            icon="question",
            option_1="Yes",
            option_2="No"
        )
        
        if response.get() == "Yes":
            self.destroy()

if __name__ == "__main__":
    app = MainApp(1, "Admin User")
    app.mainloop()
