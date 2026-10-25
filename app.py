import tkinter as tk
from itertools import cycle
from pathlib import Path
import webbrowser

from PIL import Image, ImageTk

from discourse import DiscourseDatabase

INTRO_STR = """
Foczka Hackerspace Trójmiasto znów potrzebuje Twojej pomocy!
Znalazła wpisy w bazie zasobów Hackerspace Trójmiasto, którym
brakuje kluczowych informacji.

Uzupełnij znalezione przez foczkę wpisy o brakujące zdjęcia, miejsca
i popraw błędy w formatowaniu Markdown.
"""

BG_COLOR = "white"

def display_header_img(parent, img_path: str):
    with Image.open(Path(img_path)) as image:
        photo = ImageTk.PhotoImage(image)
    label = tk.Label(parent, image=photo, bg=BG_COLOR)
    label.image = photo
    label.pack()

def display_paragraph(parent, text: str):
    label = tk.Label(
        parent,
        text=text,
        bg=BG_COLOR,
        font=("Helvetica", 18),
        wraplength=740,
    )
    label.pack(padx=20, pady=10)
    return label

def clear_parent(parent):
    for child in parent.winfo_children():
        child.destroy()

def get_button(parent, text: str, command):
    return tk.Button(
        parent,
        text=text,
        font=("Helvetica", 18),
        command=command
    )

def initialize_game_mode(parent, db, tag: str):
    clear_parent(parent)
    paragraph = display_paragraph(
        parent,
        "Foczka znalazła posty, którym brakuje zdjęć! Znajdź te zasoby, zrób im zdjęcie i uzupełnij te posty. 📸",
    )
    img_posts = db.get_tag_data(tag)
    posts = img_posts["topic_list"]["topics"]
    resource_frame = tk.Frame(parent, bg=BG_COLOR)
    resource_frame.pack(fill="x", padx=20, pady=20)
    buttons = []
    for post in posts:
        url = f'https://kb.hs3.pl/t/{post["id"]}'
        button = get_button(resource_frame,post["fancy_title"], lambda url=url: webbrowser.open_new(url))
        buttons.append(button)
    button_cycle = cycle(buttons)
    current_button = None

    def show_next():
        nonlocal current_button
        if current_button is not None:
            current_button.pack_forget()
        current_button = next(button_cycle)
        current_button.pack(fill="x")
    next_button = get_button(parent, "Pomagam dalej :)", show_next)
    next_button.pack()

    if buttons:
        show_next()
    else:
        paragraph.config(text="Wszystko gotowe, foczka jest szczęśliwa!")
        next_button.config(state=tk.DISABLED)

def display_intro(parent):
    clear_parent(parent)
    display_header_img(parent, "assets/foczka.jpg")
    display_paragraph(parent, INTRO_STR)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("0h hackathon")
    root.geometry("800x800+50+50")
    root.configure(bg=BG_COLOR)

    display_intro(root)

    db = DiscourseDatabase()

    get_button(
        root,
        "chcę robić zdjęcia",
        lambda: initialize_game_mode(root, db, "img-needed"),
    ).pack()
    
    root.mainloop()
