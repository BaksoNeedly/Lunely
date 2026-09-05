from collections.abc import Callable

from lunely.config import server_config
import socket
from ..http.request import HTTPRequest
from ..session.session_manager import SessionManager

from .handshake import WebSocketHandshake
from .router import WebSocketRouter

from ..session.client_session import ClientSession
from ..session.client_session_manager import ClientSessionManager

class WebSocketServer:
    
    def __init__(self):
        self._router = WebSocketRouter()
        
        self._access_hooks: list[Callable] = []
        
    def get_router(self) -> WebSocketRouter:
        return self._router
    
    def get_access_hooks(self) -> list[Callable]:
        return self._access_hooks
    
    def add_access_hook(self, hook: Callable) -> Callable:
        self._access_hooks.append(hook)
        return hook
    
    def handle(self, client_socket: socket.socket, request: HTTPRequest) -> None:
        WebSocketHandshake.perform(client_socket, request)
        session = SessionManager.extract_session(request)
        for hook in self._access_hooks:
            if not hook(session):
                client_socket.close()
                print("Session not found or not authenticated.")
                return
            
        
        client_session = ClientSession(client_socket, session)
        ClientSessionManager.set(client_session)
        
        
        print(client_session.get_username(), "connected.")
        print(len(ClientSessionManager.get_all()), "Users.")
        
        try:
            while True:
                raw_frame = client_socket.recv(server_config.BUFFER_SIZE)
                if not raw_frame:
                    return

                # DEBUG
                # print("Payload:", WebSocketFrame.parse(raw_frame))

                opcode = raw_frame[0] & 0b00001111
                if opcode == 0b00001000: # Close frame
                    print("CLOSE FRAME DETECTED.")
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
            ClientSessionManager.close(client_session)
            print("CLOSED")


    # @classmethod
    # def handle(cls, client_socket: socket.socket, request: HTTPRequest):
    #     WebSocketHandshake.perform(client_socket, request)        
    #     session = SessionManager.extract_session(request)
    #     if not session or not session.is_authenticated():
    #         print("Session not found or not authenticated.")
    #         client_socket.close()
    #         return
    #     session_id = session.get_session_id()
    #     client_session = ClientSession(client_socket, session)
    #     ClientSessionManager.set(client_session)
    #     if not client_session:
    #         client_socket.sendall(HTTPResponse(status="404", reason_phrase="Not Found"))
    #         client_socket.close()
    #         return
    #     print(client_session.get_username(), "connected.")

    #     print(len(ClientSessionManager.get_all()), "Users.")
        
    #     try:
    #         while True:
    #             raw_frame = client_socket.recv(server_config.BUFFER_SIZE)
    #             if not raw_frame:
    #                 return

    #             # DEBUG
    #             # print("Payload:", WebSocketFrame.parse(raw_frame))

    #             opcode = raw_frame[0] & 0b00001111
    #             if opcode == 0b00001000: # Close frame
    #                 print("CLOSE FRAME DETECTED.")
    #                 break

    #             WebSocketRouter.route(raw_frame, client_session)
    #     except (ConnectionAbortedError, ConnectionResetError, BrokenPipeError):
    #         # The browser can close the socket when navigating to another page.
    #         pass
    #     except OSError as e:
    #         # Windows reports a normal client-side disconnect as 10053/10054.
    #         if getattr(e, "winerror", None) not in (10053, 10054):
    #             print(f"Error occurred while handling WebSocket connection: {e}")
    #     except Exception as e:
    #         print(f"Error occurred while handling WebSocket connection: {e}")
    #     finally:
    #         ClientSessionManager.close(client_session)
    #         print("CLOSED")
