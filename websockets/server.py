import asyncio
import websockets


async def ws(websocket):
    name = await websocket.recv()
    print(f"Received: {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"Sent: {greeting}")


async def main():
    async with websockets.serve(ws, '127.0.0.1', 8000):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
