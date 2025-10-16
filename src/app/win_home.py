import tkinter as tk
from tkinter import ttk, messagebox
from app.win_form import open_win_form


def open_win_home(parent: tk.Tk, return_to=None):
    win = tk.Toplevel(parent)
    win.title("Home / Bienvenida")
    win.geometry("450x350")
    win.resizable(False, False)
    
    # Colores
    BG_COLOR = "#f0f0f0"
    CARD_BG = "#ffffff"
    PRIMARY_COLOR = "#0066cc"
    SECONDARY_COLOR = "#6c757d"
    
    win.configure(bg=BG_COLOR)
    
    # Estilos
    style = ttk.Style()
    style.theme_use('clam')
    
    style.configure('Card.TFrame', background=CARD_BG)
    style.configure('Title.TLabel', background=CARD_BG, foreground='#212529', font=('Segoe UI', 14, 'bold'))
    style.configure('Text.TLabel', background=CARD_BG, foreground=SECONDARY_COLOR, font=('Segoe UI', 10))
    
    style.configure('Primary.TButton', background=PRIMARY_COLOR, foreground='white', 
                   font=('Segoe UI', 10, 'bold'), borderwidth=0, padding=(20, 12))
    style.map('Primary.TButton', background=[('active', '#0052a3')])
    
    style.configure('Secondary.TButton', background='#e9ecef', foreground='#212529', 
                   font=('Segoe UI', 9), borderwidth=0, padding=(20, 10))
    style.map('Secondary.TButton', background=[('active', '#dee2e6')])
    
    # Contenedor
    container = tk.Frame(win, bg=BG_COLOR)
    container.pack(fill="both", expand=True, padx=30, pady=30)
    
    frm = ttk.Frame(container, style='Card.TFrame', padding=25)
    frm.pack(fill="both", expand=True)
    
    # Funciones ANTES de crear los widgets (esto es crítico)
    def open_and_close():
        win.destroy()
        open_win_form(parent, lambda p: open_win_home(p, return_to))
    
    def volver():
        win.destroy()
        if return_to:
            return_to(parent)
    
    # Widgets
    ttk.Label(frm, text="¡Bienvenid@s!", style='Title.TLabel').pack(pady=(10, 8))
    ttk.Label(frm, text="Explora las ventanas desde la pantalla principal.", 
             style='Text.TLabel').pack(pady=(0, 20))
    
    ttk.Separator(frm, orient='horizontal').pack(fill='x', pady=(0, 20))
    
    ttk.Button(frm, text="Iniciar Sesion", command=open_and_close, 
              style='Primary.TButton').pack(pady=(0, 10), fill="x")
    
    ttk.Button(frm, text="Cerrar", command=volver, 
              style='Secondary.TButton').pack(pady=(0, 10), fill="x")
