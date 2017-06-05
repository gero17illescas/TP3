import soundPlayer
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
