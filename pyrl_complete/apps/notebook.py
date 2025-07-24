import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import filedialog, ttk
from pyrl_complete.apps import _context


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


def create_write_tab(notebook):
    write_tab = ttk.Frame(notebook, padding=(10, 10, 10, 10))
    notebook.add(write_tab, text="Write Rules")
    # with the following the tab has one row and one column, both full weight
    write_tab.rowconfigure(0, weight=1)
    write_tab.columnconfigure(0, weight=1)
    button_panel = create_button_panel_write_frame(write_tab)
    button_panel.grid(row=1, column=0, sticky="nsew")
    top_title = tk.Label(write_tab, text="Write the rules here")
    top_title.grid(row=2, column=0, sticky="nsew")
    top_content = st.ScrolledText(write_tab)
    _context["rules_editor"] = top_content
    top_content.grid(row=3, column=0, sticky="nsew")

    return write_tab


def create_button_panel_write_frame(frame):
    button_frame = ttk.Frame(frame)
    button_frame.grid(row=0, column=0, sticky="nsew")
    button_frame.rowconfigure(0, weight=1)
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    save_rules_button = ttk.Button(
        button_frame, text="Save Rules",
        command=lambda: handle_save_rules()
    )
    save_rules_button.grid(row=0, column=0, sticky="nsew")

    return button_frame


# button handlers here


def handle_save_rules():
    rules_editor = _context["rules_editor"]
    log_content = _context["log_content"]
    rules_text = rules_editor.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(
        defaultextension=".prl",
        filetypes=[("Rules files", "*.prl"), ("All files", "*.*")],
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(rules_text)
        log_content.insert(tk.END, f"Rules saved to {file_path}")
        log_content.yview_moveto(1)


def handle_load_rules():
    rules_editor = _context["rules_editor"]
    log_content = _context["log_content"]
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "r") as file:
            rules_text = file.read()
        rules_editor.delete("1.0", tk.END)
        rules_editor.insert(tk.END, rules_text)
        log_content.insert(tk.END, f"Rules loaded from {file_path}")
        log_content.yview_moveto(1)
        # also switch to the write tab
        notebook = _context["notebook"]
        notebook.select(1)


def handle_write_rules():
    log_content = _context["log_content"]
    notebook = _context["notebook"]
    log_content.insert(tk.END, "Writing rules...")
    log_content.yview_moveto(1)
    notebook.select(1)  # Select the "Write Rules" tab (index 1)
