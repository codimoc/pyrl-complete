import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import VERTICAL, ttk

# this is the model, used by different functions
_context = dict()


def main():
    root = create_main_window()
    main_frame = create_main_frame(root)
    log_window = create_log_window(main_frame)
    notebook = create_notebook(main_frame)
    # position the notebook in the top part of main_frame..
    notebook.grid(row=0, column=0, sticky="nsew")
    # and the log in the bottom part
    log_window.grid(row=1, column=0, sticky="nsew")
    root.mainloop()


def create_main_window():
    root = tk.Tk()
    root.title("Rule tester")
    root.geometry("800x600")
    return root


def create_main_frame(root):
    main_frame = tk.Frame(root, background="lightyellow", padx=10, pady=10)
    main_frame.pack(fill="both", expand=True, padx=5, pady=5)
    main_frame.rowconfigure(0, weight=3)
    main_frame.rowconfigure(1, weight=1)
    main_frame.columnconfigure(0, weight=1)
    return main_frame


def create_notebook(parent):
    notebook = ttk.Notebook(parent)
    _context["notebook"] = notebook
    create_test_tab(notebook)
    create_write_tab(notebook)
    return notebook


def create_test_tab(notebook):
    # this is the first tab of the notebook
    test_tab = ttk.Frame(notebook, padding=(10, 10, 10, 10))
    notebook.add(test_tab, text="Test Rules")
    # with the following the tab has one row and one column, both full weight
    test_tab.rowconfigure(0, weight=1)
    test_tab.columnconfigure(0, weight=1)
    button_panel = create_button_panel_test_frame(test_tab)
    button_panel.grid(row=1, column=0, sticky="nsew")
    top_title = tk.Label(test_tab, text="Command line input")
    top_title.grid(row=2, column=0, sticky="nsew")
    top_content = st.ScrolledText(test_tab)
    top_content.grid(row=3, column=0, sticky="nsew")

    return test_tab


def create_button_panel_test_frame(frame):
    button_frame = ttk.Frame(frame)
    button_frame.grid(row=0, column=0, sticky="nsew")
    button_frame.rowconfigure(0, weight=1)
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    load_rules_button = ttk.Button(
        button_frame, text="Load Rules",
        command=lambda: handle_load_rules()
    )
    load_rules_button.grid(row=0, column=0, sticky="nsew")
    write_rules_button = ttk.Button(
        button_frame, text="Write Rules",
        command=lambda: handle_write_rules()
    )
    write_rules_button.grid(row=0, column=1, sticky="nsew")

    return button_frame


def handle_load_rules():
    log_content = _context["log_content"]
    log_content.insert(tk.END, "Loading rules...")
    log_content.yview_moveto(1)


def handle_write_rules():
    log_content = _context["log_content"]
    notebook = _context["notebook"]
    log_content.insert(tk.END, "Writing rules...")
    log_content.yview_moveto(1)
    notebook.select(1)  # Select the "Write Rules" tab (index 1)


def create_write_tab(notebook):
    tab = ttk.Frame(notebook, padding=(10, 10, 10, 10))
    notebook.add(tab, text="Write Rules")
    label = ttk.Label(tab, text="This is the content.")
    label.pack(padx=5, pady=5)
    text_widget = tk.Text(tab, height=5, width=40)
    text_widget.insert(tk.END, "You can type here in")
    text_widget.pack(padx=5, pady=5)


def create_log_window(parent):
    log_window = tk.Frame(parent, background="lightyellow")
    title = tk.Label(log_window, text="Log Activity", background="lightyellow")
    title.pack(padx=5, pady=5)
    scroll = ttk.Scrollbar(log_window, orient=VERTICAL)
    log_content = tk.Listbox(log_window, yscrollcommand=scroll.set)
    scroll.config(command=log_content.yview)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)
    log_content.pack(fill=tk.BOTH, expand=True)
    _context["log_content"] = log_content
    return log_window


if __name__ == "__main__":
    main()
