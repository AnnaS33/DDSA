import socket, pickle
import numpy as np
import cv2
import random

CONNECTED_PATTERN = "Client connected: {}:{}"
BLOCK_SIZE = 1024


class Server(object):

    def __init__(self):
        self.client = None
        self.port = 8080
        self.host = 'localhost'
        self.port2 = 8082
        self.socket = None
        self.socket2 = None

    def add_noise(self, image, v):
        v2 = 1 - v
        output = np.zeros(image.shape, np.uint8)
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                rand = random.random()
                if rand < v:
                    output[i, j] = 0
                elif rand > v2:
                    output[i, j] = 255
                else:
                    output[i, j] = image[i][j]
        return output

    def listen(self):
        self.socket.listen(1)
        while True:
            try:
                self.client, address = self.socket.accept()
            except OSError:
                print("Connection aborted")
                return
            print(CONNECTED_PATTERN.format(*address))

            n, image_noise = self.receive()
            if n:
                self.send_image(image_noise)

    def receive(self):
        image_size_in_bytes = pickle.loads(self.client.recv(20))
        buffer = b''
        n_iter = int(image_size_in_bytes / BLOCK_SIZE) + 1
        for i in range(0, n_iter):
            buffer += self.client.recv(BLOCK_SIZE)

        if (len(buffer) == image_size_in_bytes):
            print("All image blocks are received")
        else:
            print("Lack or excess of information")
            return False, None

        image = pickle.loads(buffer)
        image_noise = self.add_noise(image, 0.05)
        cv2.imwrite('Art_noise.jpg', image_noise)
        return True, image_noise

    def send_image(self, image):
        self.socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket2.connect((self.host, self.port2))
        except (socket.error, OverflowError):
            print("Connection could not be established")
            return
        print("Connected to the server")

        image_in_bytes = pickle.dumps(image)
        image_size_in_bytes = len(image_in_bytes)
        self.socket2.send(pickle.dumps(image_size_in_bytes))

        n_remains = image_size_in_bytes - BLOCK_SIZE * int(image_size_in_bytes / BLOCK_SIZE)
        for i in range(0, image_size_in_bytes - BLOCK_SIZE, BLOCK_SIZE):
            self.socket2.sendall(image_in_bytes[i:i + BLOCK_SIZE])
        if (n_remains != 0):
            self.socket2.sendall(image_in_bytes[-n_remains:])
        self.socket2.close()
        print("Image transmitted")

    def run(self):
        print(R"Noise_Server is running...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", self.port))
        self.listen()


if __name__ == "__main__":
    try:
        Server().run()
    except RuntimeError as error:
        print("Error")
        print(str(error))
