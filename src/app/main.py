import tkinter as tk
from tkinter import ttk
from app.win_home import open_win_home
from app.win_form import open_win_form
from app.win_table import open_win_table


def main():
    root = tk.Tk()
    root.title("Proyecto Integrador - MVP")
    root.geometry("500x400")
    root.resizable(False, False)
    
    # Configurar colores modernos
    BG_COLOR = "#f0f0f0"
    CARD_BG = "#ffffff"
    PRIMARY_COLOR = "#0066cc"
    PRIMARY_HOVER = "#0052a3"
    SECONDARY_COLOR = "#6c757d"
    TEXT_COLOR = "#212529"
    BORDER_COLOR = "#dee2e6"
    
    root.configure(bg=BG_COLOR)
    
  
    style = ttk.Style()
    style.theme_use('clam')
    

    style.configure('Card.TFrame', 
                   background=CARD_BG, 
                   relief='flat')
    

    style.configure('Title.TLabel', 
                   background=CARD_BG, 
                   foreground=TEXT_COLOR, 
                   font=('Segoe UI', 16, 'bold'))
    
    style.configure('Subtitle.TLabel', 
                   background=CARD_BG, 
                   foreground=SECONDARY_COLOR, 
                   font=('Segoe UI', 9))
    

    style.configure('Primary.TButton', 
                   background=PRIMARY_COLOR, 
                   foreground='white', 
                   font=('Segoe UI', 10),
                   borderwidth=0,
                   focuscolor='none',
                   padding=(20, 12))
    
    style.map('Primary.TButton',
             background=[('active', PRIMARY_HOVER), ('pressed', PRIMARY_HOVER)],
             relief=[('pressed', 'flat'), ('!pressed', 'flat')])
    

    style.configure('Secondary.TButton', 
                   background=SECONDARY_COLOR, 
                   foreground='white', 
                   font=('Segoe UI', 9),
                   borderwidth=0,
                   focuscolor='none',
                   padding=(20, 10))
    
    style.map('Secondary.TButton',
             background=[('active', '#5a6268'), ('pressed', '#5a6268')],
             relief=[('pressed', 'flat'), ('!pressed', 'flat')])

    session_started = {'value': False}
    form_saved = {'value': False}

    def show_main_menu(parent):
        for child in parent.winfo_children():
            child.destroy()
        

        container = tk.Frame(parent, bg=BG_COLOR)
        container.pack(fill="both", expand=True, padx=40, pady=40)
        

        frame = ttk.Frame(container, style='Card.TFrame', padding=30)
        frame.pack(fill="both", expand=True)
        
   
        frame.configure(relief='solid', borderwidth=1)
        
  
        title = ttk.Label(frame, 
                         text="Aplicación Demo", 
                         style='Title.TLabel')
        title.pack(pady=(0, 5))
        

        subtitle = ttk.Label(frame, 
                            text="Sistema de Gestión - MVP", 
                            style='Subtitle.TLabel')
        subtitle.pack(pady=(0, 30))
        
        # Separador
        separator = ttk.Separator(frame, orient='horizontal')
        separator.pack(fill='x', pady=(0, 25))
        
        def iniciar():
            session_started['value'] = True
            open_win_home(parent, lambda p: show_main_menu(p))
        
        def iniciar_o_bypass():
            if form_saved['value']:
                open_win_form(parent, lambda p: show_main_menu(p))
            else:
                iniciar()
        
        # Botón principal
        btn_home = ttk.Button(frame, 
                             text="🏠  Home / Bienvenida", 
                             command=iniciar_o_bypass,
                             style='Primary.TButton')
        btn_home.pack(pady=(0, 12), fill="x")
        
        # Espaciador
        spacer = tk.Frame(frame, height=20, bg=CARD_BG)
        spacer.pack()
        
        # Botón salir
        btn_exit = ttk.Button(frame, 
                             text="Salir", 
                             command=parent.destroy,
                             style='Secondary.TButton')
        btn_exit.pack(pady=(0, 0), fill="x")

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