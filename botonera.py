import tkinter as tk
from tkinter import ttk
import pygame,time
from pathlib import Path
import re

# Inicializar pygame mixer
pygame.mixer.init()

# Ruta específica de la carpeta de sonidos
sonidos_path = Path(r"C:\Users\clonador\Desktop\sonidos")

class ReproductorAudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor de Sonidos")
        self.reproduciendo = False
        self.archivo_actual = None
        self.botones = []

        self.frame_busqueda = ttk.Frame(root, padding="10")
        self.frame_busqueda.grid(row=0, column=0, sticky=(tk.W, tk.E))

        self.entrada_busqueda = ttk.Entry(self.frame_busqueda)
        self.entrada_busqueda.grid(row=0, column=0, padx=(0, 5))
        self.entrada_busqueda.bind('<KeyRelease>', self.filtrar_botones)

        ttk.Button(self.frame_busqueda, text="Buscar", command=self.filtrar_botones).grid(row=0, column=1)

        self.frame_botones = ttk.Frame(root, padding="10")
        self.frame_botones.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.etiqueta_estado = ttk.Label(root, text="")
        self.etiqueta_estado.grid(row=2, column=0, pady=5)

        self.crear_botones()

    def crear_botones(self):
        archivos = list(sonidos_path.glob("*.mp3"))
        print(f"Archivos encontrados: {len(archivos)}")
        if not archivos:
            self.etiqueta_estado.config(text="No se encontraron archivos MP3 en la carpeta especificada.")
            return
        for archivo in archivos:
            boton = ttk.Button(self.frame_botones, text=archivo.stem, command=lambda f=archivo: self.toggle_reproduccion(f))
            self.botones.append((boton, archivo))
            print(f"Botón creado para: {archivo.stem}")
        # Inicialmente, ocultamos todos los botones
        for boton, _ in self.botones:
            boton.grid_remove()

    def filtrar_botones(self, event=None):
        busqueda = re.escape(self.entrada_busqueda.get().lower())
        print(f"Buscando: '{busqueda}'")
        botones_visibles = 0
        row = 0
        col = 0
        for boton, archivo in self.botones:
            nombre_archivo = archivo.stem.lower()
            if re.search(busqueda, nombre_archivo):
                boton.grid(row=row, column=col, padx=5, pady=5)
                botones_visibles += 1
                col += 1
                if col > 2:
                    col = 0
                    row += 1
            else:
                boton.grid_remove()
        print(f"Botones visibles después de filtrar: {botones_visibles}")
        self.actualizar_grid_botones()

    def toggle_reproduccion(self, archivo):
        if self.reproduciendo and self.archivo_actual == archivo:
            self.detener_audio()
        else:
            self.reproducir_audio(archivo)

    def reproducir_audio(self, archivo):
        self.detener_audio()
        try:
            pygame.mixer.music.load(str(archivo))
            pygame.mixer.music.play()
            self.reproduciendo = True
            self.archivo_actual = archivo
            self.etiqueta_estado.config(text=f"Reproduciendo: {archivo.name}")
        except pygame.error as e:
            self.etiqueta_estado.config(text=f"Error al reproducir: {str(e)}")

    def detener_audio(self):
        if self.reproduciendo:
            pygame.mixer.music.stop()
            self.reproduciendo = False
            self.archivo_actual = None
            self.etiqueta_estado.config(text="Audio detenido")

    def actualizar_barra_progreso(self):
        while self.reproduciendo:
            if not self.actualizando_barra and pygame.mixer.music.get_busy():
                pos = pygame.mixer.music.get_pos() / 1000
                self.barra_progreso.set(pos / self.duracion * 100)
            elif not pygame.mixer.music.get_busy():
                self.detener_audio()
            time.sleep(0.1)

    def actualizar_posicion(self, value):
        if self.reproduciendo:
            self.actualizando_barra = True
            pos = float(value) / 100 * self.duracion
            pygame.mixer.music.stop()
            pygame.mixer.music.play(start=pos)
            self.actualizando_barra = False

root = tk.Tk()
app = ReproductorAudio(root)
root.mainloop()
