import cmd
class Shell(cmd.Cmd):
	intro = "Bienvenido a mi programa.\n Ingrese help o ? para listar los comandos.\n"
	prompt = "*>>"
	def do_COMANDO(self,parametros):
		"""Este metodo ejecuta un comando"""
	print("COMANDO - Parametros: ",parametros)
	def do_LOAD (self,file):
		"""Carga la canción desde el archivo. Reemplaza la canción en edición actual si es que la hay."""
		# Ejemplo :
		# LOAD last surprise.plp
		# Carga al modo de edición la canción “Last Surprise”. El cursor del
		# editor queda al inicio de la misma. Si no existe el archivo, se le debe
		# informar al usuario.
	def do_STORE (self,file):
		"""Guarda la canción."""
		# Ejemplo :
		# 	STORE shadow world.plp
		# 	Guarda la cancion en edicion actual con el nombre indicado.

	def do_STEP(self):
		"""Avanza a la siguiente marca de tiempo.Si no hay mas marcas hacia adelante, no hace nada."""
		# Ejemplo :
		# 	STEP
		# 	Eso avanza hacia la siguiente marca de tiempo. 

	def do_BACK(self):
		"""Retrocede a la anterior marca de tiempo.Si no hay mas marcas hacia atrás, no hace nada."""
		# Ejemplo :
		# BACK
		# Eso retrocede hacia la anterior marca de tiempo. 

	def do_STEPM (self, N):
		"""Avanza N marcas de tiempo hacia adelante. Si no hay mas marcas hacia adelante, no hace nada."""
		# Ejemplo :
		# 	STEPM 1
		# 	Eso avanza hacia la siguiente marca de tiempo.  Ídem que STEP.
		# Ejemplo :
		# 	STEPM 6
		# 	Eso avanza 6 marcas de tiempo hacia adelante. Si no hay suficientes
		# 	marcas hacia adelante, se queda al final.

	def do_BACKM (self, N):
		"""Retrocede N marcas de tiempo hacia atrás. Si no hay mas marcas hacia adelante, no hace nada."""
		# Ejemplo :
		# 	BACKM 1
		# 	Eso retrocede hacia la anterior marca de tiempo. Si no hay mas marcas
		# 	hacia atrás, no hace nada. Ídem que BACK
		# Ejemplo :
		# 	BACKM 5
		# 	Eso retrocede 6 marcas de tiempo. Si no suficientes marcas hacia atrás,
		# 	se queda al inicio.

	def do_TRACKADD (self, funcion, frecuencia, volumen=100):
		'''Agrega un track con el sonido indicado.'''
		# Ejemplo :
		# 	Suponiendo que se tiene la función sine dentro de las que ofrece el
		# 	programa:
		# 	TRACKADD sine 440 0.2
		# 	Eso agrega un track con un sonido generado por la función sine, a 440hz
		# 	y con un volumen del 20 %.

	def do_TRACKDEL(self, track):
		"""Elimina un track por numero."""
		# Ejemplo :
		# 	Suponiendo que se tienen 3 tracks:
		# 	TRACKDEL 2
		# 	TRACKDEL 2
		# 	Eso elimina primero el track en la posición 2, y luego elimina el track
		# 	que originalmente era el track 3, pero que luego del borrado ocupa la
		# 	posición 2.

	def do_MARKADD(self,duration):
		"""Agrega una marca de tiempo de la duración establecida. Originalmente
		todos los tracks arrancan como deshabilitados."""
		# Ejemplo :
		# 	MARKADD 2
		# 	Agrega una marca de tiempo de 2 segundos en la posición actual del
		# 	cursor.

	def do_MARKADDNEXT(self,duration):
		"""Igual que MARKADD pero la inserta luego de la marca en la cual esta
		actualmente el cursor."""
		
	def do_MARKADDPREV(self,duration):
		"""Igual que MARKADD pero la inserta antes de la marca en la cual esta
		actualmente el cursor."""

	def do_TRACKON(self, track):
		"""Habilita al track durante la marca de tiempo en la cual esta parada el
		cursor."""
		# Ejemplo :
		# 	Suponiendo que se tienen 3 tracks y la marca fue recién creada:
		# 	TRACKON 2
		# 	TRACKON 3
		# 	Habilita los tracks 2 y 3 de la marca. Cuando se reproduzca la misma,
		# 	se reproducirán los sonidos de los tracks 2 y 3 durante la duración de
		# 	la misma, pero no el del track 1.

	def do_TRACKOFF(self, track):
		"""Operación inversa del TRACKON."""
		# Ejemplo :
		# 	Suponiendo que se tiene 1 track:
		# 	TRACKON 1
		# 	TRACKOFF 1
		# 	Cuando se reproduce esta marca, no se reproduce el sonido del track1.

	def do_PLAY(self):
		"""Reproduce la marca en la que se encuentra el cursor actualmente."""
	def do_PLAYALL(self):
		"""Reproduce la canción completa desde el inicio."""
	def do_PLAYMARKS (self, N):
		"""Reproduce las próximas N marcas desde la posición actual del cursor."""
		# Ejemplo :
		# 	PLAYMARKS 5
		# 	

	def do_PLAYSECONDS (self, N):
		"""Reproduce la canción completa desde el inicio.\n
		Reproduce los próximos N segundos la posición actual del cursor.\n
		Si alguna marca dura mas del tiempo restante, la reproducción \n
		se corta antes."""
		# Ejemplo :
		# 	PLAYSECONDS 5
		
Shell().cmdloop()