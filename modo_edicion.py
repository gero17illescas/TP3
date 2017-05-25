import cmd
import soundPlayer
import tda
class Editor():
	"""Representacion del editor, tiene las funciones de avanzar y \n
	retroceder asi como los atributos en lo que se almacena la \n
	informarcion de la cancion."""
	def __init__(self):
		"""Constructor de Editor"""
		self.timeline = tda.ListaEnlazada()		#marks
		self.cursor = self.timeline.prim		#hace referencia al mark actual
		self.index = 0							#indica en que indice se encuntra el cursor
		self.pila = tda.Pila()					#aux para retroceder
		self.tracks = []		#datos de los tracks o canales que tendra la cancion
		self.sound = {
			"sine": soundPlayer.SoundFactory.get_sine_sound,
			"squa": soundPlayer.SoundFactory.get_square_sound,
			"sile": soundPlayer.SoundFactory.get_silence_sound,
			"tria": soundPlayer.SoundFactory.get_triangular_sound,
			"nois": soundPlayer.SoundFactory.get_noise_sound,}
	def avanzar(self, N):
		"""Avanza N nodos sobre donde se encuentra el cursor.\n
		Si se llega al final de la lista deja de avanzar.\n
			-> N (int): es la cantidad de pasos."""
		self.index += N
		cont = 0
		actual = self.cursor #a partir de donde estamos
		while cont < N and actual is not None:
			actual = actual.prox
			self.pila.apilar(actual)
			cont += 1
		self.cursor = actual
	def retroceder(self, N):
		"""Avanza N nodos sobre donde se encuentra el cursor.\n
		Si se llega al principio de la lista deja de retroceder.\n
			-> N (int): es la cantidad de pasos."""
		self.index -= N
		cont = 0
		while cont < N and not self.pila.esta_vacia():
			self.cursor = self.pila.desapilar()
			cont += 1
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
		"""Guarda la cancion.\n
			-> file (str)"""
		try:
			with open(file,"w") as f:
				f.write("FIELD,DATA\n")						#cabecera
				f.write("C,{}\n".format(len(editor.tracks)))	#Escribimos la cantidad de canales
				for i in range(len(editor.tracks)):			#Escribimos la info de los canales
					(funcion, frecuencia, volumen) = editor.tracks[i]
					f.write("C,{}|{}|{}\n".format(funcion, frecuencia, volumen))
				duracion_anterior = 0
				for mark in editor.timeline:
					if mark["duracion"] != duracion_anterior:
						duracion_anterior = mark.get("duracion")
						f.write("T,{}\n".format(duracion_anterior))
					cadena_mark = ""
					for i in range(len(editor.tracks)):
						cadena_mark += mark.get(i,".")
					f.write(cadena_mark+"\n")
		except IOError :
			raise IOError ("Hubo un problema con el archivo")

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
	def do_TRACKADD (self, funcion, frecuencia=440, volumen=100):
		"""Agrega un track con el sonido indicado.\n
			-> funcion (str): tipo de sonido\n
			-> frecuencia(int)\n
			-> volumen(int)\n"""
		editor.tracks.append((funcion, frecuencia, volumen))
	def do_TRACKDEL(self, posicion=None):
		"""Elimina un track por numero.Si no se especifica uno elimina\n
		el ultimo tarck.\n
			-> posicion(int)"""
		if posicion<0 or posicion>len(editor.tracks):
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
		print(editor.cursor.dato)
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
		if editor.timeline.len == 0:
			raise ValueError ("No hay marcas para reproducir")
		reproductor = soundPlayer.SoundPlay(len(editor.tracks))
		actual = editor.cursor
		while actual is not None:
			lista_aux = []
			lista_tracks = []
			mark = actual.dato
			duracion = mark.pop("duracion")
			for i in range(len(editor.tracks)):
				(funcion, frecuencia, volumen) = editor.tracks[i]
				if mark[i]=="#":
					lista_aux.append(editor.sound.get(funcion)(frecuencia, volumen))
			reproductor.play_sounds(lista_aux,duracion)
			mark["duracion"]=duracion
	def do_PLAYSECONDS (self, N):
		"""Reproduce los proximos N segundos desde la posicion actual \n
		del cursor. Si alguna marca dura mas del tiempo restante, la \n 
		reproduccion se corta antes."""
		# Ejemplo :
		# 	PLAYSECONDS 5
	def do_PRINT(self):
		for mark in editor.timeline:
			print(mark)
Shell().cmdloop()
