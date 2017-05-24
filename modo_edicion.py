import cmd
import soundPlayer
import tda
class Editor():
	def __init__(self):
		self.timeline = tda.ListaEnlazada()
		self.cursor = None
		self.pila = tda.Pila()
		self.tracks = tda.ListaEnlazada()
		self.sound = {"sine": soundPlayer.SoundFactory.get_sine_sound,
			 "squa": soundPlayer.SoundFactory.get_square_sound,
			 "sile": soundPlayer.SoundFactory.get_silence_sound,
			 "tria": soundPlayer.SoundFactory.get_triangular_sound,
			 "nois": soundPlayer.SoundFactory.get_noise_sound,}
	def avanzar(self, N):
		N = int(N)
		cont = 0
		self.cursor = self.timeline.prim
		while cont < N:
			self.cursor = self.timeline.prim.prox
			self.pila.apilar(self.cursor)
	def retroceder(self, N):
		if not self.pila.esta_vacia():
			for _ in range (N):
				self.cursor = self.pila.desapilar()
editor = Editor()
class Shell(cmd.Cmd):
	intro = "Bienvenido a mi programa.\n Ingrese help o ? para listar los comandos.\n"
	prompt = "*>>"
	def do_LOAD (self,file):
		"""Carga la cancion desde el archivo. Reemplaza la cancion en edicion actual si es que la hay."""
		# Ejemplo :
		# LOAD last surprise.plp
		# Carga al modo de edicion la cancion “Last Surprise”. El cursor del
		# editor queda al inicio de la misma. Si no existe el archivo, se le debe
		# informar al usuario.
	def do_STORE (self,file):
		"""Guarda la cancion."""
		# Ejemplo :
		# 	STORE shadow world.plp
		# 	Guarda la cancion en edicion actual con el nombre indicado.

	def do_STEP(self):
		"""Avanza a la siguiente marca de tiempo.Si no hay mas marcas hacia adelante, no hace nada."""
		do_STEPM(1)
	def do_BACK(self):
		"""Retrocede a la anterior marca de tiempo.Si no hay mas marcas hacia atras, no hace nada."""
		do_BACKM(1)
	def do_STEPM (self, N):
		"""Avanza N marcas de tiempo hacia adelante. Si no hay mas marcas hacia adelante, no hace nada."""
		
		editor.avanzar(int(N))
	def do_BACKM (self, N):
		"""Retrocede N marcas de tiempo hacia atras. Si no hay mas marcas hacia atras, no hace nada."""
		editor.retroceder(int(N))
	def do_TRACKADD (self, funcion, frecuencia, volumen=100):
		"""Agrega un track con el sonido indicado.\n
			-> funcion (str): tipo de sonido\n
			-> frecuencia(int)\n
			-> volumen(int)\n"""
		editor.tracks.append(editor.sound.get(funcion)(frecuencia,volumen))
	def do_TRACKDEL(self, posicion):
		"""Elimina un track por numero.Si no se especifica uno elimina\n
		el ultimo tarck.\n
			-> posicion(int)"""
		tracks.pop(posicion)
	def do_MARKADD(self,duration):
		"""Agrega una marca de tiempo de la duracion establecida.\n
		Originalmente todos los tracks arrancan como deshabilitados."""
		editor.timeline.append({"duracion":duration})
	def do_MARKADDNEXT(self, duration):
		
		"""Igual que MARKADD pero la inserta luego de la marca en la \n
		cual esta actualmente el cursor."""
		
	def do_MARKADDPREV(self,duration):
		"""Igual que MARKADD pero la inserta antes de la marca en la \n
		cual esta actualmente el cursor."""

	def do_TRACKON(self, track):
		"""Habilita al track durante la marca de tiempo en la cual \n
		esta parada el cursor."""
		editor.cursor.dato[track]="#"

	def do_TRACKOFF(self, track):
		"""Operacion inversa del TRACKON."""
		editor.cursor.dato[track]="."

	def do_PLAY(self):
		"""Reproduce la marca en la que se encuentra el cursor actualmente."""
	def do_PLAYALL(self):
		"""Reproduce la cancion completa desde el inicio."""
	def do_PLAYMARKS (self, N):
		"""Reproduce las proximas N marcas desde la posicion actual del cursor."""
		# Ejemplo :
		# 	PLAYMARKS 5


	def do_PLAYSECONDS (self, N):
		"""Reproduce la cancion completa desde el inicio.\n
		Reproduce los proximos N segundos la posicion actual del cursor.\n
		Si alguna marca dura mas del tiempo restante, la reproduccion \n
		se corta antes."""
		# Ejemplo :
		# 	PLAYSECONDS 5
	def do_PRINT(self):
		for mark in editor.timeline:
			print("duracion",mark(0))
			print(mark(1).get("."))
Shell().cmdloop()





