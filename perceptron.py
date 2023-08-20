from tkinter import font
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import os
from PIL import Image, ImageTk

class PerceptronApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Perceptrón - Montejo & Giraldo")

        self.x = None
        self.yd = None
        self.w = None                

        # Crear una fuente en negrita
        bold_font = font.Font(weight="bold")

        # Crear botones
        self.load_x_button = tk.Button(
            root, text="Cargar Entradas", command=self.load_x)
        self.load_x_button.pack(pady=10)

        self.load_yd_button = tk.Button(
            root, text="Cargar Salidas Deseadas", command=self.load_yd)
        self.load_yd_button.pack(pady=10)

        self.load_w_button = tk.Button(
            root, text="Cargar Pesos", command=self.load_w)
        self.load_w_button.pack(pady=10)

        # Agregar etiquetas y cuadros de texto
        self.error_label = tk.Label(root, text="Ingrese el valor del error:")
        self.error_label.pack(pady=5)

        self.error_entry = tk.Entry(root)
        self.error_entry.pack(pady=5)

        self.alfa_label = tk.Label(root, text="Ingrese el valor de alfa:")
        self.alfa_label.pack(pady=5)

        self.alfa_entry = tk.Entry(root)
        self.alfa_entry.pack(pady=5)

        # Agregar botones para cargar el error y el alfa manualmente
        self.load_error_button = tk.Button(
            root, text="Cargar Error", command=self.load_error)
        self.load_error_button.pack(pady=5)

        self.load_alfa_button = tk.Button(
            root, text="Cargar Alfa", command=self.load_alfa)
        self.load_alfa_button.pack(pady=5)

        # Crear botón de entrenar
        self.train_button = tk.Button(
            root, text="Entrenar", command=self.train, bg="green", fg="white")
        self.train_button.pack(pady=10)

        # Crear botón de reiniciar variables
        self.reset_button = tk.Button(
            root, text="Reiniciar", command=self.reset, bg="red", fg="white")
        self.reset_button.pack(pady=10)
        
        #Etiquetas para resultados del entrenamiento
        self.w_label = tk.Label(root, text="Pesos finales (w):")
        self.w_label.pack()

        self.epoca_label = tk.Label(root, text="Número de épocas:")
        self.epoca_label.pack()

        self.yd1_label = tk.Label(root, text="Salidas esperadas:")
        self.yd1_label.pack()

        self.yo_label = tk.Label(root, text="Salidas obtenidas:")
        self.yo_label.pack()


        self.possible_entries_label = tk.Label(root, text="APLICACIÓN", font=bold_font)
        self.possible_entries_label.pack()

        # Label para indicar las posibles entradas
        self.possible_entries_label = tk.Label(root, text="Posibles entradas: 100, 101, 110, 111")
        self.possible_entries_label.pack()

        # Caja de texto para ingresar las entradas
        self.input_entry = tk.Entry(root)
        self.input_entry.pack(pady=5)

        # Botón para calcular las salidas
        self.calculate_output_button = tk.Button(
            root, text="Calcular Salida", command=self.calculate_output, bg="lightblue", fg="black")
        self.calculate_output_button.pack(pady=5)

        # Label para las salidas obtenidas
        self.yo1_label = tk.Label(root, text="Salida obtenida:")
        self.yo1_label.pack()

    def calculate_output(self):
        if self.w is None:
            messagebox.showerror("Error", "Cargue los pesos antes de calcular.")
            return

        input_str = self.input_entry.get().strip()

        if input_str not in ["100", "101", "110", "111"]:
            messagebox.showerror("Error", "Ingrese una combinación válida (100, 101, 110 o 111).")
            return

        input_values = [int(val) for val in input_str]

        net = 0
        for i in range(3):
            net += self.w[0, i] * input_values[i]

        if net > 0:
            output = 1
        else:
            output = 0

        self.output_label.config(text=f"Salida obtendia: {output}")

    #Funcion para la aplicacion
    def calculate_output(self):
        if self.w is None:
            messagebox.showerror("Error", "Cargue los pesos antes de calcular.")
            return

        input_str = self.input_entry.get().strip()

        if input_str not in ["100", "101", "110", "111"]:
            messagebox.showerror("Error", "Ingrese una combinación válida (100, 101, 110 o 111).")
            return

        input_values = [int(val) for val in input_str]

        net = 0
        for i in range(3):
            net += self.w[0, i] * input_values[i]

        if net > 0:
            output = 1
        else:
            output = 0

        self.yo1_label.config(text=f"Salida obtenida: {output}")  # Actualiza 'yo_label' en lugar de 'output_label'
    
    def load_x(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    content = file.readlines()
                    rows = []
                    for line in content:
                        row = list(map(int, line.strip().split()))
                        rows.append(row)
                    self.x = np.array(rows)
                    messagebox.showinfo("Carga exitosa", "Matriz de entradas cargada exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar la matriz: {e}")


    def load_yd(self):
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                yd_vector = np.array([int(x) for x in content.split()])  # Lee los valores y los convierte en enteros
                self.yd = yd_vector.reshape(1, -1)  # Convertir a matriz de filas
                messagebox.showinfo("Carga exitosa", "Matriz de salidas deseadas cargada exitosamente.")


    def load_w(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos de texto", "*.txt")])
        if file_path:
            self.w = np.array(self.load_matrix(file_path))
            messagebox.showinfo(
                "Carga exitosa", "Matriz de pesos cargada exitosamente.")

    
    def load_error(self):
        error_str = self.error_entry.get()
        try:
            error = list(map(int, error_str.split()))
            self.error = np.array(error, dtype=int)  # Asegura que los valores sean enteros
            messagebox.showinfo("Carga exitosa", "Error cargado exitosamente.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores válidos para el error.")



    def load_alfa(self):
        alfa_str = self.alfa_entry.get()
        try:
            alfa = float(alfa_str)
            messagebox.showinfo("Carga exitosa", "Alfa cargado exitosamente.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un valor válido para alfa.")          

    def train(self):        
        
        alfa_str = self.alfa_entry.get()
        alfa = float(alfa_str)

        error_str = self.error_entry.get()
        error = np.array(list(map(float, error_str.split())))

        alfa1 = alfa
        x1 = np.array(self.x)
        errT = 0
        yo = np.array([0, 0, 0, 0])
        yd1 = self.yd
        w1 = self.w
        net = 0
        epoca = 0
        err = np.array(error)       

        try:
            errT_values = []  # Almacenar valores de errT en cada época

            while np.any(err != 0):
                errT = 0  # Reiniciar el error total en cada iteración
                for p in range(4):
                    net = 0  # Reiniciar la variable net en cada iteración
                    for i in range(3):
                        net += w1[0,i] * x1[i, p]
                    
                    if net > 0:
                        yo[p] = 1
                    else:
                        yo[p] = 0
                    
                    err[p] = yd1[0,p] - yo[p]
                    
                    for i in range(3):
                        w1[0,i] += alfa * err[p] * x1[i, p]
                    
                    errT += abs(err[p])  # Acumular el error absoluto                                

                    self.w_label.config(text=f"Pesos finales (w): {w1}")
                    self.epoca_label.config(text=f"Número de épocas: {epoca}")
                    self.yd1_label.config(text=f"Salidas esperadas: {yd1}")
                    self.yo_label.config(text=f"Salidas obtenidas: {yo}")  
                
                errT_values.append(errT)
                epoca += 1

                print("Epoca: ",epoca)
                print("Pesos Actuales:",w1)

            messagebox.showinfo("Entrenamiento", "Entrenamiento completado.")
            
            # Graficar errorT vs epocas
            plt.figure()
            plt.plot(range(1, epoca + 1), errT_values, marker='o')
            plt.xlabel("Épocas")
            plt.ylabel("Error Total (errT)")
            plt.title("Error Total vs Épocas")
            plt.grid(True)
            plt.show() 

            for i in np.arange(0, 1, 0.01):
                x2 = (-(w1[0, 1] / w1[0, 2]) * i) - (w1[0, 0] / w1[0, 2])
                plt.plot(i, x2, 'g.')
            
            # Agregar puntos (0,0), (0,1), (1,0) y (1,1)
            plt.plot([0, 0], [0, 0], 'ro')   # Punto (0,0)
            plt.plot([0, 0], [1, 1], 'ro')   # Punto (0,1)
            plt.plot([1, 1], [0, 0], 'ro')   # Punto (1,0)
            plt.plot([1, 1], [1, 1], 'ro')   # Punto (1,1)

            plt.xlim(0, 1.5)  # Ajustar los límites del eje x
            plt.ylim(0, 1.5)  # Ajustar los límites del eje y
            plt.xlabel("x1")
            plt.ylabel("x2")
            plt.title("Recta Resultante del Perceptrón")
            plt.grid(True)
            plt.show()

            
        except ValueError as e:
            messagebox.showerror("Error", str(e))                

    def load_matrix(self, file_path):
        with open(file_path) as file:
            lines = file.readlines()
        matrix = [list(map(float, line.strip().split())) for line in lines]
        return matrix
    
    def reset(self):
        self.x = None
        self.yd = None
        self.w = np.random.rand(1, 3)
        self.error_entry.delete(0, tk.END)
        self.alfa_entry.delete(0, tk.END)
        self.w_label.config(text="Pesos finales (w):")
        self.epoca_label.config(text="Número de épocas:")
        self.yd1_label.config(text="Salidas esperadas:")
        self.yo_label.config(text="Salidas obtenidas:")
        self.input_entry.delete(0, tk.END)  # Limpiar la caja de texto de entradas
        self.yo1_label.config(text="Salida obtenida:")

        # Actualizar el archivo 'w.txt' con los nuevos pesos aleatorios
        w_file_path = os.path.join(current_directory, 'w.txt')
        with open(w_file_path, 'w') as file:
            np.savetxt(file, self.w, fmt='%f')

if __name__ == "__main__":
    # Obtener la ruta absoluta del directorio actual
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Actualizar w
    w_file_path = os.path.join(current_directory, 'w.txt')
    with open(w_file_path, 'w') as file:
        w_initial = np.random.rand(1, 3)  # Generar un vector aleatorio de 3 posiciones
        np.savetxt(file, w_initial, fmt='%f')
    
    root = tk.Tk()
    app = PerceptronApp(root)

    root.iconbitmap("icon.ico") #Cambiar icono

    # Ajustar ventana
    window_width = 500  
    window_height = 650  

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = (screen_width - window_width) // 2
    y_position = 0

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    root.mainloop()