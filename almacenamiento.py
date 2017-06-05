import csv
from os.path import isfile
class _Mark():
	"""Representacion de una marca."""
	def __init__(self, duracion):
		"""Constructor"""
		self.duracion = duracion
		self.tracks = {}
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
