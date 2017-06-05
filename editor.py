import cmd, sys
import soundPlayer
import tda
import csv
from os.path import isfile
def es_entero(n):
	"""Recibe y devuelve un booleano si es \n
		->n(int ó str): es el valor validarse como entero"""
	if type(n) == int and n >= 0:
		return True
	return n.isdigit() and int(n) >= 0
def validar_parametro(argumento, max=None):
	"""Recibe un argumento y si cumple las condiciones lo devulve (int)\n
	Caso contrario devulve None.\n
		->argumento(str)\n
		->max(int): opcional\n"""
	if es_entero(argumento):
		argumento = int(argumento)
		if max is not None:
			if argumento < max:
				return argumento
			else:
				print("Se ingreso un numero mayor que ",max)
				return None
		else:
			return argumento
	else:
		print("Lo ingresado no es un numero")
		return None

class _Mark():
	"""Representacion de una marca."""
	def __init__(self, duracion):
		"""Constructor"""
		self.duracion = duracion
		self.tracks = {}

class Editor:
	"""Representacion del editor, tiene las funciones de avanzar y \n
	retroceder asi como los atributos en lo que se almacena la \n
	informarcion de la cancion."""

	def __init__(self):
		"""Constructor de Editor"""
		self.timeline = tda.ListaEnlazada()		#marks
		self.cursor = self.timeline.prim		#hace referencia al mark actual
		self.index = 0							#indica en que indice se encuntra el cursor
		self.pila = tda.Pila()					#aux para retroceder
		self.tracks = []						#datos de los tracks o canales que tendra la cancion
		self.sound = {
			"sine": soundPlayer.SoundFactory.get_sine_sound,
			"squa": soundPlayer.SoundFactory.get_square_sound,
			"sile": soundPlayer.SoundFactory.get_silence_sound,
			"tria": soundPlayer.SoundFactory.get_triangular_sound,
			"nois": soundPlayer.SoundFactory.get_noise_sound,}
			
	def avanzar(self, n):
		"""Avanza N nodos sobre donde se encuentra el cursor.\n
		Si se llega al final de la lista deja de avanzar.\n
			-> N (int): es la cantidad de pasos."""
		cont = 0
		actual = self.cursor
		while cont < n and actual.prox is not None:
			self.index += n
			self.pila.apilar(actual)
			actual = actual.prox
			cont += 1
		self.cursor = actual

	def retroceder(self, n):
		"""Avanza N nodos sobre donde se encuentra el cursor.\n
		Si se llega al principio de la lista deja de retroceder.\n
			-> N (int): es la cantidad de pasos."""
		self.index -= n
		cont = 0
		while cont < n and not self.pila.esta_vacia():
			self.cursor = self.pila.desapilar()
			cont += 1

class Reproductor:
	"""Clase encargada de reproducir la cancion."""

	def __init__(self,editor):
		"""Constructor"""
		self.editor = editor

	def play(self,marcas,segundos = None):
		"""Reproduce la cancion.\n
			->marcas(int): es la cantidad de marcas que se reproduciran.\n
			->segundos(int): es la cantidad de segundos que se reproduciran.\n
			Es un parametro opcional."""
		if self.editor.timeline.len == 0:
			print("No hay marcas para reproducir")
		reproductor = soundPlayer.SoundPlayer(len(self.editor.tracks))
		actual = self.editor.cursor
		cont_marcas = 0
		cont_seg = 0
		while actual is not None and cont_marcas < marcas:
			mark = actual.dato
			if segundos:
				if cont_seg == segundos:
					return
				cont_seg += mark.duracion
			lista_aux = []
			for i in range(len(self.editor.tracks)):
				(funcion, frecuencia, volumen) = self.editor.tracks[i]
				if mark.tracks.get((funcion, frecuencia, volumen),False)=="#":
					lista_aux.append(self.editor.sound.get(funcion)(frecuencia, volumen))
			reproductor.play_sounds(lista_aux,mark.duracion)
			actual = actual.prox
			cont_marcas += 1

class Almacenamiento():
	"""Clase encargada de guardar y cargar el archivo .plp"""
	def __init__(self, editor):
		"""Constructor"""
		self.editor = editor

	def guardar(self,file):
		"""Guarda el archivo con el nombre ingresado.\n
			->file(str): nombre del archivo"""
		with open(file,"w") as f:
			f.write("FIELD,DATA\n")							#cabecera
			f.write("C,{}\n".format(len(self.editor.tracks)))	#Escribimos la cantidad de canales
			for (funcion, frecuencia, volumen) in self.editor.tracks:				#Escribimos la info de los canales
				f.write("C,{}|{}|{}\n".format(funcion, frecuencia, volumen))
			duracion_anterior = 0
			for mark in self.editor.timeline:
				if mark.duracion != duracion_anterior:
					duracion_anterior = mark.duracion
					f.write("T,{}\n".format(mark.duracion))
				cadena = ""
				for track in self.editor.tracks:
					cadena += mark.tracks.get(track,".")
				f.write("N,"+cadena+"\n")

	def cargar(self, file):
		"""Carga el archivo con el nombre ingresado.
			->file(str): nombre del archivo"""
		if not isfile(file):
			print("El archivo no existe")
		else:
			self.editor = Editor()
			with open(file,"r") as f:
				datos_csv = csv.reader(f)
				next(datos_csv)
				cantidad_canales = int(next(datos_csv)[1])
				#leemos los canales
				for i in range(cantidad_canales):
					track = next(datos_csv)[1].split("|")
					funcion = track[0]
					frecuencia = float(track[1])
					volumen = float(track[2])
					self.editor.tracks.append((funcion, frecuencia, volumen))
				#leemos las marcas
				for mark in datos_csv:
					if mark[0] == "T":
						duracion = float(mark[1])
						continue
					marca = _Mark(duracion)
					for i in range(cantidad_canales):
						if mark[1][i] == "#":
							marca.tracks[self.editor.tracks[i]] = "#"
					self.editor.timeline.append(marca)
			self.editor.cursor = self.editor.timeline.prim
			return self.editor

MENSAJE=(" Bienvenido a mi FIUBA Music editor.\n"+
" Antes de activar los tracks debe crear al menos una marca.\n"+
" Cuando carga un archivo elimina todo lo que este en memoria.\n"+
" Ingrese help o ? para listar los comandos.\n")
class Shell(cmd.Cmd):
	intro = MENSAJE
	prompt = "*>>"
	def __init__(self):
		"""Constructor de la clase"""
		super().__init__()
		self.editor = Editor()
		self.almacenamiento = Almacenamiento(self.editor)

	def do_cargar(self,file):
		"""Carga la cancion desde el archivo.\n
		Reemplaza la cancion en edicion actual si es que la hay.\n
			-> file (str)"""
		self.editor = Almacenamiento(self.editor).cargar(file+".plp")

	def do_guardar(self,file):
		"""Guarda la cancion.\n
			-> file (str)"""
		Almacenamiento(self.editor).guardar(file+".plp")

	def do_avanzar(self,x=None):
		"""Avanza a la siguiente marca de tiempo.Si no hay mas marcas \n
		hacia adelante, no hace nada."""
		self.editor.avanzar(1)
		print("Marca: ",self.editor.index)

	def do_retroceder(self,x = None):
		"""Retrocede a la anterior marca de tiempo.Si no hay mas marcas\n
		hacia atras, no hace nada."""
		self.editor.retroceder(1)
		print("Marca: ",self.editor.index)

	def do_avanzarm (self, n):
		"""Avanza N marcas de tiempo hacia adelante. Si no hay mas mar\n
		cas hacia adelante, no hace nada."""
		n=validar_parametro(n) 
		if n:
			self.editor.avanzar(n)
			print("Marca: ",self.editor.index)

	def do_retrocederm (self, n):
		"""Retrocede N marcas de tiempo hacia atras. Si no hay mas mar\n
		cas hacia atras, no hace nada."""
		n=validar_parametro(n) 
		if n:
			self.editor.retroceder(n)
			print("Marca: ",self.editor.index)

	def do_trackadd (self, parametros):
		"""Agrega un track con el sonido indicado.\n
			->parametro(str)"""
		lista_p = parametros.split(" ")
		if len(lista_p)== 3:
			funcion, frecuencia, volumen= lista_p[0], lista_p[1], lista_p[2]
		else:
			funcion, frecuencia = lista_p[0], lista_p[1]
			volumen = 100
		frecuencia = validar_parametro(frecuencia)
		volumen = validar_parametro(volumen)
		if funcion in self.editor.sound:
			self.editor.tracks.append((funcion, frecuencia, volumen))
			return
		print("La funcion ingresada no es valida")

	def do_trackdel(self, posicion=None):
		"""Elimina un track por numero.Si no se especifica uno elimina\n
		el ultimo tarck.\n
			-> posicion(str)"""		
		if posicion:
			posicion=validar_parametro(posicion)
			if posicion is not None:
				self.editor.tracks.pop(posicion)
				print("Marca: ",self.editor.index)
		else:
			self.editor.tracks.pop(len(self.editor.tracks) - 1)
			
	def do_markadd(self, duration):
		"""Agrega una marca de tiempo de la duracion establecida.\n
		Originalmente todos los tracks arrancan como deshabilitados.\n
		Siempre que se agrega una marca el cursor vuelve al inicio."""
		duration = validar_parametro(duration) 
		if duration:
			self.editor.timeline.append( _Mark(duration/100))
			self.editor.cursor = self.editor.timeline.prim

	def do_markaddnext(self, duration):
		"""Igual que MARKADD pero la inserta luego de la marca en la \n
		cual esta actualmente el cursor."""
		duration = validar_parametro(duration) 
		if duration:
			self.editor.timeline.insert(self.editor.index+1,_Mark(duration/100))

	def do_markaddprev(self,duration):
		"""Igual que MARKADD pero la inserta antes de la marca en la \n
		cual esta actualmente el cursor."""
		duration = validar_parametro(duration) 
		if duration:
			self.editor.timeline.insert(self.editor.index,_Mark(duration/100))

	def do_trackon(self, indice):
		"""Habilita al track durante la marca de tiempo en la cual \n
		esta parada el cursor."""
		indice = validar_parametro(indice,len(self.editor.tracks)) 
		if indice is not None:
			self.editor.cursor.dato.tracks[self.editor.tracks[indice]] = "#"

	def do_trackoff(self, indice):
		"""Operacion inversa del TRACKON."""
		duration = validar_parametro(indice,len(self.editor.tracks)) 
		if duration is not None:
			self.editor.cursor.dato.tracks.pop(self.editor.tracks[indice])

	def do_play(self, x = None):
		"""Reproduce la marca en la que se encuentra el cursor actual\n
		mente."""
		Reproductor(self.editor).play(self.editor.timeline.len)

	def do_playall(self, x = None):
		"""Reproduce la cancion completa desde el inicio.""" 
		cursor_aux = self.editor.cursor
		self.editor.cursor = self.editor.timeline.prim
		Reproductor(self.editor).play(self.editor.timeline.len)
		self.editor.cursor = cursor_aux

	def do_playmarks (self, n):
		"""Reproduce las proximas N marcas desde la posicion actual del\n
		 cursor."""
		n = validar_parametro(n)
		if n:
			Reproductor(self.editor).play(n)
		
	def do_playsecond(self, n):
		"""Reproduce los proximos N segundos desde la posicion actual \n
		del cursor. Si alguna marca dura mas del tiempo restante, la \n
		reproduccion se corta antes."""
		n = validar_parametro(n)
		if n:
			Reproductor(self.editor)(self.editor.timeline.len,n)

	def do_imprimir(self, x = None):
		"""Imprime la timeline que se tiene hasta el momento"""
		for (funcion, frecuencia, volumen) in self.editor.tracks:
			print("Funcion: {} Frecuencia: {} Volumen: {}".format(funcion, frecuencia, volumen))
		cont = 0
		for mark in self.editor.timeline:
			cadena = "["+str(mark.duracion)+"]: "
			for track in self.editor.tracks:
				cadena += mark.tracks.get(track,".")
			if self.editor.index == cont:
				cadena += "<-"	#Señala el cursor
			cont += 1
			print(cadena)
	def do_salir(self, x = None):
		"""Sale del programa"""
		print("Hasta luego")
		exit()
def main():
	"""Funcion principal"""
	Shell().cmdloop()
main()