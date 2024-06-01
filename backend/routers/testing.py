from fastapi import APIRouter, WebSocket, Response

router = APIRouter()
a = 0


@router.get("/api/test_socket")
def test_socket_http():
    """
    HTTP endpoint for testing the API connection.

    Returns:
        str: A confirmation message indicating the request was received.
    """
    return "This is a real request thank you"


@router.websocket("/api/test_socket_test")
async def test_socket(websocket: WebSocket):
    """
    WebSocket endpoint for testing the WebSocket connection.

    This endpoint accepts a WebSocket connection, receives two messages,
    prints them, and then sends a response message.

    Args:
        websocket (WebSocket): The WebSocket connection instance.
    """
    await websocket.accept()

    text1 = await websocket.receive_text()
    print(text1)
    text2 = await websocket.receive_text()
    print(text2)
    await websocket.send_text("GET SCAMMED")


@router.post("/api/test")
def increment_test():
    """
    HTTP POST endpoint to increment a global counter.

    Returns:
        str: The updated value of the counter.
    """
    global a
    a += 1
    return str(a)


@router.get("/api/test")
def get_test():
    """
    HTTP GET endpoint to retrieve the current value of a global counter.

    Returns:
        str: The current value of the counter.
    """
    return str(a)


with open("assets/pop.mp3", "rb") as f:
    pop_file_data = f.read()


@router.get("/api/pop.mp3",
            responses={
                200: {
                    "content": {"audio/mpeg": {}}
                }
            },
            response_class=Response
            )
def pop():
    """
    HTTP GET endpoint to serve an MP3 file.

    Returns:
        Response: A response containing the MP3 file data with the appropriate media type.
    """
    return Response(content=pop_file_data, media_type="audio/mpeg")
