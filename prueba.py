import tkinter as tk
from tkinter import messagebox

class MaquinaDeTuring:
    def __init__(self, cinta):
        self.cinta = list(cinta)
        self.cabeza = 0
        self.estado = 'inicio'

    def paso(self):
        if self.estado == 'inicio':
            # Mover hacia la derecha hasta encontrar el delimitador '+'
            if self.cinta[self.cabeza] == '+':
                self.estado = 'sumar'
            else:
                self.cabeza += 1
        elif self.estado == 'sumar':
            # Realizar la suma bit a bit con acarreo
            acarreo = 0
            i = self.cabeza - 1
            j = len(self.cinta) - 1
            resultado = []
            while i >= 0 and self.cinta[i] != '+':
                bit1 = int(self.cinta[i])
                bit2 = int(self.cinta[j]) if j > self.cabeza else 0
                suma_bits = bit1 + bit2 + acarreo
                resultado.append(str(suma_bits % 2))
                acarreo = suma_bits // 2
                i -= 1
                j -= 1
            if acarreo:
                resultado.append('1')
            self.cinta += [' '] + list(reversed(resultado))  # Agregar espacio antes del resultado para mejor separación
            self.estado = 'detener'
        elif self.estado == 'detener':
            return False
        return True

    def ejecutar(self):
        while self.paso():
            pass
        return ''.join(self.cinta)


class AplicacionTuring:
    def __init__(self, root):
        self.root = root
        self.root.title("Máquina de Turing - Suma Binaria")

        self.etiqueta = tk.Label(root, text="Ingrese dos o más números binarios separados por '+':")
        self.etiqueta.pack()

        self.entrada = tk.Entry(root, width=50)
        self.entrada.pack()

        self.boton_ejecutar = tk.Button(root, text="Ejecutar Máquina de Turing", command=self.ejecutar_maquina_turing)
        self.boton_ejecutar.pack()

        self.etiqueta_resultado = tk.Label(root, text="Resultado: ")
        self.etiqueta_resultado.pack()

    def ejecutar_maquina_turing(self):
        cinta = self.entrada.get()
        if '+' not in cinta:
            messagebox.showerror("Error de Entrada", "La entrada debe contener al menos dos números binarios separados por '+'.")
            return

        partes_binarias = cinta.split('+')
        if len(partes_binarias) < 2 or not all(parte.isdigit() and set(parte).issubset({'0', '1'}) for parte in partes_binarias):
            messagebox.showerror("Error de Entrada", "La entrada solo debe contener números binarios (0 y 1) separados por '+'.")
            return

        # Agregar ceros a la izquierda para que todos los números binarios tengan la misma longitud
        longitud_maxima = max(len(parte) for parte in partes_binarias)
        cinta_rellenada = '+'.join(parte.zfill(longitud_maxima) for parte in partes_binarias)

        mt = MaquinaDeTuring(cinta_rellenada)
        try:
            resultado = mt.ejecutar()
            # Extraer solo la parte del resultado después del espacio para mayor claridad
            parte_resultado = resultado.split(' ')[-1]
            resultado_decimal = int(parte_resultado, 2)
            self.etiqueta_resultado.config(text=f"Resultado: Binario: {parte_resultado}, Decimal: {resultado_decimal}")
        except RecursionError:
            messagebox.showerror("Error de Ejecución", "La Máquina de Turing encontró un bucle infinito.")


if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacionTuring(root)
    root.mainloop()