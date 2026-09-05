from backend.controllers.asset_controller import AssetController
from backend.controllers.auth_controller import AuthController
from backend.controllers.chat_controller import ChatController
from backend.controllers.file_controller import FileController
from backend.controllers.page_controller import PageController
from backend.controllers.password_reset_controller import PasswordResetController
from backend.controllers.room_controller import RoomController
from backend.controllers.user_controller import UserController

from .router import HTTPRouter


class HttpRouterRegistrar:
    def __init__(self, router: HTTPRouter):
        self._router = router

    def _register_asset(self, path: str, filename: str, directory: str = None):
        def handler(request):
            if directory is None:
                return AssetController.serve_response(filename)

            return AssetController.serve_response(filename, directory)

        self._router.get(path, handler)

    def _register_assets(self, routes):
        for route in routes:
            path, filename, *directory = route
            asset_directory = directory[0] if directory else None
            self._register_asset(path, filename, asset_directory)

    def register_routes(self) -> None:
        # Dynamic routes
        self._router.post("/reset/password", AuthController.reset_password)
        self._router.get(
            "/reset/password/check",
            AuthController.redirect_to_reset_password,
        )
        self._router.post(
            "/reset/password/request",
            PasswordResetController.request_reset,
        )

        # Main
        self._router.get("/", PageController.serve_login_page)

        # CSS and images
        self._register_assets(
            [
                ("/css/style.css", "style.css"),
                ("/css/form.css", "form.css"),
                ("/css/success.css", "success.css"),
                ("/css/chat.css", "chat.css"),
                ("/css/error.css", "error.css"),
                ("/css/email.css", "email.css"),
                ("/img/user_icon.jpg", "user_icon.jpg"),
            ]
        )

        # Login
        self._router.get("/page/login", PageController.serve_login_page)
        self._register_assets(
            [
                ("/page/email", "email.html"),
                (
                    "/js/auth/email/Email.js",
                    "Email.js",
                    "frontend/js/auth/email/",
                ),
                (
                    "/js/auth/email/EmailUI.js",
                    "EmailUI.js",
                    "frontend/js/auth/email/",
                ),
                (
                    "/js/packets/PasswordResetRequestPacket.js",
                    "PasswordResetRequestPacket.js",
                    "frontend/js/packets/",
                ),
                (
                    "/js/packets/UserPacket.js",
                    "UserPacket.js",
                    "frontend/js/packets/",
                ),
                (
                    "/js/packets/http/ResetPasswordPacket.js",
                    "ResetPasswordPacket.js",
                    "frontend/js/packets/http/",
                ),
                ("/page/reset-password", "reset-password.html"),
                (
                    "/js/auth/reset-password/ResetPassword.js",
                    "ResetPassword.js",
                    "frontend/js/auth/reset-password/",
                ),
                ("/css/reset-password.css", "reset-password.css"),
                ("/page/error", "error.html"),
            ]
        )
        self._router.post("/auth/login", AuthController.login)
        self._router.get("/auth/logout", AuthController.logout)
        self._register_assets(
            [
                (
                    "/js/auth/login/Login.js",
                    "Login.js",
                    "frontend/js/auth/login/",
                ),
                (
                    "/js/auth/login/LoginUI.js",
                    "LoginUI.js",
                    "frontend/js/auth/login/",
                ),
                (
                    "/js/packets/LoginPacket.js",
                    "LoginPacket.js",
                    "frontend/js/packets/",
                ),
            ]
        )

        # Register
        self._router.get("/page/register", PageController.serve_register_page)
        self._register_assets(
            [
                (
                    "/page/register/success",
                    "registration-success.html",
                ),
                (
                    "/css/registration-success.css",
                    "registration-success.css",
                ),
            ]
        )
        self._router.post("/auth/register", AuthController.register)

        # Email verification
        self._register_assets(
            [
                ("/page/verification", "verification.html"),
                (
                    "/js/auth/verification/Verification.js",
                    "Verification.js",
                    "frontend/js/auth/verification/",
                ),
                (
                    "/js/auth/verification/VerificationHeaderUI.js",
                    "VerificationHeaderUI.js",
                    "frontend/js/auth/verification/",
                ),
                (
                    "/js/auth/verification/VerificationBodyUI.js",
                    "VerificationBodyUI.js",
                    "frontend/js/auth/verification/",
                ),
                (
                    "/js/auth/verification/VerificationFooterUI.js",
                    "VerificationFooterUI.js",
                    "frontend/js/auth/verification/",
                ),
                ("/page/verified", "verified.html"),
                ("/css/verified.css", "verified.css"),
                ("/page/account-deleted", "account-deleted.html"),
                (
                    "/css/account-deleted.css",
                    "account-deleted.css",
                ),
                ("/css/verification.css", "verification.css"),
                (
                    "/js/auth/register/Register.js",
                    "Register.js",
                    "frontend/js/auth/register/",
                ),
                (
                    "/js/auth/register/RegisterUI.js",
                    "RegisterUI.js",
                    "frontend/js/auth/register/",
                ),
                (
                    "/js/packets/RegisterPacket.js",
                    "RegisterPacket.js",
                    "frontend/js/packets/",
                ),
                (
                    "/js/packets/VerificationCodePacket.js",
                    "VerificationCodePacket.js",
                    "frontend/js/packets/",
                ),
                (
                    "/js/packets/http/UserPacket.js",
                    "UserPacket.js",
                    "frontend/js/packets/http/",
                ),
                (
                    "/js/packets/http/SearchUserPacket.js",
                    "SearchUserPacket.js",
                    "frontend/js/packets/http/",
                ),
                (
                    "/js/packets/http/NewChatPacket.js",
                    "NewChatPacket.js",
                    "frontend/js/packets/http/",
                ),
                (
                    "/js/packets/http/NewContactPacket.js",
                    "NewContactPacket.js",
                    "frontend/js/packets/http/",
                ),
            ]
        )

        # Chat
        self._router.get("/page/chat", ChatController.serve_chat_page)
        # self._router.post("/chat", UserController.chat)
        self._router.post("/chat/new", UserController.check_online_user)
        self._router.post("/chat/search", ChatController.search_online_user)

        self._register_assets(
            [
                ("/js/core/WebSocketClient.js", "WebSocketClient.js", "frontend/js/core/"),
                ("/js/core/ApiResponse.js", "ApiResponse.js", "frontend/js/core/"),
                ("/js/chat/Chat.js", "Chat.js", "frontend/js/chat/"),
                ("/js/chat/ChatApp.js", "ChatApp.js", "frontend/js/chat/"),
                (
                    "/js/chat/ui/chat/ChatUI.js",
                    "ChatUI.js",
                    "frontend/js/chat/ui/chat",
                ),
                (
                    "/js/chat/ui/chat/ChatHeaderUI.js",
                    "ChatHeaderUI.js",
                    "frontend/js/chat/ui/chat",
                ),
                (
                    "/js/chat/ui/chat/ChatBodyUI.js",
                    "ChatBodyUI.js",
                    "frontend/js/chat/ui/chat",
                ),
                (
                    "/js/chat/ui/chat/area/ChatAreaUI.js",
                    "ChatAreaUI.js",
                    "frontend/js/chat/ui/chat/area",
                ),
                (
                    "/js/chat/ui/chat/area/ChatAreaHeaderUI.js",
                    "ChatAreaHeaderUI.js",
                    "frontend/js/chat/ui/chat/area",
                ),
                (
                    "/js/chat/ui/chat/area/ChatAreaBodyUI.js",
                    "ChatAreaBodyUI.js",
                    "frontend/js/chat/ui/chat/area",
                ),
                (
                    "/js/chat/ui/chat/area/ChatAreaFooterUI.js",
                    "ChatAreaFooterUI.js",
                    "frontend/js/chat/ui/chat/area",
                ),
                (
                    "/js/chat/ui/chat/list/ChatListUI.js",
                    "ChatListUI.js",
                    "frontend/js/chat/ui/chat/list",
                ),
                (
                    "/js/chat/ui/chat/list/ChatListHeaderUI.js",
                    "ChatListHeaderUI.js",
                    "frontend/js/chat/ui/chat/list",
                ),
                (
                    "/js/chat/ui/chat/list/ChatListBodyUI.js",
                    "ChatListBodyUI.js",
                    "frontend/js/chat/ui/chat/list",
                ),
                (
                    "/js/chat/ui/chat/list/ChatListFooterUI.js",
                    "ChatListFooterUI.js",
                    "frontend/js/chat/ui/chat/list",
                ),
                (
                    "/js/chat/ui/chat/users/UsersListUI.js",
                    "UsersListUI.js",
                    "frontend/js/chat/ui/chat/users",
                ),
                (
                    "/js/chat/ui/chat/users/UsersListHeaderUI.js",
                    "UsersListHeaderUI.js",
                    "frontend/js/chat/ui/chat/users",
                ),
                (
                    "/js/chat/ui/chat/users/UsersListBodyUI.js",
                    "UsersListBodyUI.js",
                    "frontend/js/chat/ui/chat/users",
                ),
                (
                    "/js/chat/ui/chat/users/UsersListFooterUI.js",
                    "UsersListFooterUI.js",
                    "frontend/js/chat/ui/chat/users",
                ),
                (
                    "/js/chat/ui/overlay/new-chat/NewChatUI.js",
                    "NewChatUI.js",
                    "frontend/js/chat/ui/overlay/new-chat/",
                ),
                (
                    "/js/chat/ui/overlay/settings/SettingsUI.js",
                    "SettingsUI.js",
                    "frontend/js/chat/ui/overlay/settings/",
                ),
                (
                    "/js/chat/ui/overlay/settings/SettingsHeaderUI.js",
                    "SettingsHeaderUI.js",
                    "frontend/js/chat/ui/overlay/settings/",
                ),
                (
                    "/js/chat/ui/overlay/settings/SettingsBodyUI.js",
                    "SettingsBodyUI.js",
                    "frontend/js/chat/ui/overlay/settings/",
                ),
                (
                    "/js/chat/ui/overlay/settings/SettingsFooterUI.js",
                    "SettingsFooterUI.js",
                    "frontend/js/chat/ui/overlay/settings/",
                ),
                (
                    "/js/chat/ui/overlay/new-chat/NewChatHeaderUI.js",
                    "NewChatHeaderUI.js",
                    "frontend/js/chat/ui/overlay/new-chat/",
                ),
                (
                    "/js/chat/ui/overlay/new-chat/NewChatBodyUI.js",
                    "NewChatBodyUI.js",
                    "frontend/js/chat/ui/overlay/new-chat/",
                ),
                (
                    "/js/chat/ui/overlay/new-chat/NewChatFooterUI.js",
                    "NewChatFooterUI.js",
                    "frontend/js/chat/ui/overlay/new-chat/",
                ),
                (
                    "/js/chat/ui/sidebar/SidebarUI.js",
                    "SidebarUI.js",
                    "frontend/js/chat/ui/sidebar",
                ),
                (
                    "/js/chat/ui/sidebar/SidebarHeaderUI.js",
                    "SidebarHeaderUI.js",
                    "frontend/js/chat/ui/sidebar",
                ),
                (
                    "/js/chat/ui/sidebar/SidebarBodyUI.js",
                    "SidebarBodyUI.js",
                    "frontend/js/chat/ui/sidebar",
                ),
                (
                    "/js/chat/ui/sidebar/SidebarFooterUI.js",
                    "SidebarFooterUI.js",
                    "frontend/js/chat/ui/sidebar",
                ),
                ("/js/chat/ChatService.js", "ChatService.js", "frontend/js/chat/"),
                ("/js/chat/models/Connect.js", "Connect.js", "frontend/js/chat/models/"),
                (
                    "/js/chat/packets/CreateRoom.js",
                    "CreateRoom.js",
                    "frontend/js/chat/packets/",
                ),
                (
                    "/js/chat/message/Message.js",
                    "Message.js",
                    "frontend/js/chat/message/",
                ),
                (
                    "/js/chat/message/MessageManager.js",
                    "MessageManager.js",
                    "frontend/js/chat/message/",
                ),
                ("/js/chat/user/User.js", "User.js", "frontend/js/chat/user/"),
                (
                    "/js/chat/user/UserService.js",
                    "UserService.js",
                    "frontend/js/chat/user/",
                ),
                ("/js/chat/user/Contact.js", "Contact.js", "frontend/js/chat/user/"),
                ("/js/chat/room/Member.js", "Member.js", "frontend/js/chat/room/"),
                ("/js/chat/room/Room.js", "Room.js", "frontend/js/chat/room/"),
                (
                    "/js/chat/room/RoomManager.js",
                    "RoomManager.js",
                    "frontend/js/chat/room/",
                ),
                (
                    "/js/chat/room/RoomService.js",
                    "RoomService.js",
                    "frontend/js/chat/room/",
                ),
                (
                    "/js/packets/NewChatPacket.js",
                    "NewChatPacket.js",
                    "frontend/js/packets/",
                ),
                ("/js/utils/TimeUtils.js", "TimeUtils.js", "frontend/js/utils/"),
            ]
        )

        # WebSocket packets
        websocket_packets = [
            "JoinPacket",
            "MessagePacket",
            "JoinMessagePacket",
            "MessageHistoryPacket",
            "FilePacket",
            "EnterRoomPacket",
            "UserEnterRoomPacket",
            "LeaveRoomPacket",
            "GlobalJoinPacket",
            "UpdateStatusPacket",
            "TotalUserPacket",
        ]
        self._register_assets(
            [
                (
                    f"/js/packets/websocket/{packet}.js",
                    f"{packet}.js",
                    "frontend/js/packets/websocket/",
                )
                for packet in websocket_packets
            ]
        )

        # User
        self._router.get("/user/profile", UserController.load_user_profile)
        self._router.get("/user/contact", UserController.load_contacts)
        self._router.post("/user/contact/new", UserController.new_contact)
        self._router.get("/user/verify", UserController.start_verification)
        self._router.post("/user/verify/code", UserController.verify_code)
        self._router.get("/user/return", UserController.redirect_to_chat)
        self._router.get("/user/account/delete", UserController.delete_account)

        # Files
        self._router.post("/download", FileController.download)
        self._router.post("/upload", FileController.upload)

        # Room
        self._router.post("/room/message", RoomController.load_message)

        # Other
        self._router.get("/users", UserController.load_users)
