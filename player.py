import os
os.environ["SDL_AUDIODRIVER"] = "pulseaudio"

import pygame
import tkinter as tk
from tkinter import filedialog

pygame.mixer.init()

def play():
    pygame.mixer.music.play()

def pause():
    pygame.mixer.music.pause()

def resume():
    pygame.mixer.music.unpause()

def stop():
    pygame.mixer.music.stop()

def open_file():
    file = filedialog.askopenfilename(
        filetypes=[("MP3 Files", "*.mp3")]
    )
    if file:
        pygame.mixer.music.load(file)
        play()

root = tk.Tk()
root.title("MP3 Player")
root.geometry("300x200")

tk.Button(root, text="Abrir MP3", command=open_file).pack(pady=5)
tk.Button(root, text="Play", command=play).pack(pady=5)
tk.Button(root, text="Pause", command=pause).pack(pady=5)
tk.Button(root, text="Continuar", command=resume).pack(pady=5)
tk.Button(root, text="Stop", command=stop).pack(pady=5)

root.mainloop()
