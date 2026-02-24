import strawberry
from app.broadcast import broadcast
from typing import AsyncGenerator


@strawberry.type
class Subscription:

  @strawberry.subscription
  async def book_ratings(self) -> AsyncGenerator[str, None]:
    async with broadcast.subscribe(channel="RATINGS") as subscriber:
      while True:
        event = await subscriber.get()
        yield event.message
  
  @strawberry.subscription
  async def update_author_notifications(self) -> AsyncGenerator[str, None]:
    async with broadcast.subscribe(channel="NOTIFICATIONS") as subscriber:
      while True:
        event = await subscriber.get()
        yield event.message

  @strawberry.subscription
  async def book_chat(self, book_id: int) -> AsyncGenerator[str,None] :
    channel = f"BOOK_CHAT_{book_id}"
    async with broadcast.subscribe(channel=channel) as subscriber:
      while True:
        event = await subscriber.get()
        print(f"PUBLISHED to all subscriber : {event.message}")
        yield event.message