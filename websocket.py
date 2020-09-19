import asyncio
import websockets
import numpy
import time
import cv2
import aiohttp
fps = ""
detectfps = ""
framecount = 0
detectframecount = 0
time1 = 0
time2 = 0

async def hello():
    uri = "ws://10.1.1.12:3000/ws"
    async with aiohttp.ClientSession() as session:

        async with session.ws_connect(uri) as ws:
            global fps
            global detectfps
            global lastresults
            global framecount
            global detectframecount
            global time1
            global time2

            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FPS, 150)
            cap.set(3, 320)
            cap.set(4, 240)
            while(True):

                t1 = time.perf_counter()

                # 從攝影機擷取一張影像
                ret, frame = cap.read()
                img_str = cv2.imencode('.jpg', frame)[1].tobytes()
 
                await ws.send_bytes(img_str)
                framecount += 1
                if framecount >= 15:
                    fps = "(Playback) {:.1f} FPS".format(time1/15)
                    # detectfps = "(Detection) {:.1f} FPS".format(detectframecount/time2)
                    framecount = 0
                    # detectframecount = 0
                    time1 = 0
                    time2 = 0
                t2 = time.perf_counter()
                elapsedTime = t2-t1
                time1 += 1/elapsedTime
                time2 += elapsedTime
                print(fps)

                d = await ws.receive_str()
                print(d)
        # greeting = await websocket.recv()
        # print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
