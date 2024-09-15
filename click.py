import pyautogui
import time
import threading
from tkinter import *
from tkinter import messagebox
from pynput import keyboard

# Variáveis globais
clicking = False
click_interval = 0.1  # Intervalo padrão de 0.1 segundos entre cliques
click_count = 0  # Número de cliques a serem feitos (0 para infinito)
clicks_done = 0

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

# Função para lidar com eventos de tecla (F1 para ativar/desativar)
def on_press(key):
    if key == keyboard.Key.f1:
        toggle_clicker()

# Função para aplicar as configurações do usuário
def apply_settings():
    global click_interval, click_count
    try:
        click_interval = float(interval_entry.get())
        click_count = int(clicks_entry.get())
        update_status("Configurações aplicadas com sucesso!")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")
        return

# Função para mostrar a mensagem de ajuda
def show_help():
    help_text = (
        "Como usar o Auto Clicker:\n\n"
        "1. Pressione a tecla F1 para ativar/desativar o Auto Clicker.\n"
        "2. Defina o intervalo entre os cliques (em segundos) no campo de 'Intervalo entre cliques'.\n"
        "3. Defina o número de cliques no campo de 'Número de cliques'. Se deixar em '0', o Auto Clicker funcionará indefinidamente.\n"
        "4. Você pode iniciar o Auto Clicker pressionando F1 a qualquer momento.\n\n"
        "Pressione 'Aplicar Configurações' para salvar suas mudanças."
    )
    messagebox.showinfo("Ajuda - Auto Clicker", help_text)

# Criação da interface gráfica (GUI)
def create_gui():
    window = Tk()
    window.title("Auto Clicker - Painel de Controle")
    window.geometry("450x350")
    window.resizable(False, False)

    # Estilo do painel
    Label(window, text="Configurações do Auto Clicker", font=("Helvetica", 16, "bold")).pack(pady=10)

    # Intervalo entre cliques
    Label(window, text="Intervalo entre cliques (segundos):").pack(pady=5)
    global interval_entry
    interval_entry = Entry(window)
    interval_entry.insert(0, "0.1")
    interval_entry.pack(pady=5)

    # Número de cliques
    Label(window, text="Número de cliques (0 para infinito):").pack(pady=5)
    global clicks_entry
    clicks_entry = Entry(window)
    clicks_entry.insert(0, "0")
    clicks_entry.pack(pady=5)

    # Botão para aplicar configurações
    Button(window, text="Aplicar Configurações", command=apply_settings, width=20, height=2).pack(pady=10)

    # Botão de ajuda (Help)
    Button(window, text="Help", command=show_help, width=20, height=2).pack(pady=10)

    # Status do auto clicker
    global status_label
    status_label = Label(window, text="Auto Clicker Desativado", font=("Helvetica", 12), fg="red")
    status_label.pack(pady=20)

    # Mensagem de instrução
    Label(window, text="Pressione F1 para iniciar ou parar o Auto Clicker", fg="blue").pack(pady=5)

    # Listener para detectar a tecla F1
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    window.mainloop()

# Executa a interface gráfica
create_gui()
