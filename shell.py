import cmd, sys
import editor as e
import reproductor as r
import almacenamiento as a
def es_numero(n):
	"""Recibe y devuelve un booleano si es flotante o entero\n
		->n(str):"""
	try:
		float(n)
		return True
	except ValueError:
		return False

def validar_parametro(argumento, max=None):
	"""Recibe un argumento y si cumple las condiciones lo devulve (int)\n
	Caso contrario devulve None.\n
		->argumento(str)\n
		->max(int): opcional\n"""
	if es_numero(argumento):
		argumento = float(argumento)
		if max:
			if argumento >= max:
				print("Ingrese un numero menor que ",max)
				return False
		return True
	else:
		print("Lo ingresado no es un numero")
		return False

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
		self.editor = e.Editor()

	def do_cargar(self,file):
		"""Carga la cancion desde el archivo.\n
		Reemplaza la cancion en edicion actual si es que la hay.\n
			-> file (str)"""
		self.editor = a.Almacenamiento(e.Editor()).cargar(file+".plp")

	def do_guardar(self,file):
		"""Guarda la cancion.\n
			-> file (str)"""
		a.Almacenamiento(self.editor).guardar(file+".plp")

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
		if validar_parametro(n):
			n = int(n)
			self.editor.avanzar(n)
			print("Marca: ",self.editor.index)

	def do_retrocederm (self, n):
		"""Retrocede N marcas de tiempo hacia atras. Si no hay mas mar\n
		cas hacia atras, no hace nada."""
		if validar_parametro(n):
			n = int(n)
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
			volumen = 1
		if validar_parametro(volumen) and validar_parametro(frecuencia):
			frecuencia = float(frecuencia)
			volumen = int(volumen)/100
		if funcion in self.editor.sound:
			self.editor.tracks.append((funcion, frecuencia, volumen))
			return
		print("La funcion ingresada no es valida")

	def do_trackdel(self, posicion=None):
		"""Elimina un track por numero.Si no se especifica uno elimina\n
		el ultimo tarck.\n
			-> posicion(str)"""	
		if posicion is None: #Aca si o si tuve que usar el is none
							 #Si usaba un ==, auqnue posicion no fuera un 
							 #None igual cumplia el if(aunque no quisieramos)
			self.editor.tracks.pop(len(self.editor.tracks) - 1)
			return
		if validar_parametro(posicion,len(self.editor.tracks)):
			posicion = int(posicion)
			self.editor.tracks.pop(posicion)
			print("Marca: ",self.editor.index)

	def do_markadd(self, duration):
		"""Agrega una marca de tiempo de la duracion establecida.\n
		Originalmente todos los tracks arrancan como deshabilitados.\n
		Siempre que se agrega una marca el cursor vuelve al inicio."""
		if validar_parametro(duration):
			duration = float(duration)
			self.editor.timeline.append( a._Mark(duration/100))
			if self.editor.index == 0:
				self.editor.cursor = self.editor.timeline.prim
	def do_markaddnext(self, duration):
		"""Igual que MARKADD pero la inserta luego de la marca en la \n
		cual esta actualmente el cursor."""
		if validar_parametro(duration):
			duration = float(duration)
			self.editor.timeline.insert(self.editor.index+1, a._Mark(duration/100))

	def do_markaddprev(self,duration):
		"""Igual que MARKADD pero la inserta antes de la marca en la \n
		cual esta actualmente el cursor."""
		if validar_parametro(duration):
			duration = float(duration)
			self.editor.timeline.insert(self.editor.index, a._Mark(duration/100))

	def do_trackon(self, indice):
		"""Habilita al track durante la marca de tiempo en la cual \n
		esta parada el cursor."""
		if validar_parametro(indice,len(self.editor.tracks)):
			indice = int(indice)
			if self.editor.timeline.len > 0:
				self.editor.cursor.dato.tracks[self.editor.tracks[indice]] = "#"
			else:
				print("No hay marcas.Agregue una antes de activar un track")

	def do_trackoff(self, indice):
		"""Operacion inversa del TRACKON."""
		if validar_parametro(indice,len(self.editor.tracks)):
			indice = int(indice)
			if self.editor.timeline.len > 0:
				self.editor.cursor.dato.tracks.pop(self.editor.tracks[indice],False)
			else:
				print("No hay marcas.Agregue una antes de activar un track")

	def do_play(self, x = None):
		"""Reproduce la marca en la que se encuentra el cursor actual\n
		mente."""
		r.Reproductor(self.editor).play(self.editor.timeline.len)

	def do_playall(self, x = None):
		"""Reproduce la cancion completa desde el inicio.""" 
		cursor_aux = self.editor.cursor
		self.editor.cursor = self.editor.timeline.prim
		r.Reproductor(self.editor).play(self.editor.timeline.len)
		self.editor.cursor = cursor_aux

	def do_playmarks (self, n):
		"""Reproduce las proximas N marcas desde la posicion actual del\n
		 cursor."""
		if validar_parametro(n):
			n = int(n)
			r.Reproductor(self.editor).play(n)
		
	def do_playsecond(self, n):
		"""Reproduce los proximos N segundos desde la posicion actual \n
		del cursor. Si alguna marca dura mas del tiempo restante, la \n
		reproduccion se corta antes."""
		if validar_parametro(n):
			n = int(n)
			r.Reproductor(self.editor).play(self.editor.timeline.len, n)

	def do_imprimir(self, x = None):
		"""Imprime la timeline que se tiene hasta el momento"""
		for i,(funcion, frecuencia, volumen) in enumerate(self.editor.tracks):
			print("{} Funcion: {} Frecuencia: {} Volumen: {}".format(i,funcion, frecuencia, volumen*100))
		print("N marca\tduracion  trackon")
		for i,mark in enumerate(self.editor.timeline):
			cadena = "{}\t[{}+]\t: ".format(i,mark.duration)
			for track in self.editor.tracks:
				cadena += mark.tracks.get(track,".")
			if self.editor.index == i:
				cadena += "<-"	#Señala el cursor
			print(cadena)
			
	def do_salir(self, x = None):
		"""Sale del programa"""
		print("Hasta luego")
		exit()