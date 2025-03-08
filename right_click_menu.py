import tkinter as tk


# Create the context menu
def create_context_menu(window, yt_input):
    context_menu = tk.Menu(window, tearoff=0)
    context_menu.add_command(label='Clear', command=lambda: yt_input.delete(0, tk.END))
    context_menu.add_command(label="Cut", command=lambda: yt_input.event_generate("<Control-x>"))
    context_menu.add_command(label="Copy", command=lambda: yt_input.event_generate("<Control-c>"))
    context_menu.add_command(label="Paste", command=lambda: yt_input.event_generate("<Control-v>"))
    return context_menu


def show_context_menu(event, context_menu):
    context_menu.post(event.x_root, event.y_root)
