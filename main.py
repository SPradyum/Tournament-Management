import customtkinter as ctk
from ui import TournamentManagerUI

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Multi-Sport Tournament Manager")
    app.geometry("1200x700")
    app.resizable(False, False)

    TournamentManagerUI(app)
    app.mainloop()

if __name__ == "__main__":
    main()
