import tkinter as tk
from tkinter import ttk
from app.win_home import open_win_home
from app.win_form import open_win_form
from app.win_table import open_win_table

def main():
    root = tk.Tk()
    root.title("Proyecto Integrador - MVP")
    root.geometry("420x340")

    frame = ttk.Frame(root, padding=16)
    frame.pack(fill="both", expand=True)

    session_started = {'value': False}
    form_saved = {'value': False}

    def show_main_menu(parent):
        for child in parent.winfo_children():
            child.destroy()
        frame = ttk.Frame(parent, padding=16)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="Aplicación Demo (tkinter)", font=("Segoe UI", 12, "bold")).pack(pady=(0, 12))
        def iniciar():
            session_started['value'] = True
            open_win_home(parent, lambda p: show_main_menu(p))
        def iniciar_o_bypass():
            if form_saved['value']:
                open_win_form(parent, lambda p: show_main_menu(p))
            else:
                iniciar()
        ttk.Button(frame, text="1) Home / Bienvenida", command=iniciar_o_bypass).pack(pady=4, fill="x")
        ttk.Button(frame, text="Salir", command=parent.destroy).pack(pady=6)

    # Patch open_win_form to set form_saved['value'] = True after successful save
    import types
    from app import win_form as win_form_mod
    orig_open_win_form = win_form_mod.open_win_form
    def patched_open_win_form(parent, return_to=None):
        def patched_return_to(p):
            show_main_menu(p)
        def on_save():
            form_saved['value'] = True
        # Patch the validar_y_guardar inside open_win_form
        # We'll monkeypatch after window creation
        win = orig_open_win_form(parent, return_to)
        # Not strictly needed if open_win_form is not returning the window, but for future extensibility
        return win
    win_form_mod.open_win_form = patched_open_win_form

    show_main_menu(root)
    root.mainloop()

if __name__ == "__main__":
    main()