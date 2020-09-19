from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import datetime
import cv2
import numpy as np
from yolov4.tf import YOLOv4
import cv2

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://10.1.1.12:3000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

yolo = YOLOv4()

yolo.classes = "coco.names"

yolo.make_model()
yolo.load_weights("yolov4.weights", weights_type="yolo")
 
@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        # await websocket.send_text(f"Message text was: {data}")
        # print(data)
        
        # img_name = datetime.datetime.now().strftime("%Y-%m-%d%H-%M-%S-%f")

        # imgFile = open("file/"+img_name+'.jpg', 'wb')  # 開始寫入圖片檔
        # imgFile.write(data)
        # imgFile.close()

        #轉換 收到Bytes to image        
        nparr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(nparr,cv2.IMREAD_UNCHANGED)

        data = yolo.predict(frame=img)
        print(type(data)) 
        result = yolo.draw_bboxes(img, data)


        cv2.imshow('frame', result)
        await websocket.send_text("ok")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

    # 關閉所有 OpenCV 視窗

import uvicorn
if __name__ == "__main__":
   uvicorn.run(app,host="10.1.1.12",port=3000) 