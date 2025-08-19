import customtkinter as ctk
from book_manager import get_books
from db_manager import get_members, get_borrowed_books

class ReportPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="📖 Library", font=("Segoe UI", 24)).grid(row=0, column=0, padx=20, pady=20)
        
        ctk.CTkButton(self.sidebar_frame, text="Book Management", command=lambda: self.controller.show_frame("MainPage")).grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar_frame, text="Member Management", command=lambda: self.controller.show_frame("MembersPage")).grid(row=2, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar_frame, text="QR Code Generator", command=lambda: self.controller.show_frame("QRCodePage")).grid(row=3, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar_frame, text="Online Books", command=lambda: self.controller.show_frame("OnlineBooksPage")).grid(row=4, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar_frame, text="Reports", command=lambda: self.controller.show_frame("ReportPage")).grid(row=5, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar_frame, text="Logout", command=lambda: self.controller.show_frame("LoginPage"), fg_color="red").grid(row=6, column=0, padx=20, pady=10)
        
        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)
        
        self.create_reports_ui(self.content_area)

    def create_reports_ui(self, parent_frame):
        ctk.CTkLabel(parent_frame, text="📊 Reports", font=("Segoe UI", 24, "bold")).pack(pady=10)
        
        report_frame = ctk.CTkFrame(parent_frame)
        report_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.book_count_label = ctk.CTkLabel(report_frame, text="", font=("Segoe UI", 16))
        self.book_count_label.pack(pady=5)
        self.member_count_label = ctk.CTkLabel(report_frame, text="", font=("Segoe UI", 16))
        self.member_count_label.pack(pady=5)
        self.borrowed_count_label = ctk.CTkLabel(report_frame, text="", font=("Segoe UI", 16))
        self.borrowed_count_label.pack(pady=5)
        
        ctk.CTkButton(report_frame, text="Refresh Report", command=self.refresh_data).pack(pady=20)
    
    def refresh_data(self):
        books = get_books()
        members = get_members()
        borrowed_books = get_borrowed_books()
        
        self.book_count_label.configure(text=f"Total Books: {len(books)}")
        self.member_count_label.configure(text=f"Total Members: {len(members)}")
        self.borrowed_count_label.configure(text=f"Total Borrowed Books: {len(borrowed_books)}")