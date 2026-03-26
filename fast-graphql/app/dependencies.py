from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jwt import ExpiredSignatureError, InvalidTokenError
from strawberry.fastapi import BaseContext

from app.broadcast import broadcast
from app.database import SessionLocal
from app.models.user import User
from app.schema.loaders import DataLoaders, create_loaders
from app.services.author_service import AuthorService
from app.services.book_service import BookService
from app.services.conference_room_service import ConferenceRoomService
from app.services.reading_state_service import ReadingStateService
from app.services.room_booking_service import RoomBookingService
from app.services.user_service import UserService
from app.utils.auth import decode_token


async def get_user_service():
    return UserService(session_factory=SessionLocal)


async def get_author_service():
    return AuthorService(session_factory=SessionLocal, broadcast=broadcast)


async def get_book_service():
    return BookService(session_factory=SessionLocal)


async def get_reading_state_service():
    return ReadingStateService(session_factory=SessionLocal)


async def get_conference_room_service():
    return ConferenceRoomService(session_factory=SessionLocal)


async def get_room_booking_service():
    return RoomBookingService(session_factory=SessionLocal)


async def verify_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> User:

    # TODO
    # Important: in this case username is gonna be its email
    # It is a bad implementation
    # It is just a Temporary solution: to not break the whole logic of the user service

    user = await user_service.verify(
        email=form_data.username, passwd=form_data.password
    )

    if not user:
        raise HTTPException(status_code=401, detail="INVALID_CREDENTIALS")

    return user


# ---------------AUTHENTICATION------------------
@dataclass
class AuthResult:
    user: dict | None = None
    error_message: str | None = None
    status_code: int = 200
    is_authenticated: bool = False


def get_auth_result(access_token: str) -> AuthResult:
    """Pure logic to decode access_token y inject the result in the context
    this allows us to centralize the authcheck
    It only happens here once per request
    error_message and status_code if returned are to be handled in app.permissions.authenticated.py"""

    try:
        decoded = decode_token(access_token)

        if decoded.get("refresh"):
            return AuthResult(
                error_message="INVALID_TOKEN_TYPE (REFRESH)", status_code=401
            )
        print("=" * 80)
        print("DEBUG: EN LA VALIDACION DEL TOKEN, USER DICT: ", decoded["user"])
        print("=" * 80)

        return AuthResult(user=decoded["user"], is_authenticated=True)
    except ExpiredSignatureError:
        return AuthResult(error_message="ACCESS_TOKEN_EXPIRED", status_code=401)
    except InvalidTokenError:
        return AuthResult(error_message="INVALID_ACCESS_TOKEN", status_code=401)
    except Exception as e:
        return AuthResult(error_message=f"AUTH_ERROR: {str(e)}", status_code=500)


# ---------------Context Grapqhql------------------


class CustomContext(BaseContext):
    def __init__(
        self,
        user_service: UserService,
        author_service: AuthorService,
        book_service: BookService,
        reading_state_service: ReadingStateService,
        conference_room_service: ConferenceRoomService,
        room_booking_service: RoomBookingService,
    ):
        super().__init__()
        self.user_service = user_service
        self.author_service = author_service
        self.book_service = book_service
        self.reading_state_service = reading_state_service
        self.conference_room_service = conference_room_service
        self.room_booking_service = room_booking_service

        self.loaders: DataLoaders = create_loaders(
            book_service=book_service,
            author_service=author_service,
            room_booking_service=room_booking_service,
        )

    @cached_property
    def auth(self) -> AuthResult:
        if not self.request:
            return AuthResult(error_message="NO_CONNECTION_SCOPE", status_code=500)

        user_access_token = self.request.cookies.get("access_token", "")

        if not str.strip(user_access_token):
            return AuthResult(
                error_message="UNAUTHENTICATED, MISSING TOKEN", status_code=401
            )

        return get_auth_result(user_access_token)

    # helper prop
    @cached_property
    def user(self) -> dict | None:
        return self.auth.user

    @cached_property
    def access_token(self) -> str:
        if self.request:
            print("=" * 80)
            print(
                f"access_token from context: {self.request.cookies.get('access_token', '')}"
            )
            print("=" * 80)
        return self.request.cookies.get("access_token", "") if self.request else ""

    @cached_property
    def refresh_token(self) -> str:
        if self.request:
            print("=" * 80)
            print(
                f"refresh from context: {self.request.cookies.get('refresh_token', '')}"
            )
            print("=" * 80)
        return self.request.cookies.get("refresh_token", "") if self.request else ""


async def get_context(
    user_service: Annotated[UserService, Depends(get_user_service)],
    author_service: Annotated[AuthorService, Depends(get_author_service)],
    book_service: Annotated[BookService, Depends(get_book_service)],
    reading_state_service: Annotated[
        ReadingStateService, Depends(get_reading_state_service)
    ],
    conference_room_service: Annotated[
        ConferenceRoomService, Depends(get_conference_room_service)
    ],
    room_booking_service: Annotated[
        RoomBookingService, Depends(get_room_booking_service)
    ],
) -> CustomContext:

    return CustomContext(
        user_service=user_service,
        author_service=author_service,
        book_service=book_service,
        reading_state_service=reading_state_service,
        conference_room_service=conference_room_service,
        room_booking_service=room_booking_service,
    )
