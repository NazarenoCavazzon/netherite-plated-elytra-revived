#!/usr/bin/env python3
"""Cliente RCON mínimo para la prueba automática del servidor."""
import socket
import struct
import sys
import time

HOST = "127.0.0.1"
PORT = 25579
PASSWORD = "testpack"


class Rcon:
    def __init__(self, host, port, password):
        self.sock = socket.create_connection((host, port), timeout=10)
        self.rid = 0
        self._send(3, password)
        rid, _ = self._recv()
        if rid == -1:
            raise SystemExit("RCON auth failed")

    def _send(self, ptype, body):
        self.rid += 1
        data = struct.pack("<ii", self.rid, ptype) + body.encode("utf8") + b"\x00\x00"
        self.sock.sendall(struct.pack("<i", len(data)) + data)

    def _recvall(self, n):
        buf = b""
        while len(buf) < n:
            chunk = self.sock.recv(n - len(buf))
            if not chunk:
                raise EOFError
            buf += chunk
        return buf

    def _recv(self):
        (length,) = struct.unpack("<i", self._recvall(4))
        data = self._recvall(length)
        rid, ptype = struct.unpack("<ii", data[:8])
        body = data[8:-2].decode("utf8", "replace")
        return rid, body

    def cmd(self, command):
        self._send(2, command)
        _, body = self._recv()
        return body


def main():
    r = Rcon(HOST, PORT, PASSWORD)
    for cmd in sys.argv[1:]:
        print(f"$ {cmd}")
        print(r.cmd(cmd))
        time.sleep(0.3)


if __name__ == "__main__":
    main()
