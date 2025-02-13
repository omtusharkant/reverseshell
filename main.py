import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        print(f"Message received: {message}")
        await websocket.send(f"Echo: {message}")

start_server = websockets.serve(echo, "0.0.0.0", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()