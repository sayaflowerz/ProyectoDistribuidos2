import zmq

class SistemaCalidad:
    def __init__(self, direccion_suscripcion):
        # Configura la conexión con el Publish-Subscribe
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(direccion_suscripcion)

    def recibir_alertas(self):
        try:
            while True:
                mensaje = self.socket.recv_string()
                print(f"Alerta del sistema de calidad: {mensaje}")

        except KeyboardInterrupt:
            print("Sistema de Calidad detenido por el usuario.")
            self.cerrar()

    def cerrar(self):
        self.socket.close()
        self.context.term()

if __name__ == "__main__":
    direccion_suscripcion = "tcp://DIRECCION_IP_MAQUINA_VIRTUAL:PUERTO_DESEADO"

    sistema_calidad = SistemaCalidad(direccion_suscripcion)
    sistema_calidad.recibir_alertas()
