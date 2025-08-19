import customtkinter as ctk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
from book_manager import get_books

class QRCodePage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.qr_code_label = None
        self.selected_book_data = None

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Sidebar frame (Navigation Bar)
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
        
        # Main content area
        self.content_area = ctk.CTkFrame(self, fg_color="transparent")
        self.content_area.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        self.create_qr_code_ui(self.content_area)

    def create_qr_code_ui(self, parent_frame):
        ctk.CTkLabel(parent_frame, text="Generate QR Code", font=("Segoe UI", 24, "bold")).pack(pady=10)
        
        # Dropdown to select a book
        self.book_combobox = ctk.CTkComboBox(parent_frame, values=["(Select a Book)"], state="readonly", command=self.on_book_select)
        self.book_combobox.pack(pady=10)
        
        # QR Code display area
        self.qr_code_frame = ctk.CTkFrame(parent_frame)
        self.qr_code_frame.pack(pady=10)
        
        self.qr_code_label = ctk.CTkLabel(self.qr_code_frame, text="", fg_color="transparent")
        self.qr_code_label.pack(padx=10, pady=10)
        
        self.refresh_data()

    def refresh_data(self):
        self.books = get_books()
        book_titles = [f"{book['title']} by {book['author']}" for book in self.books]
        self.book_combobox.configure(values=["(Select a Book)"] + book_titles)
        self.book_combobox.set("(Select a Book)")
        self.qr_code_label.configure(text="")
        self.qr_code_label.configure(image=None)
        self.selected_book_data = None

    def on_book_select(self, choice):
        if choice == "(Select a Book)":
            self.selected_book_data = None
            self.qr_code_label.configure(image=None, text="Please select a book to generate QR code.")
            return

        selected_book = next((book for book in self.books if f"{book['title']} by {book['author']}" == choice), None)
        if selected_book:
            self.selected_book_data = selected_book
            self.generate_qr_code()

    def generate_qr_code(self):
        if not self.selected_book_data:
            messagebox.showwarning("Selection Error", "Please select a book to generate a QR code.")
            return
        
        book_id, title, author, year, isbn = self.selected_book_data['id'], self.selected_book_data['title'], self.selected_book_data['author'], self.selected_book_data['year'], self.selected_book_data['isbn']
        
        qr_data = f"Book ID: {book_id}\nTitle: {title}\nAuthor: {author}\nYear: {year}\nISBN: {isbn}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        ctk_img = ctk.CTkImage(light_image=img.convert('RGB'), dark_image=img.convert('RGB'), size=(250, 250))
        self.qr_code_label.configure(image=ctk_img, text="QR Code for Selected Book", compound="top")