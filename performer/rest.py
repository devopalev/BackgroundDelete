import logging

import uvicorn
from fastapi import FastAPI
from fastapi import UploadFile
from rembg import remove
from starlette.responses import FileResponse, Response

app = FastAPI()
logger = logging.getLogger(__name__)


@app.get("/delete_background", response_class=FileResponse)
async def delete_background(file: UploadFile):
    new = remove(file.file.read())

    try:
        return Response(new)
    except Exception as err:
        logger.error(err)
        return {"result": 'server error'}, 500


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8065)
