from fastapi import APIRouter, WebSocket, Response

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


with open("assets/pop.mp3", "rb") as f:
    pop_file_data = f.read()


@router.get("/api/pop.mp3",
            responses = {
                200: {
                    "content": {"audio/mpeg": {}}
                    }
                },
            response_class=Response
            )
def pop():
    return Response(content=pop_file_data, media_type="audio/mpeg")
