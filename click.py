import pyautogui
import time
import threading
from tkinter import *
from tkinter import messagebox
from pynput import keyboard
import webbrowser

# Variáveis globais
clicking = False
click_interval = 0.1  # Intervalo padrão de 0.1 segundos entre cliques
click_count = 0  # Número de cliques a serem feitos (0 para infinito)
clicks_done = 0
start_key = keyboard.Key.f1  # Tecla padrão para iniciar/parar
stop_key = keyboard.Key.f2   # Tecla padrão para parar

# Função para realizar o auto click
def auto_click():
    global clicks_done, clicking
    clicks_done = 0
    while clicking and (click_count == 0 or clicks_done < click_count):
        pyautogui.click()
        clicks_done += 1
        time.sleep(click_interval)
    clicking = False
    update_status("Auto Clicker Desativado")

# Função para alternar o estado do auto clicker
def toggle_clicker():
    global clicking
    clicking = not clicking
    if clicking:
        update_status("Auto Clicker Ativado")
        start_clicking_thread()
    else:
        update_status("Auto Clicker Desativado")

# Função para iniciar o thread do auto clicker
def start_clicking_thread():
    thread = threading.Thread(target=auto_click)
    thread.daemon = True  # Daemon thread para encerrar com a janela
    thread.start()

# Função para atualizar o status do auto clicker no painel
def update_status(status):
    status_label.config(text=status)

# Função para lidar com eventos de tecla
def on_press(key):
    global clicking
    if key == start_key:
        toggle_clicker()
    elif key == stop_key:
        clicking = False
        update_status("Auto Clicker Desativado")

# Função para aplicar as configurações do usuário
def apply_settings():
    global click_interval, click_count, start_key, stop_key
    try:
        click_interval = float(interval_entry.get())
        click_count = int(clicks_entry.get())
        update_status("Configurações aplicadas com sucesso!")
        
        # Atualiza atalhos de teclado
        start_key_str = start_key_entry.get().lower()
        stop_key_str = stop_key_entry.get().lower()
        
        if start_key_str.startswith('f') and start_key_str[1:].isdigit():
            start_key = getattr(keyboard.Key, f'f{start_key_str[1:]}', None)
        else:
            raise KeyError
        
        if stop_key_str.startswith('f') and stop_key_str[1:].isdigit():
            stop_key = getattr(keyboard.Key, f'f{stop_key_str[1:]}', None)
        else:
            raise KeyError
        
        # Atualiza os atalhos no listener
        global listener
        listener.stop()
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
        
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")
        return
    except KeyError:
        messagebox.showerror("Erro", "Tecla inválida para o atalho. Use teclas como 'f1', 'f2', etc.")
        return

# Função para mostrar a mensagem de ajuda
def show_help():
    help_text = (
        "Como usar o Auto Clicker:\n\n"
        "1. Pressione o atalho configurado para ativar/desativar o Auto Clicker.\n"
        "2. Defina o intervalo entre os cliques (em segundos) no campo de 'Intervalo entre cliques'.\n"
        "3. Defina o número de cliques no campo de 'Número de cliques'. Se deixar em '0', o Auto Clicker funcionará indefinidamente.\n"
        "4. Você pode alterar os atalhos de teclado nos campos de configuração.\n\n"
        "Guia de Uso:\n"
        "- O Auto Clicker é uma ferramenta que realiza cliques automáticos em intervalos regulares.\n"
        "- Ideal para tarefas repetitivas onde o clique constante é necessário.\n"
        "- Configure o intervalo e o número de cliques desejados antes de ativar o Auto Clicker.\n\n"
        "Para mais informações, consulte a documentação ou entre em contato com o suporte."
    )
    messagebox.showinfo("Ajuda - Auto Clicker", help_text)

# Função para abrir o perfil do Instagram
def open_instagram():
    webbrowser.open("https://www.instagram.com/eog_x/")

# Criação da interface gráfica (GUI)
def create_gui():
    global interval_entry, clicks_entry, status_label, start_key_entry, stop_key_entry, listener

    window = Tk()
    window.title("Auto Clicker - Painel de Controle")
    window.geometry("700x500")
    # window.resizable(False, False)
    window.config(bg="#f5f5f5")

    # icon = PhotoImage(file='images/logo.png')

    # window.iconphoto(True, icon)

    # Título
    title_frame = Frame(window, bg="#4a4a4a")
    title_frame.pack(fill=X, pady=10)

    Label(title_frame, text="Auto Clicker", font=("Helvetica", 18, "bold"), bg="#4a4a4a", fg="white").pack()

    # Configurações
    settings_frame = Frame(window, bg="#ffffff")
    settings_frame.pack(pady=10, padx=20, fill=X)

    Label(settings_frame, text="Intervalo entre cliques (segundos):", font=("Helvetica", 12), bg="#ffffff").grid(row=0, column=0, sticky=W, padx=10, pady=5)
    interval_entry = Entry(settings_frame, width=20)
    interval_entry.insert(0, "0.1")
    interval_entry.grid(row=0, column=1, padx=10, pady=5)

    Label(settings_frame, text="Número de cliques (0 para infinito):", font=("Helvetica", 12), bg="#ffffff").grid(row=1, column=0, sticky=W, padx=10, pady=5)
    clicks_entry = Entry(settings_frame, width=20)
    clicks_entry.insert(0, "0")
    clicks_entry.grid(row=1, column=1, padx=10, pady=5)

    Label(settings_frame, text="Tecla para Iniciar/Parar (ex: f1):", font=("Helvetica", 12), bg="#ffffff").grid(row=2, column=0, sticky=W, padx=10, pady=5)
    start_key_entry = Entry(settings_frame, width=20)
    start_key_entry.insert(0, "f1")
    start_key_entry.grid(row=2, column=1, padx=10, pady=5)

    Label(settings_frame, text="Tecla para Parar (ex: f2):", font=("Helvetica", 12), bg="#ffffff").grid(row=3, column=0, sticky=W, padx=10, pady=5)
    stop_key_entry = Entry(settings_frame, width=20)
    stop_key_entry.insert(0, "f2")
    stop_key_entry.grid(row=3, column=1, padx=10, pady=5)

    # Botão para aplicar configurações
    apply_button = Button(window, text="Aplicar Configurações", command=apply_settings, width=25, height=2, bg="#4a90e2", fg="white", font=("Helvetica", 12))
    apply_button.pack(pady=10)

    # Botão de ajuda (Help)
    help_button = Button(window, text="Help", command=show_help, width=25, height=2, bg="#4a90e2", fg="white", font=("Helvetica", 12))
    help_button.pack(pady=10)

    # Status do auto clicker
    status_label = Label(window, text="Auto Clicker Desativado", font=("Helvetica", 14), fg="red", bg="#f5f5f5")
    status_label.pack(pady=20)

    # Mensagem de instrução
    instruction_label = Label(window, text="Pressione o atalho configurado para iniciar ou parar o Auto Clicker", font=("Helvetica", 12), fg="blue", bg="#f5f5f5")
    instruction_label.pack(pady=5)

    # Rodapé
    footer_frame = Frame(window, bg="#4a4a4a")
    footer_frame.pack(side=BOTTOM, fill=X, pady=10)
    footer_label = Label(footer_frame, text="@eog_xx - 2024", font=("Helvetica", 10), fg="white", bg="#4a4a4a")
    footer_label.pack(side=LEFT, padx=10)
    instagram_link = Button(footer_frame, text="Instagram", font=("Helvetica", 10), fg="white", bg="#4a4a4a", relief=FLAT, command=open_instagram)
    instagram_link.pack(side=RIGHT, padx=10)

    # Listener para detectar as teclas
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    window.mainloop()

# Executa a interface gráfica
create_gui()
