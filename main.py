import customtkinter as ctk

from login_page import LoginPage
from main_page import MainPage
from members_page import MembersPage
from report_page import ReportPage
from online_books_page import OnlineBooksPage
from qr_code_window import QRCodePage # नवीन फाईल इंपोर्ट करा

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("📖 Library Management System")
        self.geometry("1100x700")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}
        
        self.frames["LoginPage"] = LoginPage(master=self, controller=self)
        self.frames["MainPage"] = MainPage(master=self, controller=self)
        self.frames["MembersPage"] = MembersPage(master=self, controller=self)
        self.frames["ReportPage"] = ReportPage(master=self, controller=self)
        self.frames["OnlineBooksPage"] = OnlineBooksPage(master=self, controller=self)
        self.frames["QRCodePage"] = QRCodePage(master=self, controller=self) # नवीन पेज जोडा
        
        for name, frame in self.frames.items():
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        if hasattr(frame, 'refresh_data'):
            frame.refresh_data()

if __name__ == "__main__":
    app = App()
    app.mainloop()