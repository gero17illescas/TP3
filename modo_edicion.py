import cmd
import soundPlayer
import tda
class Editor():
	def __init__(self):
		self.timeline = tda.ListaEnlazada()		#marks
		self.cursor = self.timeline.prim		#hace referencia al mark actual
		self.index = 0							#indica en que indice se encuntra el cursor
		self.pila = tda.Pila()					#aux para retroceder
		self.tracks = tda.ListaEnlazada()		#tracks o canales que tendra la cancion
		self.sound = {"sine": soundPlayer.SoundFactory.get_sine_sound,
			 "squa": soundPlayer.SoundFactory.get_square_sound,
			 "sile": soundPlayer.SoundFactory.get_silence_sound,
			 "tria": soundPlayer.SoundFactory.get_triangular_sound,
			 "nois": soundPlayer.SoundFactory.get_noise_sound,}
	def avanzar(self, N):
		self.index += N 
		cont = 0
		actual = self.cursor #a partir de donde estamos
		while cont < N and actual is not None:
			actual = actual.prox
			self.pila.apilar(actual)
			cont += 1 
		self.cursor = actual
	def retroceder(self, N):
		self.index -= N
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
		"""Avanza a la siguiente marca de tiempo.Si no hay mas marcas \n
		hacia adelante, no hace nada."""
		do_STEPM(1)
	def do_BACK(self):
		"""Retrocede a la anterior marca de tiempo.Si no hay mas marcas\n
		hacia atras, no hace nada."""
		do_BACKM(1)
	def do_STEPM (self, N):
		"""Avanza N marcas de tiempo hacia adelante. Si no hay mas mar\n
		cas hacia adelante, no hace nada."""
		editor.avanzar(int(N))	#TENGO QUE CONVERTIR A ENTERO, ITERO SOBRE UNA CADENA
	def do_BACKM (self, N):
		"""Retrocede N marcas de tiempo hacia atras. Si no hay mas mar\n
		cas hacia atras, no hace nada."""
		editor.retroceder(int(N))
	def do_TRACKADD (self, funcion, frecuencia=400, volumen=100):
		"""Agrega un track con el sonido indicado.\n
			-> funcion (str): tipo de sonido\n
			-> frecuencia(int)\n
			-> volumen(int)\n"""
		editor.tracks.append(editor.sound.get(funcion)(frecuencia,volumen))
	def do_TRACKDEL(self, posicion=None):
		"""Elimina un track por numero.Si no se especifica uno elimina\n
		el ultimo tarck.\n
			-> posicion(int)"""
		if posicion<0 or posicion>editor.tracks.len:
			raise IndexError ("La posicion ingresada no corresponde a un track ingresado")
		editor.tracks.pop(posicion)
	def do_MARKADD(self,duration):
		"""Agrega una marca de tiempo de la duracion establecida.\n
		Originalmente todos los tracks arrancan como deshabilitados."""
		editor.timeline.append({"duracion":duration})
	def do_MARKADDNEXT(self, duration):
		"""Igual que MARKADD pero la inserta luego de la marca en la \n
		cual esta actualmente el cursor."""
		editor.timeline.insert(editor.index+1,{"duracion":duration})
	def do_MARKADDPREV(self,duration):
		"""Igual que MARKADD pero la inserta antes de la marca en la \n
		cual esta actualmente el cursor."""
		editor.timeline.insert(editor.index+-1,{"duracion":duration})
	def do_TRACKON(self, track):
		"""Habilita al track durante la marca de tiempo en la cual \n
		esta parada el cursor."""
		editor.cursor.dato[track]="#"
	def do_TRACKOFF(self, track):
		"""Operacion inversa del TRACKON."""
		editor.cursor.dato[track]="."
	def do_PLAY(self):
		"""Reproduce la marca en la que se encuentra el cursor actual\n
		mente."""
		do_PLAY(editor.timeline.len-editor.index)
	def do_PLAYALL(self):
		"""Reproduce la cancion completa desde el inicio."""
		cursor_aux = editor.cursor
		editor.cursor = editor.timeline.prim
		do_PLAY()
		editor.cursor = cursor_aux
	def do_PLAYMARKS (self, N):
		"""Reproduce las proximas N marcas desde la posicion actual del\n
		 cursor."""
		reproductor = soundPlayer.SoundPlayer(editor.tracks.len)
		actual = editor.cursor
		while actual is not None:
			lista_aux = []
			mark = actual.dato
			duracion = mark.pop("duracion")
			for i in range(editor.tracks.len):
				if mark[i]=="#":
					lista_aux.append(editor.tracks[i])
			reproductor.play_sounds(lista_aux,duracion)
			mark["duracion"]=duracion
	def do_PLAYSECONDS (self, N):
		"""Reproduce la cancion completa desde el inicio.\n
		Reproduce los proximos N segundos desde la posicion actual del cursor.\n
		Si alguna marca dura mas del tiempo restante, la reproduccion \n
		se corta antes."""
		# Ejemplo :
		# 	PLAYSECONDS 5
	def do_PRINT(self):
		for mark in editor.timeline:
			print(mark)
Shell().cmdloop()





