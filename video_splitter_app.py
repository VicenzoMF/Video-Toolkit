import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
from moviepy.editor import VideoFileClip
import os

video_queue = []  # Lista para armazenar os vídeos na fila
progress_var = None  # Variável global para a barra de progresso

def split_video(input_file, output_folder, duration=90):
    global progress_var
    video = VideoFileClip(input_file)
    total_duration = video.duration
    current_time = 0
    part_number = 1

    while current_time < total_duration:
        end_time = min(current_time + duration, total_duration)
        part = video.subclip(current_time, end_time)
        output_file = os.path.join(output_folder, f"Parte_{part_number}.mp4")
        part.write_videofile(output_file, codec='libx264')
        current_time += duration
        part_number += 1

        # Atualiza o valor da barra de progresso
        progress_var.set(current_time / total_duration * 100)
        root.update()

    video.close()

def browse_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
    if file_path:
        video_entry.delete(0, tk.END)
        video_entry.insert(0, file_path)

def browse_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder_path)

def add_to_queue():
    file_path = video_entry.get()
    if file_path:
        video_queue.append(file_path)
        video_entry.delete(0, tk.END)
        update_queue_list()

def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder_path)

def split_video_action():
    global progress_var
    progress_bar["maximum"] = 100  # Define o valor máximo da barra de progresso (0-100%)
    for idx, video_path in enumerate(video_queue, start=1):
        input_file_path = video_path
        output_folder_path = output_folder_entry.get()

        if output_folder_path:
            if not os.path.exists(output_folder_path):
                os.makedirs(output_folder_path)

            progress_label.config(text=f"Cortando vídeo {idx} de {len(video_queue)}: {os.path.basename(video_path)}")

            # Cria uma variável IntVar para armazenar o valor da barra de progresso
            progress_var = tk.IntVar()
            progress_bar["variable"] = progress_var

            # Inicia a função split_video() usando after() para permitir atualizações de interface
            root.after(100, split_video, input_file_path, output_folder_path)

    # Após o término da divisão de vídeos, limpa a fila e reinicia a barra de progresso e label
    video_queue.clear()
    update_queue_list()
    progress_var.set(0)
    progress_label.config(text="")

def update_queue_list():
    queue_list.delete(0, tk.END)
    for idx, video_path in enumerate(video_queue, start=1):
        queue_list.insert(tk.END, f"{idx}. {video_path}")

# Cria a janela principal
root = tk.Tk()
root.title("Video Splitter App")

# Adiciona os componentes da interface
video_label = tk.Label(root, text="Vídeo:")
video_label.grid(row=0, column=0, padx=10, pady=5)

video_entry = tk.Entry(root, width=50)
video_entry.grid(row=0, column=1, padx=10, pady=5)

browse_video_button = tk.Button(root, text="Localizar vídeo", command=browse_video)
browse_video_button.grid(row=0, column=2, padx=10, pady=5)

output_folder_label = tk.Label(root, text="Pasta de Salvamento:")
output_folder_label.grid(row=1, column=0, padx=10, pady=5)

output_folder_entry = tk.Entry(root, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=5)

browse_output_folder_button = tk.Button(root, text="Pasta de salvamento", command=select_output_folder)
browse_output_folder_button.grid(row=1, column=2, padx=10, pady=5)

add_to_queue_button = tk.Button(root, text="Adicionar à fila", command=add_to_queue)
add_to_queue_button.grid(row=2, column=0, columnspan=3, padx=10, pady=5)

split_button = tk.Button(root, text="Dividir Vídeos da Fila", command=split_video_action)
split_button.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

queue_list = tk.Listbox(root, width=70, height=10)
queue_list.grid(row=4, column=0, columnspan=3, padx=10, pady=5)

progress_label = tk.Label(root, text="", pady=5)
progress_label.grid(row=5, column=0, columnspan=3)

progress_bar = Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

# Inicia o loop principal do aplicativo
root.mainloop()
