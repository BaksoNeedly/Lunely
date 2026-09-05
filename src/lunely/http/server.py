from lunely.config import server_config
import socket
import threading
from lunely.http.request import HTTPRequest
from lunely.http.router import HTTPRouter
from lunely.websocket.server import WebSocketServer
from pathlib import Path
from lunely.http.response import HTTPResponse
from ..lifecycle import Lifecycle

import time

class HTTPServer:

    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        self._lifecycle = Lifecycle()
        self._status = False
        self._router = HTTPRouter()        
        self._websocket_server = WebSocketServer()
        
        self._address = (host, port)
        
    def get_lifecycle(self):
        return self._lifecycle

    def get_status(self):
        return self._status
    
    def get_router(self) -> HTTPRouter:
        return self._router
    
    def get_websocket_server(self) -> WebSocketServer:
        return self._websocket_server

    def start(self) -> None:
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(self._address)
        self._server.listen()
        self._status = True        

        self.on_enable()

        while self.get_status():
            conn, _ = self._server.accept()
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def close(self) -> None:
        self._lifecycle.run_shutdown()
        self.on_disable()
        self._server.close()
    
    def on_enable(self) -> None:
        self.info("Listening on " + f"{self._address}...")
        threading.Thread(target=self.on_command).start()
        threading.Thread(target=self.time_run).start()
        self._lifecycle.run_startup()

    def on_disable(self) -> None:
        self.info("Server closed...")

    def handle_client(self, client_socket: socket.socket) -> None:
        data = b""
        while b"\r\n\r\n" not in data:
            raw = client_socket.recv(server_config.BUFFER_SIZE)
            if not raw:
                break
            data += raw

        response = HTTPResponse(
            status="404",
            reason_phrase="Not Found",
            headers={
                "Content-Type": "text/html; charset=utf-8"
            },
            body="<h1>404 Not Found</h1>"
        )

        if data:
            request = HTTPRequest(data, client_socket)

            headers = request.get_headers()
            upgrade = headers.get("upgrade")
            connection = headers.get("connection")

            if upgrade and connection:
                self._websocket_server.handle(client_socket, request)
                return

            # self.write_log(data.decode(app_config.ENCODING))
            router_result = self.get_router().route(request)

            if router_result:
                response = router_result
 
            # DEBUG
            # print("HTTPSERVER: ", SessionManager.size(), "sessions.")
            # print(len(RouteManager.get_all()), "ROUTES")
            # print("PATHS:", paths)
            # print("PATH:", request.get_url().get_path())
            # print("REQUEST BODY:", request.get_body())
            # print("RESPONSE BODY:", response.decode().split("\r\n\r\n",1)[1])
            # print(request.get_data(), "\r\n")
            # print(response.decode(app_config.ENCODING), "\r\n")        

        client_socket.sendall(response.build())
        client_socket.close()

    def time_run(self):
        while True:
            time.sleep(1)
            
            # PasswordResetTokenRepository.delete_expired(TimeUtils.get_current_time_stamp())

            # self.info(f"MESSAGES: {MessageRepository.get_messages()}")
            # MessageRepository.get_messages()

            # self.info("TOTAL SESSION: " + str(len(SessionManager.get_all())))
            # for id, s in SessionManager.get_all().items():
            #     self.info("SESSION:" + s.get_session_id() + f": {s.get_username()} {s.get_email()} {s.is_authenticated()}")

            # self.info("\n")

            # self.info("TOTAL USER: " + str(len(UserManager.get_all())))
            # for id, s in UserManager.get_all().items():
            #     self.info("USER:" + s.get_session_id() + f": {s.get_username()}")


    def info(self, msg: str) -> None:
        print("[SERVER]", msg)

    def write_log(self, log: str):
        with open(Path(__file__).parent / "log.txt", "w", encoding="utf-8") as file:
            file.write(repr(log) + "\n\n")
        with open(Path(__file__).parent / "log_.txt", "a", encoding="utf-8") as file:
            file.write(log)

    def on_command(self) -> None:
        try:
            while self.get_status():
                _ = input("> ")
        except (Exception, KeyboardInterrupt, EOFError) as e:
            self.info(str(e))
        finally:
            self.close()
