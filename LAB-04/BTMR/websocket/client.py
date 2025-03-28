import tornado.ioloop
import tornado.websocket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class WebSocketClient:
    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop
        self.aes_key = None  # AES key will be shared manually for simplicity

    def start(self):
        self.connect_and_read()

    def stop(self):
        self.io_loop.stop()

    def connect_and_read(self):
        tornado.websocket.websocket_connect(
            url=f"ws://localhost:8888/websocket/",
            callback=self.on_connect,
        )

    def on_connect(self, future):
        try:
            self.connection = future.result()
            print("Connected to server.")
            self.connection.read_message(callback=self.on_message)
        except Exception as e:
            print(f"Connection failed: {e}")
            self.io_loop.call_later(3, self.connect_and_read)

    def on_message(self, message):
        if message is None:
            print("Disconnected, reconnecting...")
            self.connect_and_read()
            return

        # Decrypt the received message
        encrypted_message = bytes.fromhex(message)
        iv = encrypted_message[:AES.block_size]
        ciphertext = encrypted_message[AES.block_size:]
        cipher = AES.new(self.aes_key, AES.MODE_CBC, iv)
        decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

        print(f"Decrypted message from server: {decrypted_message}")
        self.connection.read_message(callback=self.on_message)

    def send_message(self, message):
        if self.connection:
            self.connection.write_message(message)

def main():
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketClient(io_loop)
    client.aes_key = bytes.fromhex(input("Enter the shared AES key (hex): "))  # Manually input the AES key
    io_loop.add_callback(client.start)

    # Add a loop to send messages
    def send_loop():
        while True:
            message = input("Enter a message to send to the server: ")
            client.send_message(message)

    # Start the send loop in a separate thread
    import threading
    threading.Thread(target=send_loop, daemon=True).start()

    io_loop.start()

if __name__ == "__main__":
    main()