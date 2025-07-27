import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import filedialog, ttk
from pyrl_complete.apps import _context
from pyrl_complete.parser import Parser


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
    test_tab.columnconfigure(0, weight=1)
    test_tab.rowconfigure(0, weight=1)
    test_tab.rowconfigure(1, weight=1)
    test_tab.rowconfigure(2, weight=1)
    test_tab.rowconfigure(3, weight=1)
    # this is the top row containing the buttons
    button_panel = create_button_panel_test_frame(test_tab)
    button_panel.grid(row=0, column=0, sticky="nsew")
    # this is the second row containing the content 
    test_inner_frame = ttk.Frame(test_tab)  # where the content is
    test_inner_frame.grid(row=1, column=0, sticky="nsew")
    # first row for helpers
    test_inner_frame.rowconfigure(0, weight=3)
    # second row for label
    test_inner_frame.rowconfigure(1, weight=1)
    # third row for typing
    test_inner_frame.columnconfigure(0, weight=1)
    # this goes on the top row and it is split in two 
    # columns, one for rules and one for predictions
    test_inner_frame_top = ttk.Frame(test_inner_frame)
    test_inner_frame_top.grid(row=0, column=0, sticky="nsew")
    # this is for a lablel containg a read-only version
    # of the rules
    test_inner_frame_top.columnconfigure(0, weight=3)
    # this for a list of predictions
    test_inner_frame_top.columnconfigure(1, weight=1)
    label_rules = tk.Label(test_inner_frame_top, text="Rules")
    label_rules.grid(row=0, column=0, sticky="nsew")
    label_predictions = tk.Label(test_inner_frame_top, text="Predictions")
    label_predictions.grid(row=0, column=1, sticky="nsew")   
    test_rules = st.ScrolledText(
        test_inner_frame_top,
        bg="lightyellow",
        padx=5,
        wrap=tk.WORD,
        height=5
    )
    test_rules.grid(row=1, column=0, sticky="nsew")
    test_rules.config(state=tk.DISABLED)  # make it read-only
    _context["test_rules"] = test_rules
    test_predictions = tk.Listbox(test_inner_frame_top)
    test_predictions.grid(row=1, column=1, sticky="nsew")
    _context["test_predictions"] = test_predictions
    
    label_input = tk.Label(test_tab, text="Command line input")
    label_input.grid(row=2, column=0, sticky="nsew")
    text_input = tk.Entry(test_tab)
    _context
    text_input.grid(row=3, column=0, sticky="nsew")

    return test_tab


def create_button_panel_test_frame(frame):
    button_frame = ttk.Frame(frame)
    button_frame.grid(row=0, column=0, sticky="nsew")
    button_frame.rowconfigure(0, weight=1)
    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.columnconfigure(2, weight=1)

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
    test_paths_label = tk.Label(button_frame, 
                                text="0 paths generated", 
                                fg="red")
    test_paths_label.grid(row=0, column=2, sticky="nsew", padx=5)
    _context["test_paths_label"] = test_paths_label

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
    button_frame.columnconfigure(2, weight=1)

    save_rules_button = ttk.Button(
        button_frame, text="Save Rules",
        command=lambda: handle_save_rules()
    )
    save_rules_button.grid(row=0, column=0, sticky="nsew")
    parse_rules_button = ttk.Button(
        button_frame, text="Parse Rules",
        command=lambda: handle_parse_rules()
    )
    parse_rules_button.grid(row=0, column=1, sticky="nsew")

    write_paths_label = tk.Label(
        button_frame, text="0 paths generated", fg="red"
    )
    write_paths_label.grid(row=0, column=2, sticky="nsew", padx=5)
    _context["write_paths_label"] = write_paths_label

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
    write_paths_label = _context["write_paths_label"]
    test_paths_label = _context["test_paths_label"]
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.prl"), ("All files", "*.*")]
    )
    if file_path:
        with open(file_path, "r") as file:
            rules_text = file.read()
        rules_editor.delete("1.0", tk.END)
        rules_editor.insert(tk.END, rules_text)
        log_content.insert(tk.END, f"Rules loaded from {file_path}")
        log_content.yview_moveto(1)
        write_paths_label.config(text="0 paths generated", fg="red")
        test_paths_label.config(text="0 paths generated", fg="red")
        # also switch to the write tab
        notebook = _context["notebook"]
        notebook.select(1)


def handle_write_rules():
    log_content = _context["log_content"]
    notebook = _context["notebook"]
    log_content.insert(tk.END, "Writing rules...")
    log_content.yview_moveto(1)
    notebook.select(1)  # Select the "Write Rules" tab (index 1)


def handle_parse_rules():
    log_content = _context["log_content"]
    write_paths_label = _context["write_paths_label"]
    test_paths_label = _context["test_paths_label"]
    test_rules = _context["test_rules"]
    log_content.insert(tk.END, "Parsing rules...")
    log_content.yview_moveto(1)
    if "parser" not in _context:        
        _context["parser"] = Parser()
    parser = _context["parser"]
    rules_editor = _context["rules_editor"]
    rules_text = rules_editor.get("1.0", tk.END)
    parser.parse(rules_text)  # Assuming parser.parse() takes the rules text
    num_paths = len(parser.paths)
    log_content.insert(tk.END,
                       f"Rules parsed successfully: generated "
                       f"{num_paths} paths from rules.")
    
    test_rules.config(state=tk.NORMAL)
    test_rules.delete("1.0", tk.END)
    test_rules.insert(tk.END, rules_text)
    test_rules.config(state=tk.DISABLED)
    write_paths_label.config(text=f"{num_paths} paths generated", fg="green")
    test_paths_label.config(text=f"{num_paths} paths generated", fg="green")

