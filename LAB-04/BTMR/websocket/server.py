import random
import tornado.ioloop
import tornado.web
import tornado.websocket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class WebSocketServer(tornado.websocket.WebSocketHandler):
    clients = set()
    aes_key = get_random_bytes(16)  # Generate a random AES key

    def open(self):
        WebSocketServer.clients.add(self)

    def on_message(self, message):
        # Encrypt the received message
        cipher = AES.new(WebSocketServer.aes_key, AES.MODE_CBC)
        ciphertext = cipher.iv + cipher.encrypt(pad(message.encode(), AES.block_size))
        self.write_message(ciphertext.hex())  # Send encrypted message back to the client

    def on_close(self):
        WebSocketServer.clients.remove(self)

class RandomWordSelector:
    def __init__(self, word_list):
        self.word_list = word_list

    def sample(self):
        return random.choice(self.word_list)

def main():
    app = tornado.web.Application(
        [(r"/websocket/", WebSocketServer)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )
    app.listen(8888)
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.start()

if __name__ == "__main__":
    main()