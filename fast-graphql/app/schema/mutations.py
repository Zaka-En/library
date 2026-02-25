from .inputs import ( CreateAuthorInput, UpdateAuthorInput, CreateBookInput, UpdateBookInput, StartReadingInput, UpdateProgressInput, FinishReadingInput, RegisterInput, LoginInput, UpdateUserInput, RoomBookingInput )
from .types import AuthorType, BookType, ReadingStateType, UserType, LoginResponse, UserProfileType,RoomBookingType
import strawberry
from strawberry.types import Info
from .convertors import author_to_type, book_to_type, reading_state_to_type
from time import sleep
from fastapi.concurrency import run_in_threadpool
from app.permissions.authenticated import IsAuthenticated
from app.permissions.authorized import RBAC
from app.services.user_service import UserService
from app.services.author_service import AuthorService
#from app.services.book_service import BookService
from app.services.reading_state_service import ReadingStateService
from app.services.room_booking_service import RoomBookingService
from app.broadcast import broadcast
from app.dependencies import CustomContext
from typing import Optional
from datetime import date as pyDate
from fastapi import Response

REFRESH_TOKEN_EXPIRY= 6 * 30


@strawberry.type
class Mutation:
  @strawberry.mutation
  async def register_user(self, info: Info[CustomContext, None], data: RegisterInput) -> UserType:
    user_service: UserService = info.context.user_service

    try:
      new_user = await user_service.register(data=data)
    except Exception as e:
      raise e
    
    return UserType(
      id=strawberry.ID(str(new_user.id)),
      fullname=new_user.fullname,
      name=new_user.name,
      email=new_user.email,
      rol=new_user.rol
    )
      
  @strawberry.mutation
  async def login(self, info: Info[CustomContext, None], data: LoginInput) -> LoginResponse:

    user_service: UserService = info.context.user_service

    user, access_token, refresh_token = await user_service.authenticate(data=data)

    return LoginResponse(
      access_token=access_token,
      refresh_token=refresh_token,
      token_type="bearer",
      user=UserType(
        id=strawberry.ID(str(user.id)),
        email=user.email,
        name=user.name,
        fullname=user.fullname,
        rol=user.rol
      )
    )

  #TODO: este refresh es un desastre, hay que cambiarlo 
  # @strawberry.mutation
  # async def refresh_token(self, info: Info[CustomContext, None]) -> LoginResponse:

  #   request: Request = info.context.request
  #   response: Response = info.context.response

  #   refresh_token = request.cookies.get("refresh_token", "")
   
  #   token_data = decode_token(refresh_token)

  #   if not token_data.get("refresh"):
  #       raise Exception("PROVIDED TOKEN IS NOT A REFRESH TOKEN")
    
  #   exp = token_data.get("exp")
  #   if not exp or datetime.fromtimestamp(exp) < datetime.now():
  #       raise Exception("REFRESH TOKEN EXPIRED")
    
  #   user_data = token_data.get("user")
  #   if not user_data:
  #       raise Exception("INVALID TOKEN")
    
  #   new_access_token = create_access_token(user_data=user_data)

  #   response.set_cookie(
  #     key="access_token",
  #     value=new_access_token,
  #     httponly=True,
  #     samesite="strict",
  #     #secure=True, 
  #     max_age=900  # 15 minutos
  #   )

  #   return LoginResponse(
  #     access_token=new_access_token,
  #     refresh_token=refresh_token,
  #     token_type="bearer"
  #   )

  
  @strawberry.mutation
  async def update_user(
      self, 
      info: Info[CustomContext, None], 
      input: UpdateUserInput
    ) -> Optional[UserProfileType]:
        
        user_service = info.context.user_service
        
        updated_user = await user_service.update(data=input)
        
        if not updated_user:
          raise Exception(f"Usuario con id {input.id} no encontrado")
            
        return updated_user

  @strawberry.mutation(permission_classes=[RBAC("admin", "editor")]) #TODO RBAC(roles=[.....])
  async def create_author(self, input: CreateAuthorInput, info: Info[CustomContext, None]) -> AuthorType:
    author_service: AuthorService = info.context.author_service
    author = await author_service.create(data=input)
    return author_to_type(author=author)

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def update_author(self, input: UpdateAuthorInput, info: Info[CustomContext, None]) -> AuthorType:
    author_service: AuthorService = info.context.author_service
    author = await author_service.update(data_input=input)
    return author_to_type(author=author)
    

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def delete_author(self, id: int, info: Info[CustomContext, None]) -> bool:
    author_service: AuthorService = info.context.author_service
    return await author_service.delete(author_id=id)

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def create_book(self, input: CreateBookInput, info: Info[CustomContext, None]) -> BookType:
    book_service = info.context.book_service
    book = await book_service.create(data=input)
    return book_to_type(book)

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def update_book(self, input: UpdateBookInput, info: Info[CustomContext, None]) -> BookType:
    book_service = info.context.book_service
    book = await book_service.update(data=input)
    return book_to_type(book)

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def delete_book(self, id: int, info: Info[CustomContext, None]) -> bool:
    return await info.context.book_service.delete(id=id) 

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def start_reading(self, input: StartReadingInput, info: Info[CustomContext, None]) -> ReadingStateType:
    service: ReadingStateService = info.context.reading_state_service
    reading_state = await service.start_reading(book_id=input.book_id,user_id=input.user_id)
      
    return reading_state_to_type(reading_state)

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def update_progress(self, input: UpdateProgressInput, info: Info[CustomContext, None]) -> ReadingStateType:
    service: ReadingStateService = info.context.reading_state_service
    return reading_state_to_type(await service.update_progress(state_id=input.id,current_page=input.current_page))
        
  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def finish_reading(self, input: FinishReadingInput, info: Info[CustomContext, None]) -> ReadingStateType:
    service: ReadingStateService = info.context.reading_state_service
    return reading_state_to_type(await service.finish_reading(state_id=input.id))
  
  @strawberry.mutation
  async def book_conference_room(self, input: RoomBookingInput, info: Info[CustomContext, None]) -> RoomBookingType:
    room_booking_service: RoomBookingService =  info.context.room_booking_service
    response: Response | None = info.context.response

    if room_booking_service._check_availability(
      room_id=input.room_id,
      date=pyDate.fromisoformat(input.date),
      end=input.end_hour,
      start=input.start_hour
    ):
      if response:
        response.status_code = 409
      raise Exception("CONFERENCE_ROOM_OCCUPIED")

    room_booking= await room_booking_service.create(input.to_model_dict())
    return RoomBookingType(
      id=strawberry.ID(str(room_booking.id)),
      room_id=room_booking.room_id,
      start_hour=room_booking.start_hour,
      end_hour=room_booking.end_hour,
      status= room_booking.status,
      date= pyDate.isoformat(room_booking.date),
      attendees_count=room_booking.attendees_count
    )

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def add_rating(self, text: str) -> str:
    await broadcast.publish(channel="RATINGS",message=text)
    return text

  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def generate_reporting(self, author_id: int) -> str:

    def heavy_work():
      print("heavy work")
      sleep(10)
      return "report generated"
    

    result = await run_in_threadpool(heavy_work)
    return f"hecho {result}"
  
  @strawberry.mutation(permission_classes=[IsAuthenticated])
  async def send_book_chat_message(
    self,
    book_id: int,
    user_name: str,
    message: str
  ) -> bool:
    
    channel = f"BOOK_CHAT_{book_id}"

    payload = f"{user_name}: {message}"

    await broadcast.publish(channel=channel, message=payload)

    return True 