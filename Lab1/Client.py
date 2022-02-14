import cv2
import socket, pickle

BLOCK_SIZE = 1024


class Client(object):
    def __init__(self, port, host):
        self.host = host
        self.port = port
        self.socket = None

    def execute(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, self.port))
        except (socket.error, OverflowError):
            print("Connection could not be established")
            return False
        print("Connected to the server")
        return True

    def send_image(self, image):
        image_in_bytes = pickle.dumps(image)
        image_size_in_bytes = len(image_in_bytes)

        self.socket.send(pickle.dumps(len(image_in_bytes)))
        print("The size of the image is sent")

        n_remains = image_size_in_bytes - BLOCK_SIZE * int(image_size_in_bytes / BLOCK_SIZE)
        for i in range(0, image_size_in_bytes - BLOCK_SIZE, BLOCK_SIZE):
            self.socket.sendall(image_in_bytes[i:i + BLOCK_SIZE])

        if (n_remains != 0):
            self.socket.sendall(image_in_bytes[-n_remains:])
        print("Image transmitted")


if __name__ == '__main__':
    image_or = cv2.imread('Art.jpg')
    client = Client(8080, 'localhost')
    if (client.execute()):
        client.send_image(image_or)
