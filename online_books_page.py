import customtkinter as ctk
import webbrowser
import urllib.parse

class OnlineBooksPage(ctk.CTkFrame):
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
        self.content_area.grid_rowconfigure(2, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self.content_area, text="🌐 Online Books Search", font=("Segoe UI", 24, "bold")).grid(row=0, column=0, pady=10)
        
        search_frame = ctk.CTkFrame(self.content_area)
        search_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Search for online books on Google...")
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=10)
        
        search_button = ctk.CTkButton(search_frame, text="Search", command=self.search_online_books)
        search_button.grid(row=0, column=1, padx=(0, 10), pady=10)

        online_books_frame = ctk.CTkScrollableFrame(self.content_area)
        online_books_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

        # Hardcoded list of books from Project Gutenberg
        books = [
            ("Pride and Prejudice", "Jane Austen", "https://www.gutenberg.org/ebooks/1342"),
            ("The Adventures of Sherlock Holmes", "Arthur Conan Doyle", "https://www.gutenberg.org/ebooks/1661"),
            ("Frankenstein", "Mary Shelley", "https://www.gutenberg.org/ebooks/84"),
            ("Moby Dick", "Herman Melville", "https://www.gutenberg.org/ebooks/2701"),
            ("Alice's Adventures in Wonderland", "Lewis Carroll", "https://www.gutenberg.org/ebooks/11"),
            ("A Christmas Carol", "Charles Dickens", "https://www.gutenberg.org/ebooks/46")
        ]

        for i, (title, author, link) in enumerate(books):
            book_frame = ctk.CTkFrame(online_books_frame)
            book_frame.pack(fill="x", padx=10, pady=5)
            
            ctk.CTkLabel(book_frame, text=f"{title}", font=("Segoe UI", 16, "bold")).pack(side="left", padx=10)
            ctk.CTkLabel(book_frame, text=f"by {author}", font=("Segoe UI", 14)).pack(side="left", padx=5)
            
            read_button = ctk.CTkButton(book_frame, text="Read Online", command=lambda url=link: webbrowser.open_new(url))
            read_button.pack(side="right", padx=10)

    def search_online_books(self):
        query = self.search_entry.get()
        if query:
            # URL-encode the search query
            encoded_query = urllib.parse.quote_plus(f"read {query} online free")
            google_url = f"https://www.google.com/search?q={encoded_query}"
            webbrowser.open_new_tab(google_url)
        else:
            messagebox.showwarning("Search Error", "Please enter a search query.")