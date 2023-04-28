import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import math
import numpy as np
def flood_fill_puntos(canvas, x, y, color_reemplazo):
    color_borde = "Ghostwhite"
    color_inicial = canvas.obtener_color_pixel(x, y)

    pila = [(x, y)]
    visitados = set()
    en_pila = set([(x, y)])

    while pila:
        x, y = pila.pop()
        en_pila.remove((x, y))

        if (x, y) in visitados:
            continue

        canvas.create_rectangle(x-5, y-5, x + 5, y+5, outline=color_reemplazo, fill=color_reemplazo)
        
        visitados.add((x, y))

        for dx, dy in [(-5, 0), (5, 0), (0, -5), (0, 5)]:
            nx, ny = x + dx, y + dy
            if canvas.obtener_color_pixel(nx, ny) != color_borde:
                if (nx, ny) not in visitados and (nx, ny) not in en_pila:
                    pila.append((nx, ny))
                    en_pila.add((nx, ny))

def bresenham(x1, y1, x2, y2):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 10 if x1 < x2 else -10
    sy = 10 if y1 < y2 else -10
    err = dx - dy
    x, y = x1, y1
    puntos = []
    while True:
        puntos.append((x, y))
        
        if x == x2 and y == y2:
            break 
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy      
    return puntos

def dda(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    
    # Calcula la distancia total a través de la fórmula de la distancia Euclidiana
    distancia = math.sqrt(dx**2 + dy**2)
    
    # Calcula el incremento en x y y
    if distancia != 0:
        inc_x = dx / distancia
        inc_y = dy / distancia
    
        # Dibuja el primer punto
        x, y = x1, y1
        puntos = [(x, y)]
    
        # Dibuja los puntos intermedios
        while abs(x - x2) > 0.1 or abs(y - y2) > 0.1:
            x += inc_x
            y += inc_y
            puntos.append((round(x), round(y)))
    
        # Dibuja el último punto
        puntos.append((x2, y2))
    else:
        puntos = [(x1, y1)]
    
    return puntos

def punto_medio(x0, y0, radio):
    radio_en_pixeles = math.ceil(radio / 10)
    x = 0
    y = radio_en_pixeles
    d = 1 - radio_en_pixeles
    puntos = []
    while x <= y:
        puntos.append((x0 + x * 10, y0 + y * 10))
        puntos.append((x0 + y * 10, y0 + x * 10))
        puntos.append((x0 - y * 10, y0 + x * 10))
        puntos.append((x0 - x * 10, y0 + y * 10))
        puntos.append((x0 - x * 10, y0 - y * 10))
        puntos.append((x0 - y * 10, y0 - x * 10))
        puntos.append((x0 + y * 10, y0 - x * 10))
        puntos.append((x0 + x * 10, y0 - y * 10))
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
    return puntos

class Figura:
    def __init__(self, x, y, color='White', grosor=10, tipo_linea='solid'):
        self.x = x
        self.y = y
        self.color = color
        self.grosor = grosor
        self.tipo_linea = tipo_linea
        self.escala = 1  # Agregue la propiedad escala aquí
        self.borde_seleccionado = False
    def escalar(self, factor):
        # Redondea el factor de escala al múltiplo de 5 más cercano
        self.escala = factor
    def get_escala(self):
        return self.escala
    def rotar(self, angulo):
        # Implementación de la función de rotación
        pass  # Reemplazar con la implementación real
    def cambiar_color(self, color):
        self.color = color
    def trasladar(self, dx, dy):
        self.x += dx
        self.y += dy
    def imprimir_atributos(self):
        print(f"Tipo: {type(self).__name__}, X: {self.x}, Y: {self.y}, Color: {self.color}, Grosor: {self.grosor}, Tipo de línea: {self.tipo_linea}, Escala: {self.escala}")
    def colorear(self, canvas):
        pass
      
class Cuadrado(Figura):
    def __init__(self, x, y, lado, color='black', grosor=1, tipo_linea='solid'):
        # Redondea las coordenadas x e y al múltiplo de 10 más cercano
        x = round(x / 5) * 5
        y = round(y / 5) * 5
        super().__init__(x, y, color, grosor, tipo_linea)
        self.lado = round(lado / 5) * 5
    def colisiona_con_punto(self, x, y):
        return self.x <= x <= self.x + self.lado * self.escala and self.y <= y <= self.y + self.lado * self.escala

    def imprimir_atributos(self):
        super().imprimir_atributos()
        print(f"Lado: {self.lado}")    
    def colorear(self, canvas):
        semilla_x = round((self.x + int(self.lado * self.escala / 2)) / 5) * 5
        semilla_y = round((self.y + int(self.lado * self.escala / 2)) / 5) * 5
        flood_fill_puntos(canvas, semilla_x, semilla_y, self.color)
def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

class Triangulo(Figura):
    def __init__(self, x1, y1, x2, y2, x3, y3, color='black', grosor=1, tipo_linea='solid'):
        super().__init__(x1, y1, color, grosor, tipo_linea)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.escala = 1
    def coordenadas_escaladas(self):
        # Identifica el punto superior (el que tiene la coordenada y más pequeña)
        puntos = np.array([[self.x1, self.y1], [self.x2, self.y2], [self.x3, self.y3]])
        punto_superior = np.argmin(puntos, axis=0)[1]
        
        # Calcula la matriz de escalado
        escala_matriz = np.array([[self.escala, 0], [0, self.escala]])
        
        # Escala las coordenadas
        puntos_escalados = puntos - puntos[punto_superior]
        puntos_escalados = np.dot(puntos_escalados, escala_matriz)
        puntos_escalados = puntos_escalados + puntos[punto_superior]
        
        # Redondea las coordenadas escaladas
        puntos_escalados = np.round(puntos_escalados / 10) * 10
        
        # Devuelve los valores de las coordenadas escaladas
        x1_escalado, y1_escalado = puntos_escalados[0]
        x2_escalado, y2_escalado = puntos_escalados[1]
        x3_escalado, y3_escalado = puntos_escalados[2]
        return x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado
    def punto_medio_triangulo(x1, y1, x2, y2, x3, y3):
        x_medio = (x1 + x2 + x3) / 3
        y_medio = (y1 + y2 + y3) / 3
        return x_medio, y_medio   
    def colisiona_con_punto(self, x, y):
        x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado = self.coordenadas_escaladas()
        area_total = area(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado)
        area1 = area(x, y, x2_escalado, y2_escalado, x3_escalado, y3_escalado)
        area2 = area(x1_escalado, y1_escalado, x, y, x3_escalado, y3_escalado)
        area3 = area(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x, y)
        return abs(area_total - (area1 + area2 + area3)) < 0.1
    def trasladar(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        self.x3 += dx
        self.y3 += dy
    def imprimir_atributos(self):
        super().imprimir_atributos()
    def colorear(self, canvas):
        x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado = self.coordenadas_escaladas()
        semilla_x, semilla_y = Triangulo.punto_medio_triangulo(x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado)
        flood_fill_puntos(canvas, round(semilla_x/5)*5, round(semilla_y/5)*5, self.color)
class Circunferencia(Figura):
    def __init__(self, x, y, radio, color='yellow', grosor=1, tipo_linea='solid'):
        super().__init__(x, y, color, grosor, tipo_linea)
        self.radio = radio
    def colisiona_con_punto(self, x, y):
        distancia_centro = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
        return distancia_centro <= self.radio * self.escala
    def imprimir_atributos(self):
        super().imprimir_atributos()
        print(f"Radio: {self.radio}")
    def colorear(self, canvas):
        flood_fill_puntos(canvas, self.x, self.y, self.color)
class FigurasCanvas(tk.Canvas):
    # def borrar_figura(self, figura):
    #     if figura is not None:
    #         items = self.find_all()
    #         for item in items:
    #             if self.gettags(item) == (str(id(figura)),):
    #                 self.delete(item)
    def borrar_figura(self, figura):
        if figura is not None:
            self.delete(figura.id)
    def obtener_color_pixel(self, x, y):
    # Encuentra los elementos en la coordenada (x, y)
        elementos = self.find_overlapping(x, y, x+1, y+1)

        # Si hay elementos en la coordenada
        if elementos:
            # Obtén el color del fondo del Canvas
            color_fondo = self["bg"]
            
            # Itera sobre los elementos superpuestos
            for elemento in elementos:
                color = self.itemcget(elemento, "fill")
                
                # Si el color del elemento es diferente al fondo, devuélvelo
                if color != color_fondo:
                    return color

        # Si no se encontró un elemento con color diferente al fondo, devuelve None
        return None
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.figuras = []
        self.figura_seleccionada = None
        self.bind("<Button-1>", self.on_click_izquierdo)
        self.bind("<B1-Motion>", self.on_arrastre_izquierdo)
        self.bind("<ButtonRelease-1>", self.on_suelta_izquierdo)
        self.estado = "dibujar"
        self.figura_actual = "cuadrado"
          
    def dibujar_figura(self, figura):
        escala = figura.escala
        if isinstance(figura, Cuadrado):
            lado = (round(figura.lado * escala/10)*10)
            puntos_linea1 = bresenham(figura.x, figura.y, figura.x + lado, figura.y)
            puntos_linea2 = bresenham(figura.x, figura.y, figura.x, figura.y + lado)
            puntos_linea3 = bresenham(figura.x + lado, figura.y, figura.x + lado, figura.y + lado)
            puntos_linea4 = bresenham(figura.x, figura.y + lado, figura.x + lado, figura.y + lado)
            for punto in puntos_linea1 + puntos_linea2 + puntos_linea3 + puntos_linea4:
                x, y = punto
                # outline=color_reemplazo
                # self.create_rectangle(x, y, x+10, y+10, width=1, fill="GhostWhite")
                self.create_rectangle(x, y, x+10, y+10, width=1,outline="Black", fill="Ghostwhite")
            figura.colorear(self)
            
        elif isinstance(figura, Circunferencia):
            radio  = (round(figura.radio * escala/10)*10)
            puntos_circunferencia = punto_medio(figura.x, figura.y, radio)
            for punto in puntos_circunferencia:
                x, y = punto
                self.create_rectangle(x, y, x+10, y+10, width=1,outline="Black",fill="Ghostwhite")
            figura.colorear(self)
        elif isinstance(figura, Triangulo):
            x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado = figura.coordenadas_escaladas()
            
            puntos_linea1 = bresenham(x1_escalado, y1_escalado, x2_escalado, y2_escalado)
            puntos_linea2 = bresenham(x2_escalado, y2_escalado, x3_escalado, y3_escalado)
            puntos_linea3 = bresenham(x3_escalado, y3_escalado, x1_escalado, y1_escalado)
            for punto in puntos_linea1 + puntos_linea2 + puntos_linea3:
                x, y = punto
                self.create_rectangle(x, y, x+10, y+10, width=1, outline="Black", fill="Ghostwhite")
            figura.colorear(self)
        self.dibujar_segundo_borde(figura, "Black", 0)

    
    def dibujar_segundo_borde(self, figura, color, grosor):
        escala = figura.escala

        if isinstance(figura, Cuadrado):
            lado = (round(figura.lado * escala/10)*10)
            puntos_linea1 = bresenham(figura.x, figura.y, figura.x + lado, figura.y)
            puntos_linea2 = bresenham(figura.x, figura.y, figura.x, figura.y + lado)
            puntos_linea3 = bresenham(figura.x + lado, figura.y, figura.x + lado, figura.y + lado)
            puntos_linea4 = bresenham(figura.x, figura.y + lado, figura.x + lado, figura.y + lado)
            for punto in puntos_linea1 + puntos_linea2 + puntos_linea3 + puntos_linea4:
                x, y = punto
                self.create_rectangle(x, y, x+10, y+10, width=grosor, outline=color, fill=color)
            
        elif isinstance(figura, Circunferencia):
            radio  = (round(figura.radio * escala/10)*10)
            puntos_circunferencia = punto_medio(figura.x, figura.y, radio)
            for punto in puntos_circunferencia:
                x, y = punto
                self.create_rectangle(x, y, x+10, y+10, width=grosor, outline=color, fill=color)
            
        elif isinstance(figura, Triangulo):
            x1_escalado, y1_escalado, x2_escalado, y2_escalado, x3_escalado, y3_escalado = figura.coordenadas_escaladas()
            
            puntos_linea1 = bresenham(x1_escalado, y1_escalado, x2_escalado, y2_escalado)
            puntos_linea2 = bresenham(x2_escalado, y2_escalado, x3_escalado, y3_escalado)
            puntos_linea3 = bresenham(x3_escalado, y3_escalado, x1_escalado, y1_escalado)
            for punto in puntos_linea1 + puntos_linea2 + puntos_linea3:
                x, y = punto
                self.create_rectangle(x, y, x+10, y+10, width=grosor, outline=color, fill=color)
    def get_pixel_color(self, x, y):
        items = self.find_overlapping(x, y, x, y)
        if items:
            return self.itemcget(items[0], "fill")
        else:
            return None

    def set_pixel_color(self, x, y, color):
        self.itemconfig(self.find_closest(x, y), fill=color)

    def in_bounds(self, x, y):
        return 0 <= x < self.winfo_width() and 0 <= y < self.winfo_height()
    
    # Las funciones agregar_cuadrado, agregar_circulo y agregar_triangulo deben estar al mismo nivel que dibujar_figura, no dentro de la función __init__
    def agregar_cuadrado(self, x, y):
        figura = Cuadrado(x, y, 90, "Blue", 2, "solid")
        self.figuras.append(figura)
        self.dibujar_figura(figura)
        
    def agregar_circulo(self, x, y):
        figura = Circunferencia(x, y, 45, "Yellow", 2, "solid")
        self.figuras.append(figura)
        self.dibujar_figura(figura)

    def agregar_triangulo(self, x, y):
        figura = Triangulo(x - 50, y + 80, x, y-10, x + 50, y + 80, "Green", 2, "solid")
        self.figuras.append(figura)
        self.dibujar_figura(figura)
        
    def on_click_izquierdo(self, event):
        x, y = (round(event.x/10)*10), (round(event.y/10)*10)
        # x, y = event.x, event.y
         
        
        if self.estado == "dibujar":
            if self.figura_actual == "cuadrado":
                self.agregar_cuadrado(x, y)
            elif self.figura_actual == "circulo":
                self.agregar_circulo(x, y)
            elif self.figura_actual == "triangulo":
                self.agregar_triangulo(x, y)
        elif self.estado == "mover":
            self.seleccionar_figura(x, y)
        print("Color del píxel en ({}, {}): {}".format(x, y, self.obtener_color_pixel(x, y)))
        # print("Color del píxel en ({}, {}): {}".format(x, y, self.get_pixel_color(self, x, y)))
        

    def on_arrastre_izquierdo(self, event):
        if self.estado == "mover" and self.figura_seleccionada is not None:
            if not hasattr(self, 'prev_x'):
                self.prev_x = event.x
                self.prev_y = event.y
            # dx = event.x - self.prev_x
            # dy = event.y - self.prev_y
            dx = round((event.x - self.prev_x) / 10) * 10
            dy = round((event.y - self.prev_y) / 10) * 10   
            self.prev_x = event.x
            self.prev_y = event.y
            if isinstance(self.figura_seleccionada, Triangulo):
                self.figura_seleccionada.x1 += dx
                self.figura_seleccionada.y1 += dy
                self.figura_seleccionada.x2 += dx
                self.figura_seleccionada.y2 += dy
                self.figura_seleccionada.x3 += dx
                self.figura_seleccionada.y3 += dy
            else:
                self.figura_seleccionada.trasladar(dx, dy)
            # self.borrar_figura(self.figura_seleccionada)
            # self.dibujar_figura(self.figura_seleccionada)
            
            self.delete("all")
            for figura in self.figuras:
                self.dibujar_figura(figura)
    def on_suelta_izquierdo(self, event):
        if hasattr(self, 'prev_x'):
            del self.prev_x
            del self.prev_y
    
    def seleccionar_figura(self, x, y):
        self.figura_seleccionada = None
        for figura in self.figuras:
            if figura.colisiona_con_punto(x, y):
                figura.borde_seleccionado = not figura.borde_seleccionado
                self.figura_seleccionada = figura
                break
    def borrar_figura_seleccionada(self):
        if self.figura_seleccionada is not None:
            self.figuras.remove(self.figura_seleccionada)
            self.figura_seleccionada = None
            self.delete("all")
            for figura in self.figuras:
                self.dibujar_figura(figura)
    def cambiar_color_figura_seleccionada(self, event):
        if self.canvas.figura_seleccionada is not None:
            color_seleccionado = self.color_var.get()
            colores = {'Negro': 'black', 'Rojo': 'red', 'Verde': 'green', 'Azul': 'blue', 'Amarillo': 'yellow', 'Naranja': 'orange', 'Morado': 'purple'}
            self.canvas.figura_seleccionada.cambiar_color(colores[color_seleccionado])
            self.canvas.delete("all")
            for figura in self.canvas.figuras:
                self.canvas.dibujar_figura(figura)
                
    def cambiar_color_seleccionado(self, color):
        if self.figura_seleccionada is not None:
            # Cambie el atributo color de la figura seleccionada
            self.figura_seleccionada.cambiar_color(color)
            self.figura_seleccionada.imprimir_atributos()
            # self.borrar_figura(self.figura_seleccionada)
            # self.dibujar_figura(self.figura_seleccionada)
            
            self.delete("all")
            for figura in self.figuras:
                self.dibujar_figura(figura)
    def mover_figura(self, dx, dy):
        figura = self.figura_seleccionada
        if isinstance(figura, Triangulo):
            figura.x1 += dx
            figura.y1 += dy
            figura.x2 += dx
            figura.y2 += dy
            figura.x3 += dx
            figura.y3 += dy
        else:
            figura.trasladar(dx, dy)

        self.delete("all")
        for fig in self.figuras:
            self.dibujar_figura(fig) 
    def escalar_figura(self, factor):
        if self.figura_seleccionada is not None:
            self.figura_seleccionada.escalar(factor)
            self.delete("all")
            for figura in self.figuras:
                self.dibujar_figura(figura)   
              
                       
class Aplicacion(tk.Tk):
    def __init__(self):
        bg1 = "#67747f"
        col2 = "#e9eeee"
        # d9dee2
        super().__init__()
        self.title("Dibujo de figuras geométricas")
        self.configure(bg="#d9dee2")
        self.canvas = FigurasCanvas(self, width=800, height=600)
        self.canvas.configure(bg="#d9dee2", highlightthickness=0)
        self.canvas.pack()

        self.frame_controles = tk.Frame(self)
        self.frame_controles.pack(side=tk.TOP, padx=5, pady=5)
        self.frame_controles.configure(bg=bg1)
        
        self.frame_figura = tk.Frame(self.frame_controles)
        self.frame_figura.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame_figura.configure(bg=bg1)

        self.figura_var = tk.StringVar()
        self.seleccion_figura = ttk.Combobox(self.frame_figura, textvariable=self.figura_var, state='readonly')
        self.seleccion_figura['values'] = ('Cuadrado', 'Círculo', 'Triángulo')
        self.seleccion_figura.current(0)
        self.seleccion_figura.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="W")
        self.seleccion_figura.bind("<<ComboboxSelected>>", self.actualizar_figura_actual)

        
        self.boton_dibujar = tk.Button(self.frame_figura, text="Dibujar", command=self.dibujar, width=6)
        self.boton_dibujar.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.boton_dibujar.configure(bg=col2)
        
        self.boton_mover = tk.Button(self.frame_figura, text="Seleccionar", command=self.mover, width=10)
        self.boton_mover.grid(row=2, column=1, padx=5, pady=5, sticky="W")
        self.boton_mover.configure(bg=col2)
        
        self.frame_color = tk.Frame(self.frame_controles)
        self.frame_color.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame_color.configure(bg=bg1)

        self.label_color = tk.Label(self.frame_color, text="Color de Figura", font=("Arial", 10, "bold"), bg="#EFEFEF", fg=col2)
        self.label_color.grid(row=2, column=0, sticky="W", padx=5, pady=7)
        self.label_color.configure(bg=bg1)
        
        self.color_var = tk.StringVar()
        self.seleccion_color = ttk.Combobox(self.frame_color, textvariable=self.color_var, state='readonly', width=14)
        self.seleccion_color['values'] = ('Black', 'Red', 'Green', 'Blue', 'Yellow', 'Orange')
        self.seleccion_color.current(0)
        self.seleccion_color.grid(row=1, column=0, sticky="W", padx=5, pady=0)
        self.seleccion_color.bind("<<ComboboxSelected>>", self.cambiar_color_figura_seleccionada)
        #_______________________
        #_______________________
        
        
        
        self.frame_escala = tk.Frame(self.frame_controles)
        self.frame_escala.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame_escala.configure(bg=bg1)
        
        self.label_escala = tk.Label(self.frame_escala, text="Tamaño", font=("Arial", 10, "bold"), bg="#EFEFEF", fg= col2 )
        self.label_escala.grid(row=2, column=0, columnspan=2, pady=(0, 10))
        self.label_escala.configure(bg=bg1)
        
        self.boton_aumentar = tk.Button(self.frame_escala, text="+", command=self.aumentar_escala, width=4, height=1)
        self.boton_aumentar.grid(row=1, column=1, padx=0, pady=2)
        self.boton_aumentar.configure(bg=col2)
        
        self.boton_disminuir = tk.Button(self.frame_escala, text="-", command=self.disminuir_escala, width=4, height=1)
        self.boton_disminuir.grid(row=1, column=0, padx=0, pady=0)
        self.boton_disminuir.configure(bg=col2)

        self.frame_movimiento = tk.Frame(self.frame_controles)
        self.frame_movimiento.pack(side=tk.LEFT, padx=5, pady=5)
        self.frame_movimiento.configure(bg=bg1)
        
        self.boton_arriba = tk.Button(self.frame_movimiento, text="↑", command=self.mover_arriba, width=4, height=1)
        self.boton_arriba.grid(row=0, column=1)
        self.boton_arriba.configure(bg=col2)
        self.boton_abajo = tk.Button(self.frame_movimiento, text="↓", command=self.mover_abajo, width=4, height=1)
        self.boton_abajo.grid(row=1, column=1)
        self.boton_abajo.configure(bg=col2)
        
        self.boton_izquierda = tk.Button(self.frame_movimiento, text="←", command=self.mover_izquierda, width=4, height=1)
        self.boton_izquierda.grid(row=1, column=0)
        self.boton_izquierda.configure(bg=col2)
        self.boton_derecha = tk.Button(self.frame_movimiento, text="→", command=self.mover_derecha, width=4, height=1)
        self.boton_derecha.grid(row=1, column=2)
        self.boton_derecha.configure(bg=col2)
        
        self.boton_borrar = tk.Button(self.frame_controles, text="Borrar", command=self.borrar, width=6, height=2)
        self.boton_borrar.pack(side=tk.LEFT, padx=5)
        self.boton_borrar.configure(bg=col2)
        
        #########
        

        
        
                                
             
    def dibujar(self):
        self.canvas.estado = "dibujar"
        self.actualizar_botones()
        
    def aumentar_escala(self):
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            self.canvas.escalar_figura(fig.get_escala()+0.4)

    def disminuir_escala(self):
        fig = self.canvas.figura_seleccionada
        if fig is not None:
            self.canvas.escalar_figura(fig.get_escala()-0.4)
                
            
    def escalar(self):
        if self.canvas.figura_seleccionada is not None:
            try:
                factor = float(self.escala_var.get())
                self.canvas.figura_seleccionada.escalar(factor)
                self.canvas.delete("all")
                for figura in self.canvas.figuras:
                    self.canvas.dibujar_figura(figura)
            except ValueError:
                messagebox.showerror("Error", "Ingrese un valor numérico válido.")
    def mover_arriba(self):
        if self.canvas.figura_seleccionada is not None:
            self.canvas.mover_figura(0, -80)

    def mover_abajo(self):
        if self.canvas.figura_seleccionada is not None:
            self.canvas.mover_figura(0, 80)

    def mover_izquierda(self):
        if self.canvas.figura_seleccionada is not None:
            self.canvas.mover_figura(-80, 0)

    def mover_derecha(self):
        if self.canvas.figura_seleccionada is not None:
            self.canvas.mover_figura(80, 0)

    
    def mover(self):
        self.canvas.estado = "mover"
        self.actualizar_botones()
    def actualizar_botones(self):
        if self.canvas.estado == "dibujar":
            self.boton_dibujar.config(bg="#c2c7cd", relief=tk.SUNKEN)  # Botón presionado
            self.boton_mover.config(bg="#e9eeee", relief=tk.RAISED)  # Botón no presionado
        elif self.canvas.estado == "mover":
            self.boton_dibujar.config(bg="#e9eeee", relief=tk.RAISED)  # Botón no presionado
            self.boton_mover.config(bg="#c2c7cd", relief=tk.SUNKEN)  # Botón presionado
    def borrar(self):
        self.canvas.borrar_figura_seleccionada()
    
    # Agregar la función actualizar_figura_actual para manejar la selección de figura
    def actualizar_figura_actual(self, event):
        figura_seleccionada = self.figura_var.get()
        if figura_seleccionada == "Cuadrado":
            self.canvas.figura_actual = "cuadrado"
        elif figura_seleccionada == "Círculo":
            self.canvas.figura_actual = "circulo"
        elif figura_seleccionada == "Triángulo":
            self.canvas.figura_actual = "triangulo"
    def cambiar_color_figura_seleccionada(self, event):
        color_seleccionado = self.color_var.get()#.lower()
        print(color_seleccionado)
        self.canvas.cambiar_color_seleccionado(color_seleccionado)
                       
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
    
    
















