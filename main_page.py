
import customtkinter as ctk
from tkinter import messagebox, ttk
from book_manager import get_books, add_book, update_book, delete_book
from db_manager import get_members, get_borrowed_books, borrow_book_db, return_book_db, is_book_borrowed_db
from datetime import datetime
from tkcalendar import Calendar
import qrcode
from PIL import Image, ImageTk
import os

class MainPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.selected_book_id = None
        self.selected_borrow_id = None
        self.member_list = {}
        self.qr_code_label = None

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

        self.create_book_management_ui(self.content_area)

    def create_book_management_ui(self, parent_frame):
        ctk.CTkLabel(parent_frame, text="📚 Book Management", font=("Segoe UI", 24, "bold")).pack(pady=10)
        form = ctk.CTkFrame(parent_frame)
        form.pack(pady=10, fill="x", padx=10)
        self.title_var = ctk.StringVar()
        self.author_var = ctk.StringVar()
        self.year_var = ctk.StringVar()
        self.isbn_var = ctk.StringVar()
        
        ctk.CTkLabel(form, text="Title").grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkEntry(form, textvariable=self.title_var, width=150).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(form, text="Author").grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkEntry(form, textvariable=self.author_var, width=150).grid(row=0, column=3, padx=5, pady=5)
        ctk.CTkLabel(form, text="Year").grid(row=0, column=4, padx=5, pady=5)
        ctk.CTkEntry(form, textvariable=self.year_var, width=80).grid(row=0, column=5, padx=5, pady=5)
        ctk.CTkLabel(form, text="ISBN").grid(row=0, column=6, padx=5, pady=5)
        ctk.CTkEntry(form, textvariable=self.isbn_var, width=120).grid(row=0, column=7, padx=5, pady=5)

        btn_frame = ctk.CTkFrame(parent_frame)
        btn_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkButton(btn_frame, text="Add Book", command=self.add_book, fg_color="green").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Update Book", command=self.update_book, fg_color="orange").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Delete Book", command=self.delete_book, fg_color="red").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Generate QR Code", command=self.generate_qr_code).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Refresh", command=self.refresh_data).pack(side="right", padx=5)
        
        # QR Code display frame
        self.qr_code_frame = ctk.CTkFrame(parent_frame)
        self.qr_code_frame.pack(pady=10)
        self.qr_code_label = ctk.CTkLabel(self.qr_code_frame, text="", fg_color="transparent")
        self.qr_code_label.pack(padx=10, pady=10)

        self.books_tree = ttk.Treeview(parent_frame, columns=("ID", "Title", "Author", "Year", "ISBN"), show="headings")
        self.books_tree.pack(fill="x", padx=10, pady=10)
        for col in self.books_tree["columns"]:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=100)
        self.books_tree.bind("<<TreeviewSelect>>", self.on_books_tree_select)

        # Borrow/Return Frame setup
        borrow_frame = ctk.CTkFrame(parent_frame)
        borrow_frame.pack(pady=10, fill="x", padx=10)
        ctk.CTkLabel(borrow_frame, text="Borrow/Return Books", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=5, pady=(0, 10))
        
        ctk.CTkLabel(borrow_frame, text="Select Member").grid(row=1, column=0, padx=5, pady=5)
        self.member_combo = ctk.CTkComboBox(borrow_frame, values=["(Select Member)"], state="readonly")
        self.member_combo.grid(row=1, column=1, padx=5, pady=5)
        
        ctk.CTkLabel(borrow_frame, text="Return Date").grid(row=1, column=2, padx=5, pady=5)
        self.return_date_entry = ctk.CTkEntry(borrow_frame, placeholder_text="YYYY-MM-DD", width=120)
        self.return_date_entry.grid(row=1, column=3, padx=5, pady=5)
        
        ctk.CTkButton(borrow_frame, text="Open Calendar", command=self.open_calendar).grid(row=1, column=4, padx=5, pady=5)
        ctk.CTkButton(borrow_frame, text="Borrow Book", command=self.borrow_book).grid(row=2, column=0, padx=5, pady=5)
        ctk.CTkButton(borrow_frame, text="Return/Delete Borrowed Book", command=self.return_book, fg_color="red").grid(row=2, column=1, padx=5, pady=5)

        self.calendar = Calendar(borrow_frame, selectmode='day', date_pattern='yyyy-mm-dd',
                                 command=self.select_date)
        
        ctk.CTkLabel(parent_frame, text="Borrowed Books", font=("Segoe UI", 16, "bold")).pack(pady=(10, 0))
        self.borrowed_tree = ttk.Treeview(parent_frame, columns=("ID", "Book Title", "Member Name", "Borrow Date", "Return Date"), show="headings")
        self.borrowed_tree.pack(fill="x", padx=10, pady=10)
        for col in self.borrowed_tree["columns"]:
            self.borrowed_tree.heading(col, text=col)
            self.borrowed_tree.column(col, width=100)
        self.borrowed_tree.bind("<<TreeviewSelect>>", self.on_borrowed_tree_select)
    
    def refresh_data(self):
        self.load_books()
        self.load_borrowed_books()
        self.load_members_to_combo()
        self.clear_book_form()
        self.return_date_entry.delete(0, 'end')
        self.selected_borrow_id = None
        # Hide the QR code when refreshing the data
        if self.qr_code_label:
            self.qr_code_label.configure(image=None, text="")

    def add_book(self):
        if not self.title_var.get() or not self.author_var.get():
            messagebox.showwarning("Input Error", "Title and Author are required")
            return
        book_data = {
            "title": self.title_var.get(),
            "author": self.author_var.get(),
            "year": self.year_var.get(),
            "isbn": self.isbn_var.get()
        }
        add_book(book_data)
        self.refresh_data()
        messagebox.showinfo("Success", "Book added successfully")

    def update_book(self):
        if not self.selected_book_id:
            messagebox.showwarning("Selection Error", "No book selected")
            return
        book_data = {
            "title": self.title_var.get(),
            "author": self.author_var.get(),
            "year": self.year_var.get(),
            "isbn": self.isbn_var.get(),
        }
        update_book(self.selected_book_id, book_data)
        self.refresh_data()
        messagebox.showinfo("Success", "Book updated successfully")

    def delete_book(self):
        if not self.selected_book_id:
            messagebox.showwarning("Selection Error", "No book selected")
            return
        if is_book_borrowed_db(self.selected_book_id):
            messagebox.showwarning("Deletion Error", "Cannot delete a book that is currently borrowed.")
            return
        
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?")
        if confirm:
            delete_book(self.selected_book_id)
            self.refresh_data()
            messagebox.showinfo("Deleted", "Book deleted successfully")

    def load_books(self):
        self.books_tree.delete(*self.books_tree.get_children())
        books = get_books()
        for book in books:
            self.books_tree.insert("", "end", values=(book['id'], book['title'], book['author'], book['year'], book['isbn']))

    def on_books_tree_select(self, event):
        selected = self.books_tree.selection()
        if selected:
            values = self.books_tree.item(selected[0], "values")
            self.selected_book_id = values[0]
            self.title_var.set(values[1])
            self.author_var.set(values[2])
            self.year_var.set(values[3])
            self.isbn_var.set(values[4])
        else:
            self.clear_book_form()
            self.selected_book_id = None
        # Hide the QR code when a new book is selected or deselected
        if self.qr_code_label:
            self.qr_code_label.configure(image=None, text="")


    def clear_book_form(self):
        self.title_var.set("")
        self.author_var.set("")
        self.year_var.set("")
        self.isbn_var.set("")
        self.selected_book_id = None

    def load_members_to_combo(self):
        members = get_members()
        self.member_list = {row['name']: row['id'] for row in members}
        self.member_combo.configure(values=["(Select Member)"] + list(self.member_list.keys()))
        self.member_combo.set("(Select Member)")

    def open_calendar(self):
        if self.calendar.winfo_ismapped():
            self.calendar.grid_forget()
        else:
            self.calendar.grid(row=2, column=2, columnspan=3, padx=5, pady=5)
            
    def select_date(self, date_string):
        self.return_date_entry.delete(0, 'end')
        self.return_date_entry.insert(0, date_string)
        self.calendar.grid_forget()

    def generate_qr_code(self):
        if not self.selected_book_id:
            messagebox.showwarning("Selection Error", "Please select a book to generate a QR code.")
            return
        
        # Get book data for QR code content
        selected_book_values = self.books_tree.item(self.books_tree.selection()[0], "values")
        book_id, title, author, year, isbn = selected_book_values
        
        # Create a string with book information
        qr_data = f"Book ID: {book_id}\nTitle: {title}\nAuthor: {author}\nYear: {year}\nISBN: {isbn}"
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert PIL Image to CustomTkinter Image and display
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(150, 150))
        self.qr_code_label.configure(image=ctk_img, text="QR Code for Selected Book", compound="top")


    def borrow_book(self):
        if not self.selected_book_id:
            messagebox.showwarning("Input Error", "Please select a book to borrow.")
            return
        member_name = self.member_combo.get()
        if member_name == "(Select Member)":
            messagebox.showwarning("Input Error", "Please select a member.")
            return
        
        member_id = self.member_list.get(member_name)
        if is_book_borrowed_db(self.selected_book_id):
            messagebox.showwarning("Borrowing Error", "This book is already borrowed.")
            return
        
        return_date = self.return_date_entry.get()
        if not return_date:
            messagebox.showwarning("Input Error", "Please select a return date.")
            return

        borrow_book_db(self.selected_book_id, member_id, return_date)
        self.refresh_data()
        messagebox.showinfo("Success", f"Book borrowed by {member_name} successfully.")

    def return_book(self):
        if not self.selected_borrow_id:
            messagebox.showwarning("Input Error", "Please select a borrowed book to return.")
            return

        confirm = messagebox.askyesno("Confirm Return", "Are you sure you want to return this book?")
        if confirm:
            return_book_db(self.selected_borrow_id)
            self.refresh_data()
            messagebox.showinfo("Success", "Book returned successfully.")

    def load_borrowed_books(self):
        self.borrowed_tree.delete(*self.borrowed_tree.get_children())
        rows = get_borrowed_books()
        for row in rows:
            self.borrowed_tree.insert("", "end", values=row)

    def on_borrowed_tree_select(self, event):
        selected = self.borrowed_tree.selection()
        if selected:
            # Correctly set the selected borrow ID without trying to populate the book form
            values = self.borrowed_tree.item(selected[0], "values")
            self.selected_borrow_id = values[0]
        else:
            self.selected_borrow_id = None
        # Hide the QR code when a new book is selected or deselected
        if self.qr_code_label:
            self.qr_code_label.configure(image=None, text="")