import tkinter as tk
from itertools import cycle
from pathlib import Path
import webbrowser

from PIL import Image, ImageTk

from discourse import DiscourseDatabase, DISCOURSE_URL

INTRO_STR = """
Foczka Hackerspace Trójmiasto znów potrzebuje Twojej pomocy!
Znalazła wpisy w bazie zasobów Hackerspace Trójmiasto, którym
brakuje kluczowych informacji.

Wybierz tryb gry (co chcesz poprawić):
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

def initialize_game_mode(parent, db, tag: str, description: str, img_path: str):
    clear_parent(parent)
    display_header_img(parent, img_path)
    paragraph = display_paragraph(
        parent,
        description,
    )
    img_posts = db.get_tag_data(tag)
    posts = img_posts["topic_list"]["topics"]
    resource_frame = tk.Frame(parent, bg=BG_COLOR)
    resource_frame.pack(fill="x", padx=20, pady=20)
    buttons = []
    for post in posts:
        url = f'{DISCOURSE_URL}/t/{post["id"]}'
        button = get_button(resource_frame,post["title"], lambda url=url: webbrowser.open_new(url))
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
    get_button(
        parent,
        "Kończymy, wracam do początku",
        lambda: display_intro(parent, db),
    ).pack()
    next_button.pack()

    if buttons:
        show_next()
    else:
        paragraph.config(text="Wszystko gotowe, foczka jest szczęśliwa!")
        next_button.config(state=tk.DISABLED)

def display_intro(parent, db):
    clear_parent(parent)
    display_header_img(parent, "assets/foczka.jpg")
    display_paragraph(parent, INTRO_STR)
    img_mode_intro = "Foczka znalazła posty, którym brakuje zdjęć! Znajdź te zasoby, zrób im zdjęcie i uzupełnij te posty. 📸"
    place_mode_intro = "Czas zabawić się w detektywa. 🐾 Foczka znalazła posty, które mają nieprawidłowe lub brakujące miejsce. Znajdź gdzie dany przedmiot się ukrywa i uzupełnij je."
    md_mode_intro = "Foczka znalazła posty, które mają błędy w formatowaniu Markdown. Pomóż jej proszę, płetwami ciężko wyklikuje się klawiaturę. :<"
    get_button(
        parent,
        "chcę robić zdjęcia",
        lambda: initialize_game_mode(
            parent, db, "img-needed", img_mode_intro, "assets/foczka_img.jpg"
        ),
    ).pack()

    get_button(
        parent,
        "chcę szukać zasobów",
        lambda: initialize_game_mode(
            parent, db, "fix-place", place_mode_intro, "assets/foczka_place.jpg"
        ),
    ).pack()

    get_button(
        parent,
        "chcę naprawiać formatowanie",
        lambda: initialize_game_mode(
            parent, db, "fix-markdown", md_mode_intro, "assets/foczka_md.jpg"
        ),
    ).pack()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("0h hackathon")
    root.geometry("800x800+50+50")
    root.configure(bg=BG_COLOR)

    db = DiscourseDatabase()
    display_intro(root, db)

    root.mainloop()
