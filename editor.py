import tda
import soundPlayer
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
		while cont < n and actual.prox:
			self.pila.apilar(actual)
			actual = actual.prox
			cont += 1
			self.index += 1
		self.cursor = actual

	def retroceder(self, n):
		"""Avanza N nodos sobre donde se encuentra el cursor.\n
		Si se llega al principio de la lista deja de retroceder.\n
			-> N (int): es la cantidad de pasos."""
		cont = 0
		while cont < n and not self.pila.esta_vacia():
			self.cursor = self.pila.desapilar()
			cont += 1
			self.index -= 1
