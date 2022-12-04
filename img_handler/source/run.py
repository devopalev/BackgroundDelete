import logging

import rembg
import uvicorn
from fastapi import FastAPI
from fastapi import UploadFile
from rembg import remove
from starlette.responses import FileResponse, Response

app = FastAPI()
logger = logging.getLogger(__name__)


def delete_background(img: bytes) -> Response:
    try:
        new = remove(img)
        return Response(new, 200)
    except Exception as err:
        logger.error(err)
        return Response('{"result": "server error"}', 500)


@app.post("/delete_background", response_class=FileResponse)
async def api_delete_background(file: UploadFile):
    return delete_background(file.file.read())


@app.get("/healthcheck")
async def api_healthcheck():
    with open("test.jpg", "rb") as file:
        img = file.read()
    res = delete_background(img)
    return res.status_code


if __name__ == "__main__":
    with open("test.jpg", "rb") as file:
        img = file.read()
    res = delete_background(img)
    if res.status_code == 200:
        uvicorn.run(app, host="0.0.0.0", port=8080)
    exit(1)
