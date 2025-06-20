import sys
import threading
import tkinter as tk
from time import strftime
from PIL import Image, ImageTk
from dadjokes import Dadjoke
from right_click_menu import show_context_menu, create_context_menu
from youtube_to_mp3 import *

BG = 'deep sky blue'
INFO_LBL_FONT = ("Comic Sans MS", 15, 'italic')
WELCOME_LBL_FONT = ('System', 30, ['bold'])
PADDING = 10

joke_window = None


def resource_path(relative_path):
    """ Returns the path dynamically """
    if hasattr(sys, '_MEIPASS'):
        # noinspection PyProtectedMember
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def start_download():
    """ Starts the YT download in a new thread """
    url = yt_input.get()
    yt_input.delete(0, tk.END)
    # if invalid input -> do nothing
    if url is None or url == '' or len(url) < 5:
        title_var.set('Invalid input! Try again..\n(Input must be longer than 5 symbols!)')
        return
    else:
        if url.startswith('https'):
            title_var.set(f'Downloading from Link: >>\n{url}')
        else:
            title_var.set(f'Searching YouTube for: >>\n{url}')
        # using thread, so the download doesn't block the UI
        threading.Thread(target=youtube_downloader, args=(url, update_song_label), daemon=True).start()



def update_song_label(info):
    """ Func to update the status label """
    # title_var.set(' ✅ Download complete! ✅\n' + '--' * 50 + f'\n{title}')
    title_var.set(info)


def open_folder():
    """ Function to open the download folder """
    os.startfile(DOWNLOAD_DIR)


def update_time():
    """ Function to update the clock every second """
    current_time = strftime('%H:%M:%S')
    clock_label.config(text=current_time)
    clock_label.after(1000, update_time)


def new_joke():
    """ Function to create new tkinter window, and print new joke in it. """
    global joke_window
    if joke_window is not None:
        try:
            joke_window.destroy()
        except tk.TclError:
            joke_window = None
    joke_window = tk.Toplevel()
    joke_window.title('Just another Dad Joke..😁😀')
    joke_window.minsize(100, 100)
    joke_window.config(padx=50, pady=50, bg='sky blue')
    # IT jokes // boring
    # text = pyjokes.get_joke(language='en')
    text = '😁'*10 + f'\n{Dadjoke().joke}\n' + '😁'*10
    joke_label = tk.Label(
        joke_window,
        text=text,
        font=('Aerial', 18),
        bg='sky blue',
        wraplength=300)
    joke_label.grid(column=0, row=0, rowspan=3)
    joke_window.protocol("WM_DELETE_WINDOW", on_close_joke_window)


def on_close_joke_window():
    global joke_window
    joke_window.destroy()
    joke_window = None  # Reset the reference


# main window settings
main_window = tk.Tk()
main_window.title("Youtube Downloader 1.0")
main_window.minsize(560, 560)
main_window.config(padx=PADDING, pady=PADDING, bg=BG)

folder_img_path = resource_path('images\\folder_img.png')
img = Image.open(folder_img_path)
# Resize the image proportionally based on the width
max_width = 50  # Maximum width for the image
width_percent = (max_width / float(img.size[0]))  # Calculate the width percentage
height_size = int((float(img.size[1]) * float(width_percent)))  # Scale the height proportionally
# Resize using LANCZOS for high-quality resampling
img = img.resize((max_width, height_size), Image.Resampling.LANCZOS)
# Convert to PhotoImage for use in Tkinter
folder_img = ImageTk.PhotoImage(img)

# YouTube app welcome label
welcome_label = tk.Label(
    text='YouTube mp3 Downloader',
    bg=BG,
    font=WELCOME_LBL_FONT)
welcome_label.grid(column=0, row=0, padx=PADDING, pady=PADDING, sticky='NSEW')

# YouTube search label
yt_input_label = tk.Label(
    text='⬇ Insert YouTube URL or search for song below ⬇',
    font=('Aerial', 15),
    bg=BG)
yt_input_label.grid(column=0, row=1, padx=PADDING, pady=PADDING, sticky='NSEW')

# YouTube search input box
yt_input = tk.Entry(
    font=('Aerial', 16),
    width=41,
    bg='sky blue',
    borderwidth=4)
yt_input.grid(column=0, row=2, padx=PADDING, pady=PADDING, sticky='NSEW')
yt_input.focus_set()

# handles the right click menu
context_menu = create_context_menu(main_window, yt_input)
yt_input.bind("<Button-3>", lambda event: show_context_menu(event, context_menu))

# YT Download button
yt_button = tk.Button(
    text='Download mp3',
    font=('Aerial', 18),
    command=start_download,
    relief='raised',
    overrelief='raised',
    borderwidth=4,
    width=35,
    bg='RoyalBlue1',
    activebackground=BG)
yt_button.grid(column=0, row=3, padx=PADDING, pady=PADDING, sticky='NSEW')

# Download status label
title_var = tk.StringVar()
title_var.set('Downloaded song will appear below...')
info_label = tk.Label(
    textvariable=title_var,
    font=INFO_LBL_FONT,
    bg=BG,
    wraplength=500,  # Set the maximum width (in pixels) before wrapping
    justify='center',)
info_label.grid(column=0, row=4, rowspan=3, padx=PADDING, pady=PADDING, sticky='NSEW')

# clock label
clock_label = tk.Label(
    font=('Ink free', 40),
    bg='black',
    fg='cyan',
    width=17)
clock_label.grid(column=0, row=9, padx=PADDING, pady=PADDING, sticky='NSEW')

# New joke button
get_joke_button = tk.Button(
    text="I'm bored! Tell me a Dad joke!",
    command=new_joke,
    font=('Aerial', 18),
    relief='raised',
    borderwidth=4,
    width=35,
    bg='RoyalBlue1',
    activebackground=BG)
get_joke_button.grid(column=0, row=10, padx=PADDING, pady=PADDING, sticky='NSEW')

# button to open downloads folder
download_folder_button = tk.Button(
    text='Download Folder',
    command=open_folder,
    font=('Aerial', 10),
    image=folder_img,
    compound='bottom',
    width=80,
    height=80,
    bg=BG,
    activebackground=BG,
    relief='flat',
    wraplength=80)
download_folder_button.grid(column=0, row=11, rowspan=2, padx=PADDING, pady=PADDING, sticky='NSEW')

update_time()

main_window.mainloop()


