import zmq

class Config:
    def __init__(self, direccion):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(direccion)

    def publicar(self, topico, mensaje):
        mensaje_completo = f"{topico} {mensaje}"
        self.socket.send_string(mensaje_completo)

    def cerrar(self):
        self.socket.close()
        self.context.term()

class Suscriptor:
    def __init__(self, direccion):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(direccion)

    def suscribir(self, topico):
        self.socket.setsockopt_string(zmq.SUBSCRIBE, topico)

    def recibir_mensaje(self):
        mensaje = self.socket.recv_string()
        return mensaje

    def cerrar(self):
        self.socket.close()
        self.context.term()
