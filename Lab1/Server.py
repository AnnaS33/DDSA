import socket, pickle
import numpy as np
import cv2

CONNECTED_PATTERN = "Client connected: {}:{}"
BLOCK_SIZE = 1024


class Server(object):

    def __init__(self):
        self.client = None
        self.port = 8082
        self.socket = None

    # Метод для рассчёта медианного фильтра
    def m_filter(self, image):

        result = np.zeros(image.shape, np.uint8)
        pr_result = np.zeros((9, 3))

        for a in range(1, image.shape[0] - 1):
            for b in range(1, image.shape[1] - 1):
                pr_result[0:3] = image[a - 1:a + 2, b][0:3]
                pr_result[3:6] = image[a - 1:a + 2, b + 1][0:3]
                pr_result[6:9] = image[a - 1:a + 2, b - 1][0:3]

                p = sorted(pr_result[0:10, 0])
                p2 = sorted(pr_result[0:10, 1])
                p3 = sorted(pr_result[0:10, 2])

                result[a, b][0] = p[4]
                result[a, b][1] = p2[4]
                result[a, b][2] = p3[4]

        # Обрабатываем граничные пиксели
        result[0, :] = result[1, :]
        result[image.shape[0] - 1, :] = result[image.shape[0] - 2, :]
        result[:, 0] = result[:, 1]
        result[:, image.shape[1] - 1] = result[:, image.shape[1] - 2]

        return result

    def comparison(self, image, str1):
        image_or = cv2.imread('Art.jpg')
        result = cv2.absdiff(image_or, image)

        p = 0
        size_im=image.shape[0] * image.shape[1]
        for i in range(0, result.shape[0]):
            for j in range(0, result.shape[1]):
                if (sum(result[i, j], 0) > 20):
                    p += 1

        print("Standard deviation for image " + str1, np.std(result))
        print("Percentage of untouched pixels ",(size_im - p) * 100 / size_im, "%")

    def listen(self):
        self.socket.listen(1)
        while True:
            try:
                self.client, address = self.socket.accept()
            except OSError:
                print("Connection aborted")
                return
            print(CONNECTED_PATTERN.format(*address))
            self.receive()

    def receive(self):
        image_size_in_bytes = pickle.loads(self.client.recv(20))
        buffer = b''
        for i in range(0, int(image_size_in_bytes / BLOCK_SIZE) + 1):
            buffer += self.client.recv(BLOCK_SIZE)

        if (len(buffer) == image_size_in_bytes):
            print("All image blocks are received")
        else:
            print("Lack or excess of information")
            return

        image = pickle.loads(buffer)
        result_image = self.m_filter(image)
        cv2.imwrite('Result_art.jpg', result_image)

        self.comparison(image, "with noise")
        self.comparison(result_image, "without noise")

    def run(self):
        print(R"Server is running...")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(("", self.port))
        self.listen()


if __name__ == "__main__":
    try:
        Server().run()
    except RuntimeError as error:
        print("Error")
        print(str(error))