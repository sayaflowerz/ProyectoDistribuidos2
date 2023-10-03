import zmq
import time
import random

class Sensor:
    def __init__(self, tipo_sensor, intervalo_tiempo, direccion_publicacion):
        self.tipo_sensor = tipo_sensor
        self.intervalo = intervalo_tiempo

        # Configura la conexión con el Publish-Subscribe
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(direccion_publicacion)

    def generar_medicion(self):
        try:
            while True:
                # Genera mediciones aleatorias para el tipo de sensor
                if self.tipo_sensor == "temperatura":
                    medicion = random.uniform(68, 89)
                elif self.tipo_sensor == "ph":
                    medicion = random.uniform(6.0, 8.0)
                elif self.tipo_sensor == "oxigeno":
                    medicion = random.uniform(2, 11)

                # Publica la medición en el canal
                mensaje = f"{self.tipo_sensor}: {medicion}"
                self.socket.send_string(mensaje)

                # Espera según el intervalo de tiempo
                time.sleep(self.intervalo)

        except KeyboardInterrupt:
            print("Sensor detenido por el usuario.")

if __name__ == "__main__":
    tipo_sensor = "temperatura"  # Cambia el tipo de sensor según sea necesario
    intervalo_tiempo = 5  # Cambia el intervalo de tiempo según sea necesario
    direccion_publicacion = "tcp://DIRECCION_IP_MAQUINA_VIRTUAL:PUERTO_DESEADO"

    sensor = Sensor(tipo_sensor, intervalo_tiempo, direccion_publicacion)
    sensor.generar_medicion()
