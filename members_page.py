import customtkinter as ctk
from tkinter import messagebox, ttk
from db_manager import get_members, add_member_db, update_member_db, delete_member_db

class MembersPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.selected_member_id = None

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

        self.create_members_management_ui(self.content_area)

    def create_members_management_ui(self, parent_frame):
        ctk.CTkLabel(parent_frame, text="🧑‍🤝‍🧑 Member Management", font=("Segoe UI", 24, "bold")).pack(pady=10)
        
        form = ctk.CTkFrame(parent_frame)
        form.pack(pady=10, fill="x", padx=10)
        self.name_var = ctk.StringVar()
        self.member_id_var = ctk.StringVar()
        ctk.CTkLabel(form, text="Member Name").grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkEntry(form, textvariable=self.name_var, width=150).grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(form, text="Member ID").grid(row=0, column=2, padx=5, pady=5)
        ctk.CTkEntry(form, textvariable=self.member_id_var, width=150).grid(row=0, column=3, padx=5, pady=5)

        btn_frame = ctk.CTkFrame(parent_frame)
        btn_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkButton(btn_frame, text="Add Member", command=self.add_member, fg_color="green").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Update Member", command=self.update_member, fg_color="orange").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Delete Member", command=self.delete_member, fg_color="red").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Refresh", command=self.refresh_data).pack(side="right", padx=5)

        self.members_tree = ttk.Treeview(parent_frame, columns=("ID", "Name", "Member ID"), show="headings")
        self.members_tree.pack(fill="x", padx=10, pady=10)
        for col in self.members_tree["columns"]:
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=100)
        self.members_tree.bind("<<TreeviewSelect>>", self.on_members_tree_select)

    def refresh_data(self):
        self.load_members()
        self.clear_member_form()

    def add_member(self):
        name = self.name_var.get()
        member_id = self.member_id_var.get()
        if not name or not member_id:
            messagebox.showwarning("Input Error", "All fields are required")
            return
        add_member_db(name, member_id)
        self.refresh_data()
        messagebox.showinfo("Success", "Member added successfully")

    def update_member(self):
        if not self.selected_member_id:
            messagebox.showwarning("Selection Error", "No member selected")
            return
        name = self.name_var.get()
        member_id = self.member_id_var.get()
        if not name or not member_id:
            messagebox.showwarning("Input Error", "All fields are required")
            return
        update_member_db(self.selected_member_id, name, member_id)
        self.refresh_data()
        messagebox.showinfo("Success", "Member updated successfully")

    def delete_member(self):
        if not self.selected_member_id:
            messagebox.showwarning("Selection Error", "No member selected")
            return
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this member?")
        if confirm:
            delete_member_db(self.selected_member_id)
            self.refresh_data()
            messagebox.showinfo("Deleted", "Member deleted successfully")

    def load_members(self):
        self.members_tree.delete(*self.members_tree.get_children())
        members = get_members()
        for member in members:
            self.members_tree.insert("", "end", values=(member['id'], member['name'], member['member_id']))

    def on_members_tree_select(self, event):
        selected = self.members_tree.selection()
        if selected:
            values = self.members_tree.item(selected[0], "values")
            self.selected_member_id = values[0]
            self.name_var.set(values[1])
            self.member_id_var.set(values[2])
        else:
            self.clear_member_form()
            self.selected_member_id = None

    def clear_member_form(self):
        self.name_var.set("")
        self.member_id_var.set("")