import os
import sys

if sys.platform.startswith("linux"):
    os.environ["SDL_AUDIODRIVER"] = "pulseaudio"

import pygame
import tkinter as tk
from tkinter import filedialog

pygame.mixer.init(frequency=44100, size=-16, channels=2)

music_loaded = False
music_length = 0
dragging = False

def play(start=0):
    if music_loaded:
        pygame.mixer.music.play(start=start)

def pause():
    if music_loaded:
        pygame.mixer.music.pause()

def resume():
    if music_loaded:
        pygame.mixer.music.unpause()

def stop():
    if music_loaded:
        pygame.mixer.music.stop()
        progress.set(0)

def set_volume(val):
    pygame.mixer.music.set_volume(float(val))

def open_file():
    global music_loaded, music_length
    file = filedialog.askopenfilename(
        filetypes=[("MP3 Files", "*.mp3")]
    )
    if file:
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        music_loaded = True

        music_label.config(text=os.path.basename(file))

        music_length = pygame.mixer.music.get_length()

        progress.config(to=music_length)

def start_drag(event):
    global dragging
    dragging = True

def end_drag(event):
    global dragging
    if music_loaded:
        pos = progress.get()
        pygame.mixer.music.play(start=pos)
    dragging = False

def update_progress():
    if music_loaded and pygame.mixer.music.get_busy() and not dragging:
        pos = pygame.mixer.music.get_pos() / 1000
        real_pos = start_offset + pos

        if real_pos < music_length:
            progress.set(real_pos)
    root.after(300, update_progress)

# ---------------- GUI ----------------

root = tk.Tk()
root.title("MP3 Player")
root.geometry("450x350")
root.resizable(False, False)

music_label = tk.Label(root, text="Nenhuma música", wraplength=320)
music_label.pack(pady=10)

progress = tk.Scale(
    root, from_=0, to=100,
    orient="horizontal", length=320,
    showvalue=False
)
progress.pack(pady=10)

progress.bind("<Button-1>", start_drag)
progress.bind("<ButtonRelease-1>", end_drag)

controls = tk.Frame(root)
controls.pack(pady=10)

tk.Button(controls, text="Play", command=play, width=8).grid(row=0, column=0, padx=3)
tk.Button(controls, text="Pause", command=pause, width=8).grid(row=0, column=1, padx=3)
tk.Button(controls, text="Continuar", command=resume, width=8).grid(row=0, column=2, padx=3)
tk.Button(controls, text="Stop", command=stop, width=8).grid(row=0, column=3, padx=3)

tk.Button(root, text="Abrir MP3", command=open_file, width=20).pack(pady=10)

tk.Label(root, text="Volume").pack()
volume = tk.Scale(
    root, from_=0, to=1,
    resolution=0.05,
    orient="horizontal",
    command=set_volume,
    length=200
)
volume.set(0.7)
volume.pack(pady=10)

update_progress()
root.mainloop()