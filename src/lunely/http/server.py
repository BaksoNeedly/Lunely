from lunely.config import server_config
import socket
import threading
from lunely.hooks.request_hooks import RequestHooks
from lunely.http.request import HTTPRequest
from lunely.http.router import HTTPRouter
from lunely.middleware.pipeline import MiddlewarePipeline
from lunely.registrars.middleware import MiddlewareRegistrar
from lunely.session.session_manager import SessionManager
from lunely.websocket.server import WebSocketServer
from pathlib import Path
from lunely.http.response import HTTPResponse
from ..lifecycle import Lifecycle
from lunely.logging import get_logger

import time

class HTTPServer:

    def __init__(
        self, 
        host: str = "0.0.0.0", 
        port: int = 8080,
        server_name: str = "Lunely Server",
        server_id: str = "lunely"
    ):
        self._lifecycle = Lifecycle()
        self._status = False
        self._router = HTTPRouter()
        self._session_manager = SessionManager()
        self._name = server_name
        self._id = server_id
        self._logger = get_logger(server_name)
        self._websocket_server = WebSocketServer(self._session_manager, server_name=server_name)
        
        self._request_hooks = RequestHooks()
        
        self._middleware_pipeline = MiddlewarePipeline()
        
        # Registrar
        middleware_registrar = MiddlewareRegistrar(
            self._middleware_pipeline,
            self._session_manager
        )
        middleware_registrar.register()
        
        self._address = (host, port)
        
    def get_name(self) -> str:
        return self._name
    
    def get_id(self) -> str:
        return self._id
        
    def get_lifecycle(self):
        return self._lifecycle

    def get_status(self):
        return self._status
    
    def get_router(self) -> HTTPRouter:
        return self._router
    
    def get_websocket_server(self) -> WebSocketServer:
        return self._websocket_server

    def get_session_manager(self) -> SessionManager:
        return self._session_manager
    
    def get_request_hooks(self) -> RequestHooks:
        return self._request_hooks
    
    def get_middleware_pipeline(self) -> MiddlewarePipeline:
        return self._middleware_pipeline

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
        self._logger.info("Listening on " + f"{self._address}...")
        self._logger.info(f"{len(self._router.get_all())} routes are registered.")
        self._logger.info(f"{len(self._request_hooks.get_all())} request hooks are registered.")
        self._logger.info(f"{len(self._middleware_pipeline.get_all())} middlewares are registered.")
        
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
            
            # Request hooks
            for hook in self._request_hooks.get_all():
                hook(request) 
            
            session = self._session_manager.extract_session(request)
            session_id = session.get_session_id() if session else None
            if session_id:
                session_label = f"'{session_id[:8]}...'"
            else:
                session_label = "'UNKNOWN SESSION'"
            
            self._logger.info(
                f"{session_label} Request: '{request.get_url().get_full_path()}'"
            )

            headers = request.get_headers()
            upgrade = headers.get("upgrade")
            connection = headers.get("connection")
            
            if upgrade and connection:
                self._websocket_server.handle(client_socket, request)
                return

            # self.write_log(data.decode(app_config.ENCODING))
            endpoint = self.get_router().endpoint(request)
            
            middleware = self._middleware_pipeline.handle(
                request,
                endpoint
            )
            
            if middleware:
                response = middleware
            else:
                self._logger.warning(f"Failed to receive: '{request.get_method()}', '{request.get_url().get_path()}'")
 
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
        self._logger.info(msg)

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
