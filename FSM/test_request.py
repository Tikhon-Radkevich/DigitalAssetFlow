import asyncio
import websockets


async def connect_to_binance_websocket():
    url = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
    while True:
        try:
            async with websockets.connect(url) as websocket:
                # Do something with the websocket connection
                await websocket.send("Hello, Binance!")
                response = await websocket.recv()
                print(response)
        except websockets.exceptions.ConnectionClosed as e:
            # Handle connection closed exception
            print(f"Connection closed: {e}")
        except Exception as e:
            # Handle other exceptions
            print(f"Exception occurred: {e}")

        # Wait for 24 hours before attempting to reconnect
        await asyncio.sleep(86400)


# Run the event loop
asyncio.get_event_loop().run_until_complete(connect_to_binance_websocket())