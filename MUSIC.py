from tkinter import *
from tkinter import messagebox, scrolledtext, ttk
import os, datetime

def open_main_menu():
    root = Tk()
    root.title("🎵 MusicLogger")
    root.geometry("350x350")
    root.configure(bg="#b30000")
    font = ("Helvetica", 12, "bold")

    Label(root, text="🎶 Welcome to MusicLogger 🎶", font=("Helvetica", 16, "bold"), bg="#b30000", fg="white").pack(pady=20)
    Button(root, text="🔐 Login", font=font, width=20, command=lambda: [root.destroy(), open_login_page()]).pack(pady=10)
    Button(root, text="📝 Register", font=font, width=20, command=lambda: [root.destroy(), open_register_page()]).pack(pady=10)

    Label(root, text="Quick Select User:", font=font, bg="#b30000", fg="white").pack(pady=10)
    user_list = Listbox(root, font=font, height=2)
    user_list.insert(END, "ibrahim")
    user_list.insert(END, "yousef")
    user_list.pack(pady=5)

    def on_user_select(event):
        try:
            selected = user_list.get(user_list.curselection())
            messagebox.showinfo("Selected", f"{selected} selected")
        except:
            pass

    user_list.bind("<<ListboxSelect>>", on_user_select)

    root.mainloop()

def open_register_page():
    root = Tk()
    root.title("Register")
    root.geometry("350x350")
    root.configure(bg="#b30000")
    font = ("Helvetica", 12, "bold")

    Label(root, text="📝 Register", font=("Helvetica", 16, "bold"), bg="#b30000", fg="white").pack(pady=10)

    Label(root, text="New Username", font=font, bg="#b30000", fg="white").pack()
    ent1 = Entry(root, font=font)
    ent1.pack(pady=5)

    Label(root, text="New Password", font=font, bg="#b30000", fg="white").pack()
    ent2 = Entry(root, show="*", font=font)
    ent2.pack(pady=5)

    lbl = Label(root, text="", bg="#b30000", fg="white", font=font)
    lbl.pack(pady=5)

    def register():
        u = ent1.get().strip()
        p = ent2.get().strip()
        if not u or not p:
            lbl.config(text="Fill all fields")
            return
        try:
            with open("user.txt", "r") as f:
                data = f.readlines()
        except FileNotFoundError:
            data = []
        for line in data:
            if line.startswith(f"{u},"):
                lbl.config(text="Username exists")
                return
        with open("user.txt", "a") as f:
            f.write(f"{u},{p}\n")
        lbl.config(text="Registered successfully")
        ent1.delete(0, END)
        ent2.delete(0, END)

    Button(root, text="Register", font=font, width=15, command=register).pack(pady=5)
    Button(root, text="⬅ Back", font=font, command=lambda: [root.destroy(), open_main_menu()]).pack()

    root.mainloop()

def open_song_window(username):
    root = Tk()
    root.title("🎵 Music Page")
    root.geometry("700x550")
    root.configure(bg="#b30000")
    font = ("Helvetica", 12, "bold")

    Label(root, text=f"Welcome {username}", font=("Helvetica", 16, "bold"), bg="#b30000", fg="white").pack(pady=10)

    Label(root, text="Title", font=font, bg="#b30000", fg="white").pack()
    song_ent = Entry(root, font=font)
    song_ent.pack()

    Label(root, text="Artist", font=font, bg="#b30000", fg="white").pack()
    artist_ent = Entry(root, font=font)
    artist_ent.pack()

    Label(root, text="Genre", font=font, bg="#b30000", fg="white").pack()
    genre_box = ttk.Combobox(root, values=["Pop", "Rap", "Rock", "Trap", "Lo-fi"], font=font)
    genre_box.pack()

    Label(root, text="Why you like it?", font=font, bg="#b30000", fg="white").pack()
    reason_txt = scrolledtext.ScrolledText(root, width=50, height=4, font=font)
    reason_txt.pack()

    def save_song():
        title = song_ent.get().strip()
        artist = artist_ent.get().strip()
        genre = genre_box.get().strip()
        reason = reason_txt.get("1.0", END).strip()
        date = str(datetime.date.today())

        if not title or not artist or not genre or not reason:
            messagebox.showerror("Error", "Fill all fields")
            return

        file = f"songs_{username}.txt"
        with open(file, "a", encoding="utf-8") as f:
            f.write(f"Title: {title}\n")
            f.write(f"Artist: {artist}\n")
            f.write(f"Genre: {genre}\n")
            f.write(f"Reason: {reason}\n")
            f.write(f"Date: {date}\n")
            f.write("---\n")

        song_ent.delete(0, END)
        artist_ent.delete(0, END)
        genre_box.set("")
        reason_txt.delete("1.0", END)
        messagebox.showinfo("Saved", "Song saved!")

    Button(root, text="💾 Save", font=font, command=save_song).pack(pady=5)
    Button(root, text="📃 View/Search", font=font, command=lambda: [root.destroy(), open_view_search_window(username)]).pack(pady=5)

    root.mainloop()

def open_view_search_window(username):
    root = Tk()
    root.title("📃 View Songs")
    root.geometry("700x650")
    root.configure(bg="#b30000")
    font = ("Helvetica", 12, "bold")

    Label(root, text="Search by Artist", font=font, bg="#b30000", fg="white").pack(pady=5)
    search_ent = Entry(root, font=font)
    search_ent.pack(pady=5)

    def search_artist():
        name = search_ent.get().strip().lower()
        result = ""
        block = ""
        file = f"songs_{username}.txt"
        if not name:
            messagebox.showerror("Error", "Enter artist name")
            return
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip() == "---":
                        if f"artist: {name}" in block.lower():
                            result += block + "---\n"
                        block = ""
                    else:
                        block += line
        box.config(state="normal")
        box.delete("1.0", END)
        box.insert(END, result if result else "No results")
        box.config(state="disabled")

    Button(root, text="🔍 Search", font=font, command=search_artist).pack(pady=5)

    box = scrolledtext.ScrolledText(root, width=80, height=20, font=font)
    box.pack(pady=10)
    box.config(state="disabled")

    def view_all():
        file = f"songs_{username}.txt"
        box.config(state="normal")
        box.delete("1.0", END)
        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                box.insert(END, f.read())
        else:
            box.insert(END, "No songs yet")
        box.config(state="disabled")

    Button(root, text="📂 Show All", font=font, command=view_all).pack(pady=5)
    Button(root, text="⬅ Back", font=font, command=lambda: [root.destroy(), open_song_window(username)]).pack(pady=5)

    root.mainloop()

open_main_menu()
