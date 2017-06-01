import cmd
import soundPlayer
import tda
import csv
from os.path import isfile


def validar_entero(n):
    """Recibe n devolviendolo como int. Si no puede convertir levanta\n
    excepcion.\n
        ->n(int ó str): es el valor a devolverse como entero"""

    if type(n) == int:
        return n
    if n.isdigit():
        return int(n)
    raise TypeError ("Lo recibido no es un entero")


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
        actual = self.cursor  # a partir de donde estamos
        while cont < N and actual is not None:
            actual = actual.prox
            self.pila.apilar(actual)
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

    def __init__(self):
        """Constructor"""
        return

    def play(self,n):
        if editor.timeline.len == 0:
            print("No hay marcas para reproducir")
        reproductor = soundPlayer.SoundPlay(len(editor.tracks))
        actual = editor.cursor
        cont = 0
        while actual is not None and cont < n:
            lista_aux = []
            lista_tracks = []
            mark = actual.dato
            duracion = mark.dato["duracion"]
            for i in range(len(editor.tracks)):
                (funcion, frecuencia, volumen) = editor.tracks[i]
                if mark[i]=="#":
                    lista_aux.append(editor.sound.get(funcion)(frecuencia, volumen))
            reproductor.play_sounds(lista_aux, duracion)
            mark["duracion"]=duracion
            actual = actual.prox
            cont += 1


class Almacenamiento:
    """Clase encargada de guardar y cargar el archivo .plp"""
    def __init__(self):
        """Constructor"""
        return

    def guardar(self,file):
        """Guarda el archivo con el nombre ingresado.\n
            ->file(str): nombre del archivo"""

        with open(file,"w") as f:
            f.write("FIELD,DATA\n")							#cabecera
            f.write("C,{}\n".format(len(editor.tracks)))	#Escribimos la cantidad de canales
            for i in range(len(editor.tracks)):				#Escribimos la info de los canales
                (funcion, frecuencia, volumen) = editor.tracks[i]
                f.write("C,{}|{}|{}\n".format(funcion, frecuencia, volumen))
            duracion_anterior = 0
            for mark in editor.timeline:
                if mark.get("duracion") != duracion_anterior:
                    duracion_anterior = mark.get("duracion")
                    f.write("T,{}\n".format(mark.get("duracion")))
                cadena_mark = ""
                for i in range(len(editor.tracks)):
                    cadena_mark += mark.get(i,".")
                f.write("N,"+cadena_mark+"\n")
    def cargar(self, file):
        """Carga el archivo con el nombre ingresado.Si no existe ninguno\n
        archivo con ese nombre carga una cancion vacia
            ->file(str): nombre del archivo"""
        if not isfile(file):
            print("El archivo no existe")
        else:
            with open(file,"r") as f:
                datos_csv = csv.reader(f)
                encabezado = next(datos_csv)
                #if encabezado != ["FIELD","DATA"]: No es necesario, el archivo que nos mandaron no tiene esto
                #    raise ValueError ("se ingreso otro tipo de archivo")
                cantidad_canales = int(next(datos_csv)[1])
                for i in range(cantidad_canales):
                    track = next(datos_csv)[1].split("|")
                    funcion = track[0]
                    frecuencia = float(track[1])
                    volumen = float(track[2])
                    editor.tracks.append((funcion, frecuencia, volumen))
                for mark in datos_csv:
                    if mark[0] == "T":
                        duracion = float(mark[1])
                        continue
                    diccionario = {"duracion":duracion}
                    for i in range(len(mark[1])):
                        if mark[1][i] == "#":
                            diccionario[i] = mark[1][i]
                    editor.timeline.append(diccionario)

class Shell(cmd.Cmd):
    intro = " Bienvenido a mi FIUBA Music Editor.\n Ingrese help o ? para listar los comandos.\n"
    prompt = "*>>"
    def do_cargar(self,file):
        """Carga la cancion desde el archivo.\n
        Reemplaza la cancion en edicion actual si es que la hay.\n
            -> file (str)"""
        almacenamiento.cargar(file)

    def do_guardar(self,file):
        """Guarda la cancion.\n
            -> file (str)"""
        almacenamiento.guardar(file)

    def do_avanzar(self,x=None):
        """Avanza a la siguiente marca de tiempo.Si no hay mas marcas \n
        hacia adelante, no hace nada."""
        editor.avanzar(1)

    def do_retroceder(self,x = None):
        """Retrocede a la anterior marca de tiempo.Si no hay mas marcas\n
        hacia atras, no hace nada."""
        editor.retroceder(1)

    def do_avanzarm (self, n):
        """Avanza N marcas de tiempo hacia adelante. Si no hay mas mar\n
        cas hacia adelante, no hace nada."""
        editor.avanzar(validar_entero(n))

    def do_retrocederm (self, n):
        """Retrocede N marcas de tiempo hacia atras. Si no hay mas mar\n
        cas hacia atras, no hace nada."""
        editor.retroceder(validar_entero(n))

    def do_trackadd (self, parametros):
        """Agrega un track con el sonido indicado.\n
            -> funcion (str): tipo de sonido\n
            -> frecuencia(int)\n
            -> volumen(int)\n"""

        lista_p = parametros.split(" ")
        if len(lista_p)== 3:
            funcion, frecuencia, volumen = lista_p[0], lista_p[1], lista_p[2]
        else:
            funcion, frecuencia = lista_p[0], lista_p[1]
            volumen = 100
        frecuencia = validar_entero(frecuencia)
        if not funcion in editor.sound:
            print("La funcion ingresada no esta definida")
        editor.tracks.append((funcion, frecuencia, volumen))

    def do_trackdel(self, posicion=None):
        """Elimina un track por numero.Si no se especifica uno elimina\n
        el ultimo tarck.\n
            -> posicion(str)"""
        if posicion is None:
            posicion = len(editor.tracks - 1)
        else:
            posicion = validar_entero(posicion)
        if posicion<0 or posicion>len(editor.tracks):
            print("La posicion ingresada no corresponde a un track ingresado")
        editor.tracks.pop(int(posicion))

    def do_markadd(self, duration):
        """Agrega una marca de tiempo de la duracion establecida.\n
        Originalmente todos los tracks arrancan como deshabilitados."""
        duration = validar_entero(duration)
        editor.timeline.append({"duracion":duration/100})
        editor.avanzar(1)
        print(editor.timeline)

    def do_markaddnext(self, duration):
        """Igual que MARKADD pero la inserta luego de la marca en la \n
        cual esta actualmente el cursor."""
        duration = validar_entero(duration)
        editor.timeline.insert(editor.index+1,{"duracion":duration/100})

    def do_markaddprev(self,duration):
        """Igual que MARKADD pero la inserta antes de la marca en la \n
        cual esta actualmente el cursor."""
        duration = validar_entero(duration)
        print(editor.timeline.len)
        print(editor.index)
        editor.timeline.insert(editor.index-1,{"duracion":duration/100})


    def do_trackon(self, track):
        """Habilita al track durante la marca de tiempo en la cual \n
        esta parada el cursor."""
        track = validar_entero(track)

        editor.cursor.dato[track]="#"

    def do_trackoff(self, track):
        """Operacion inversa del TRACKON."""
        track = validar_entero(track)
        editor.cursor.dato.pop(track)

    def do_play(self, x = None):
        """Reproduce la marca en la que se encuentra el cursor actual\n
        mente."""
        do_playmarks(editor.timeline.len-editor.index)

    def do_playall(self, x = None):
        """Reproduce la cancion completa desde el inicio."""
        cursor_aux = editor.cursor
        editor.cursor = editor.timeline.prim
        do_play()
        editor.cursor = cursor_aux

    def do_playmarks (self, n):
        """Reproduce las proximas N marcas desde la posicion actual del\n
         cursor."""
        n = validar_entero(n)
        reproductor.play(n)

    def do_playsecond(self, n):
        """Reproduce los proximos N segundos desde la posicion actual \n
        del cursor. Si alguna marca dura mas del tiempo restante, la \n
        reproduccion se corta antes."""
        n = validar_entero(n)
        # Ejemplo :
        # 	PLAYSECONDS 5

    def do_imprimir(self, x = None):
        """Imprime la timeline que se tiene hasta el momento"""
        for mark in editor.timeline:
            print(mark)


    def do_salir(self, x = None):
        """Sale del programa"""
        print("Hasta luego")
        exit()

editor = Editor()
almacenamiento = Almacenamiento()
reproductor = Reproductor()
Shell().cmdloop()