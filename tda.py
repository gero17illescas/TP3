class _Nodo:
	'''Representacion de un nodo'''
	def __init__(self, dato, prox=None):
		"""Constructor del nodo"""
		self.dato = dato
		self.prox = prox

class ListaEnlazada:
	"""Clase la lista enlazada"""
	def __init__(self):
		"""Constructor de la lista enlazada"""
		self.prim = None
		self.len = 0
	def __iter__(self):
		return _IteradorListaEnlazada(self.prim)
	def __str__(self):
		lista = []
		for dato in self:
			lista.append(dato)
		return str(lista)
	def append(self, dato):
		"""Agrega el dato al final de la lista"""
		self.insert(self.len, dato)
	def insert(self, i, dato):
		"""Inserta el dato recibido en la posicion indicada\n
			->i (int): indice, no puede ser cero o mayor a la longitud de la lista\n
			->dato(): valor a agregar"""
		if i < 0 or i > self.len:
			raise IndexError
		nodo = _Nodo(dato)
		self.len += 1
		if i==0:
			nodo.prox = self.prim
			self.prim = nodo
		else:
			actual = self.prim
			for j in range(1,i):
				actual = actual.prox
			nodo.prox = actual.prox
			actual.prox = nodo
	def extend(self, otra):
		"""Conecta dos listas, manteniendo la segunda independiente"""
		if otra.len==0:
			return 
		if self.prim is None:
			self.prim=_Nodo(otra.prim.dato)
			aux = otra.prim.prox
		else:
			aux = otra.prim
		actual = self.prim
		while actual.prox is not None:
			actual = actual.prox
		while aux is not None:
			actual.prox = _Nodo (aux.dato)
			actual = actual.prox
			aux = aux.prox
	def invert(self):
		actual=self.prim
		anterior=None
		while actual is not None:
			prox=actual.prox
			actual.prox = anterior
			anterior = actual
			actual = prox
		self.prim=anterior
	def remove(self,elemento):
		"""Quita de la lista el elemento en su primera aparicion, si se encuentra.\n
		De no encontrarse en la lista,se produce un error. Si la lista esta vacia,\n
		levanta un error."""
		if self.len == 0:
			raise ValueError ("La lista esta vacia")
		if self.prim.dato == elemento:
			self.prim = self.prim.prox
			self.len -= 1
		else:
			actual = self.prim
			while actual.prox is not None:
				siguiente = actual.prox
				if siguiente.dato == elemento:
					actual.prox=siguiente.prox
					self.len -= 1
					return
				actual = actual.prox
		raise ValueError ("No se encontro tal elemento en la lista")
	def pop(self,posicion = None):
		"""Elimina el elemento en la posicion ingresada, y lo devuelve.\n
			-> posicion (int): posicion a eliminar \n"""
		if self.len == 0:
			raise ValueError ("La lista esta vacia")
		if posicion is None:
			posicion = self.len-1
		elif 0 > posicion > self.len+1:
			raise IndexError ("Ingreso una posicion fuera de la lista")
		self.len -= 1
		actual = self.prim
		if posicion == 0:
			self.prim = actual.prox
		for i in range (1,posicion):
			actual = actual.prox
		if posicion == self.len-1:
			actual.prox = None
		else: 
			actual.prox=actual.prox.prox
		return actual.dato
class _IteradorListaEnlazada:
	def __init__(self, posicion):
		self.actual = posicion
	def __next__(self):
		if self.actual is None:
			raise StopIteration()
		dato = self.actual.dato
		self.actual = self.actual.prox
		return dato
class Pila:
	"""docstring for Pila"""
	def __init__(self):
		"""Constructor for Pila"""
		self.elementos= []
	def esta_vacia(self):
		"""Devuelve un booleano segun la pila esta vacia o no."""
		return len(self.elementos)==0
	def apilar(self,dato):
		"""Agrega un dato a la pila."""
		self.elementos.append(dato)
	def desapilar(self):
		"""Elimina el ultimo elemento ingresado de la pila y lo devuelve."""
		if self.esta_vacia():
			raise ValueError ("La pila esta vacia")
		return self.elementos.pop()
	def tope(self):
		"""Devuelve el ultimo elemento ingresado en la lista.\n
		Error si esta vacia"""
		if self.esta_vacia():
			raise ValueError("La pila esta vacia")
		return self.elementos[-1]
	def invertir(self):
		"""Devuelve la misma pila con sus elementos invertidos."""
		cola_aux = Cola()
		while not self.esta_vacia():
			cola_aux.encolar(self.desapilar())
		while not cola_aux.esta_vacia():
			self.apilar(cola_aux.desencolar())
class Cola:
	"""docstring for Cola"""
	def __init__(self, arg):
		"""Constructor for Cola"""
		self.primero=None
		self.ultimo=None
	def esta_vacia(self):
		"""Devuelve un booleano segun la cola esta vacia o no."""
		return self.primero is None
	def encolar(self,dato):
		"""Agrega un dato a la cola."""
		nodo=_Nodo(dato)
		if self.ultimo is not None:
			self.ultimo.prox=nodo
		else:
			self.primero=nodo
		self.ultimo=nodo
	def desencolar(self):
		"""Elimina el primer elemento de la cola y lo devuelve."""
		if self.esta_vacia():
			raise ValueError ("La cola no tiene primero, esta vacia.")
		dato=self.primero.dato
		self.primero=self.primero.prox
		return dato
	def ver_primero(self):
		"""Devuelve el ultimo elemento ingresado en la lista.\n
		Error si esta vacia."""
		if self.esta_vacia():
			raise ValueError ("La cola no tiene primero, esta vacia.")
		return self.primero.dato