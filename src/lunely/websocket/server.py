from collections.abc import Callable

from lunely.config import server_config
import socket

from lunely.logging import log_info
from lunely.session.session import Session
from ..http.request import HTTPRequest
from ..session.session_manager import SessionManager

from .handshake import WebSocketHandshake
from .router import WebSocketRouter

from ..session.client_session import ClientSession
from ..session.client_session_manager import ClientSessionManager
from .broadcaster import WebSocketBroadcaster

SessionHandler = Callable[[Session], None]

class WebSocketServer:
    
    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager
        self._client_session_manager = ClientSessionManager()
        self._broadcaster = WebSocketBroadcaster(self._client_session_manager)
        self._router = WebSocketRouter()
        
        self._access_hooks: list[SessionHandler] = []
        
    def get_router(self) -> WebSocketRouter:
        return self._router

    def get_client_session_manager(self) -> ClientSessionManager:
        return self._client_session_manager

    def get_broadcaster(self) -> WebSocketBroadcaster:
        return self._broadcaster
    
    def get_access_hooks(self) -> list[SessionHandler]:
        return self._access_hooks
    
    def add_access_hook(self, hook: SessionHandler) -> SessionHandler:
        self._access_hooks.append(hook)
        return hook
    
    def handle(self, client_socket: socket.socket, request: HTTPRequest) -> None:
        WebSocketHandshake.perform(client_socket, request)
        session = self._session_manager.extract_session(request)
        if not session:
            client_socket.close()
            print("Session not found.")
            return
        
        for hook in self._access_hooks:
            if not hook(session):
                client_socket.close()
                print("Access denied.")
                return
            
        
        client_session = ClientSession(client_socket, session)
        self._client_session_manager.set(client_session)
        session_id = session.get_session_id()
        if session_id:
            session_label = f"'{session_id[:8]}...'"
        else:
            session_label = "'UNKNOWN SESSION'"
        
        log_info(f"{session_label} is connected.", "WEBSOCKET")
        log_info(f"{len(self._client_session_manager.get_all())} User(s) are connected.", "WEBSOCKET")
        
        try:
            while True:
                raw_frame = client_socket.recv(server_config.BUFFER_SIZE)
                if not raw_frame:
                    return

                # DEBUG
                # print("Payload:", WebSocketFrame.parse(raw_frame))

                opcode = raw_frame[0] & 0b00001111
                if opcode == 0b00001000: # Close frame
                    break

                self._router.route(raw_frame, client_session)
        except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
            # The browser can close the socket when navigating to another page.
            pass
        except OSError as e:
            # Windows reports a normal client-side disconnect as 10053/10054.
            if getattr(e, "winerror", None) not in (10053, 10054):
                print(f"Error occurred while handling WebSocket connection: {e}")
        except Exception as e:
            print(f"Error occurred while handling WebSocket connection: {e}")
        finally:
            self._client_session_manager.close(client_session)
            log_info(f"{session_label} is closed.", "WEBSOCKET")