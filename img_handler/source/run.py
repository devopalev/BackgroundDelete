import logging
import os

import uvicorn
from fastapi import FastAPI
from fastapi import UploadFile
from rembg import remove, new_session
from starlette.responses import FileResponse, Response

app = FastAPI()
logger = logging.getLogger(__name__)
MODEL = os.getenv("MODEL")


def delete_background(img: bytes) -> Response:
    try:
        session = new_session("u2netp")
        new = remove(img, session=session)
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
    log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    with open(os.path.join(os.getcwd(), os.path.abspath("test.jpg")), "rb") as file:
        img = file.read()
    res = delete_background(img)
    if res.status_code == 200:
        logger.info("Img Handler start")
        uvicorn.run(app, host="0.0.0.0", port=8080)
    else:
        logger.error(f"Failed run server. Status code: {res.status_code}")
        exit(1)
