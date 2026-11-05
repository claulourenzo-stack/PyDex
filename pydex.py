'''
#Description: Python-based Pokedex with a graphical interface (tkinter) to help pokemon trainers organize and manage their collections.
#Purpose: To apply programming concepts learned in CSC 1301K to develop an interactive Pokemon collection system.
# Concepts learned in CSC 1301K: Functions, user input, dictionaries, sets, conditional statements, and loops.
#Date: October 30, 2026 - November 02, 2026
#Program: PyDex - Pokemon Collection Management System (GUI version)
#Author: Claudia Lourenco Barroso
#Course: CSC 1301K - Principles of Computer Science I - Dr Liu
#Institution: Georgia State University, perimeter.
#Email: clourencobarroso1@student.gsu.edu
#Version: 2.0 (tkinter)
'''
import tkinter as tk
from tkinter import ttk, messagebox
import json
from urllib.request import Request, urlopen
from PIL import Image, ImageTk
from io import BytesIO
# Store downloaded Pokemon images
pokemon_images = {}
# POKEMON DATABASE
# Concept: Dictionaries and loops
# Purpose: Store the name and Pokedex number of our starter Pokemon.
#This will load the original 151 Kanto Pokemon.
url = "https://pokeapi.co/api/v2/pokemon?limit=151&offset=0"
request = Request(
    url,
    headers={"User-Agent": "PyDex/2.0"}
)
with urlopen(request, timeout=15) as response:
    data = json.load(response)
pokemon = {}
for number, item in enumerate(data["results"], start=1):
    name = item["name"].capitalize()
    pokemon[name] = number
print("Pokemon loaded:", len(pokemon))
# POKEMON COLLECTION - Sets
# Use my_collection.add to add more pokemons the user caught.
my_collection = {"Pikachu", "Bulbasaur"}
# ---------- COLORS / FONTS ----------
PURPLE = "#39245F"
DARK_PURPLE = "#25163F"
LIGHT_PURPLE = "#EDE7F6"
WHITE = "#FFFFFF"
LIGHT = "#F8F6FC"
YELLOW = "#FFCB05"
BLUE = "#2A75BB"
FONT_TITLE = ("Helvetica", 22, "bold")
FONT_SUB = ("Helvetica", 14)
FONT_TEXT = ("Helvetica", 12)
FONT_BTN = ("Helvetica", 12, "bold")
root = tk.Tk()
root.title("PyDex - Pokemon Collection Management System by Claudia Lourenco Barroso")
root.geometry("760x480")
root.resizable(False, False)
root.configure(bg=PURPLE)
# Frames (screens)
welcome_frame = tk.Frame(root, bg=PURPLE)
main_frame = tk.Frame(root, bg=PURPLE)
# Right-side panel of the main menu, where each option shows its content
content = None
# ---------- HELPER FUNCTIONS ----------
def clear_content():
# Remove everything from the content panel before showing a new screen
    for widget in content.winfo_children():
        widget.destroy()
def make_title(text):
    tk.Label(content, text=text, font=FONT_TITLE, bg=LIGHT, fg=PURPLE).pack(pady=(20, 10))

# FUNCTION: load_pokemon_image()
# Purpose: Download and display Pokemon artwork.
# Concepts: Functions, dictionaries, and conditional statements.
def load_pokemon_image(number):
# Check if the image was already downloaded
    if number in pokemon_images:
        return pokemon_images[number]
    # Get the Pokemon artwork from PokeAPI
    url = (
        "https://raw.githubusercontent.com/PokeAPI/sprites/"
        "master/sprites/pokemon/other/official-artwork/"
        + str(number) + ".png"
    )
    try:
        with urlopen(url, timeout=10) as response:
            image_data = response.read()
        image = Image.open(BytesIO(image_data))
        image = image.convert("RGBA")
        image.thumbnail((130, 130))
        photo = ImageTk.PhotoImage(image)
    # Save the image in our dictionary
        pokemon_images[number] = photo
        return photo
    except Exception as error:
        print("ERROR LOADING POKEMON IMAGE:", error)
        return None

# FUNCTION: search_pokemon()
# Purpose: Search Pokemon by name and display its artwork.
# Concepts: Functions, dictionaries, conditionals, and user input.
def search_pokemon():
    clear_content()
    make_title("POKEMON SEARCH")
    tk.Label(
        content,
        text="Enter Pokemon name:",
        font=FONT_TEXT,
        bg=LIGHT
    ).pack()
    entry = tk.Entry(
        content,
        font=FONT_SUB,
        justify="center",
        width=20
    )
    entry.pack(pady=5)
    entry.focus()
    result = tk.Label(
        content,
        text="",
        font=FONT_TEXT,
        bg=LIGHT
    )
    result.pack(pady=5)
    # Label for Pokemon artwork
    image_label = tk.Label(content, bg=LIGHT)
    image_label.pack(pady=5)
    def do_search(event=None):
        name = entry.get().strip().capitalize()
    # Clear previous image
        image_label.config(image="")
        image_label.image = None
        if name in pokemon:
            number = pokemon[name]
            if name in my_collection:
                in_col = "Yes"
            else:
                in_col = "No"
            result.config(
                text=f"Pokemon found!\n"
                     f"Name: {name}\n"
                     f"Pokedex Number: #{number:03d}\n"
                     f"In your collection: {in_col}",
                fg="green"
            )
    # Download and display Pokemon artwork
            photo = load_pokemon_image(number)
            if photo is not None:
                image_label.config(image=photo)
                image_label.image = photo
            else:
                print("Could not load image for:", name)
        else:
            result.config(
                text="Oh no! Pokemon not found!",
                fg=PURPLE
            )
    tk.Button(
        content,
        text="Search",
        font=FONT_BTN,
        bg=BLUE,
        fg=WHITE,
        width=12,
        command=do_search
    ).pack(pady=5)
    entry.bind("<Return>", do_search)

# FUNCTION: show_collection()
# Purpose: Display all collected Pokemon in a scrollable list.
def show_collection():
    clear_content()
    make_title("MY COLLECTION")
    tk.Label(
        content,
        text=f"Pokemon collected: {len(my_collection)}",
        font=FONT_SUB,
        bg=LIGHT
    ).pack(pady=5)
    # Create a frame for the list and scrollbar
    list_frame = tk.Frame(content, bg=LIGHT)
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)
    # Create a scrollbar
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")
    # Display the Pokemon collection
    listbox = tk.Listbox(
        list_frame,
        font=FONT_TEXT,
        yscrollcommand=scrollbar.set
    )
    listbox.pack(side="left", fill="both", expand=True)
    # Connect the scrollbar to the list
    scrollbar.config(command=listbox.yview)
    # Add collected Pokemon to the list
    for name in sorted(my_collection):
        listbox.insert(tk.END, f"#{pokemon[name]:03d}  {name}")

# FUNCTION: catch_pokemon()
# Purpose: Add a pokemon to the collection.
def catch_pokemon():
    clear_content()
    make_title("CATCH A POKEMON")
    tk.Label(content, text="Which Pokemon would you like to catch?",
             font=FONT_TEXT, bg=LIGHT).pack()
    entry = tk.Entry(content, font=FONT_SUB, justify="center", width=20)
    entry.pack(pady=8)
    entry.focus()
    result = tk.Label(content, text="", font=FONT_SUB, bg=LIGHT)
    result.pack(pady=15)
    def do_catch(event=None):
        name = entry.get().strip().capitalize()
        if name in pokemon:
            if name in my_collection:
                result.config(text=f"You already have {name}!", fg=BLUE)
            else:
                my_collection.add(name)
                result.config(text=f"{name} was added to your collection!", fg="green")
        else:
            result.config(text="Oh no! Pokemon not found!", fg=PURPLE)
        entry.delete(0, tk.END)
    tk.Button(content, text="Catch!", font=FONT_BTN, bg=BLUE, fg=WHITE,
              width=12, command=do_catch).pack()
    entry.bind("<Return>", do_catch)

# FUNCTION: missing_pokemon()
# Purpose: Show the pokemon that are still missing (set difference).
def missing_pokemon():
    clear_content()
    make_title("MISSING POKEMON")
    # Concept: Set difference
    missing = set(pokemon) - my_collection
    if len(missing) == 0:
        tk.Label(
            content,
            text="You caught them all! Congratulations!",
            font=FONT_SUB,
            bg=LIGHT,
            fg="green"
        ).pack(pady=30)
        return
    tk.Label(
        content,
        text=f"Pokemon missing: {len(missing)}",
        font=FONT_SUB,
        bg=LIGHT
    ).pack(pady=5)
    # Create a frame for the list and scrollbar
    list_frame = tk.Frame(content, bg=LIGHT)
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)
    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")
    listbox = tk.Listbox(
        list_frame,
        font=FONT_TEXT,
        yscrollcommand=scrollbar.set
    )
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)
    # Display missing Pokemon
    for name in sorted(missing):
        listbox.insert(tk.END, f"#{pokemon[name]:03d}  {name}")

# FUNCTION: collection_progress()
# Purpose: Show how much of the Pokedex is completed.
def collection_progress():
    clear_content()
    make_title("COLLECTION PROGRESS")
    total = len(pokemon)
    caught = len(my_collection)
    percent = caught / total * 100
    tk.Label(content, text=f"{caught} of {total} Pokemon collected",
             font=FONT_SUB, bg=LIGHT).pack(pady=10)
    bar = ttk.Progressbar(content, length=350, maximum=total, value=caught)
    bar.pack(pady=10)
    tk.Label(content, text=f"{percent:.0f}% complete",
             font=FONT_SUB, bg=LIGHT, fg=BLUE).pack(pady=5)
    if caught == total:
        tk.Label(content, text="Pokedex complete!", font=FONT_SUB,
                 bg=LIGHT, fg="green").pack(pady=10)

# FUNCTION: exit_app()
def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit PyDex?"):
        messagebox.showinfo("PyDex", "Exit..bye-bye")
        root.destroy()
    # ---------- SCREENS ----------

# FUNCTION: welcome()
# Purpose: Display the welcome screen with a Canva background
# and an animated Pikachu GIF.
def welcome():
    welcome_frame.pack(fill="both", expand=True)
    # Create a Canvas for the background and Pikachu
    canvas = tk.Canvas(
        welcome_frame,
        width=760,
        height=480,
        highlightthickness=0
    )
    canvas.pack()
    # Load the Canva background
    background = tk.PhotoImage(file="welcome.png")
    canvas.background = background
    canvas.create_image(
        0, 0,
        image=background,
        anchor="nw"
    )
    # PIKACHU ANIMATION
    # Concepts: Lists, loops, functions
    gif = Image.open("pikachu.gif")
    pikachu_frames = []
    # Load all frames and preserve transparency
    for frame_number in range(gif.n_frames):
        gif.seek(frame_number)
        frame = gif.convert("RGBA")
        pikachu_frames.append(ImageTk.PhotoImage(frame))
    # Keep the images in memory
    canvas.pikachu_frames = pikachu_frames
    # Display Pikachu on the background
    if pikachu_frames:
        pikachu = canvas.create_image(
            620, 360,
            image=pikachu_frames[0],
            anchor="center"
        )
    # Animate Pikachu by changing frames
        def animate_pikachu(index=0):
            if not canvas.winfo_exists():
                return
            canvas.itemconfig(
                pikachu,
                image=pikachu_frames[index]
            )
            next_index = (index + 1) % len(pikachu_frames)
            root.after(100, animate_pikachu, next_index)
        animate_pikachu()
    # Continue button opens the main menu
    continue_button = tk.Button(
        welcome_frame,
        text="CONTINUE",
        font=FONT_BTN,
        bg=YELLOW,
        fg="black",
        command=menu
    )
    continue_button.place(
        x=300,
        y=380,
        width=160,
        height=50
    )

# FUNCTION: menu()
# Purpose: Display the PyDex main menu with all the options.
def menu():
    global content
    welcome_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)
    # Left side: menu buttons
    sidebar = tk.Frame(
        main_frame,
        bg=DARK_PURPLE,
        width=220
    )
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)
    tk.Label(
        sidebar,
        text="PYDEX\nMAIN MENU",
        font=("Helvetica", 16, "bold"),
        bg=DARK_PURPLE,
        fg=YELLOW
    ).pack(pady=20)
    # Menu options created with a loop
    options = [
        ("1. Search Pokemon", search_pokemon),
        ("2. My Collection", show_collection),
        ("3. Catch a Pokemon", catch_pokemon),
        ("4. Missing Pokemon", missing_pokemon),
        ("5. Collection Progress", collection_progress),
        ("6. Exit", exit_app),
    ]
    for text, command in options:
        tk.Button(
            sidebar,
            text=text,
            font=FONT_BTN,
            bg=WHITE,
            fg="black",
            width=20,
            pady=6,
            command=command
        ).pack(pady=5)
    # Right side: content panel
    content = tk.Frame(main_frame, bg=LIGHT)
    content.pack(
        side="right",
        fill="both",
        expand=True,
        padx=8,
        pady=8
    )
    tk.Label(
        content,
        text="LET'S START! Choose an option\nfrom the menu",
        font=FONT_SUB,
        bg=LIGHT,
        fg="gray"
    ).pack(expand=True)
    # Call the welcome function to start the program.
welcome()
root.mainloop()
