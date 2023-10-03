import zmq
import time
import random
import sqlite3

class Monitor:
    def __init__(self, tipo_sensor, direccion_suscripcion):
        self.tipo_sensor = tipo_sensor

        # Configura la conexión con el Publish-Subscribe
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(direccion_suscripcion)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.tipo_sensor)

        # Configura el archivo de registro
        self.archivo_registro = f"{self.tipo_sensor}_registro.txt"

        # Configura la conexión a la base de datos SQLite
        self.conexion_db = sqlite3.connect(f"{self.tipo_sensor}_data.db")
        self.cursore_db = self.conexion_db.cursor()

    def recibir_mediciones(self):
        try:
            while True:
                mensaje = self.socket.recv_string()
                print(f"Medición recibida por el monitor ({self.tipo_sensor}): {mensaje}")

                # Registra la medición en el archivo
                with open(self.archivo_registro, 'a') as archivo:
                    archivo.write(f"{mensaje}\n")

                # Registra la medición en la base de datos
                self.cursore_db.execute("INSERT INTO mediciones (valor) VALUES (?)", (mensaje,))
                self.conexion_db.commit()

        except KeyboardInterrupt:
            print("Monitor detenido por el usuario.")
            self.cerrar()

    def cerrar(self):
        self.socket.close()
        self.context.term()
        self.conexion_db.close()

if __name__ == "__main__":
    tipo_sensor = "temperatura"  # Cambia el tipo de sensor según sea necesario
    direccion_suscripcion = "tcp://DIRECCION_IP_MAQUINA_VIRTUAL:PUERTO_DESEADO"

    monitor = Monitor(tipo_sensor, direccion_suscripcion)
    monitor.recibir_mediciones()
