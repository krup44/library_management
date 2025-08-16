import customtkinter as ctk
from tkinter import messagebox
from db_manager import check_credentials

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        login_frame = ctk.CTkFrame(self, fg_color="transparent")
        login_frame.grid(row=0, column=0, padx=20, pady=20)
        
        ctk.CTkLabel(login_frame, text="🔑 Admin Login", font=("Segoe UI", 30, "bold")).pack(pady=(20, 10))

        ctk.CTkLabel(login_frame, text="Username").pack(pady=(10, 0))
        self.username_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter username")
        self.username_entry.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(login_frame, text="Password").pack(pady=(10, 0))
        self.password_entry = ctk.CTkEntry(login_frame, placeholder_text="Enter password", show="*")
        self.password_entry.pack(pady=5, padx=20, fill="x")

        ctk.CTkButton(login_frame, text="Login", command=self.login, width=200).pack(pady=20)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if check_credentials(username, password):
            messagebox.showinfo("Success", "Login Successful! 😊")
            self.controller.show_frame("MainPage")
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Invalid username or password. 😔")