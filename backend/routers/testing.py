from fastapi import APIRouter, WebSocket

router = APIRouter()
a = 0


@router.get("/api/test_socket")
def test_socket_http():
    return "This is a real request thank you"


@router.websocket("/api/test_socket_test")
async def test_socket(websocket: WebSocket):
    await websocket.accept()

    text1 = await websocket.receive_text()
    print(text1)
    text2 = await websocket.receive_text()
    print(text2)
    await websocket.send_text("GET SCAMMED")


@router.post("/api/test")
def test():
    global a
    a += 1
    return str(a)


@router.get("/api/test")
def get_test():
    return str(a)
