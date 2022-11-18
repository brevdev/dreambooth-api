# import io
# import os
# import re
# import time
# import inspect
# import json
# from fastapi import FastAPI, File, UploadFile
# import flask
# import sys
# import base64
# from PIL import Image
# from io import BytesIO
# from starlette.responses import StreamingResponse
# from typing import Union

# import torch
# import diffusers

# app = FastAPI()


# @app.post("/txt2img")
# def stable_txt2img(file: bytes = File()):
#     # print("input prompt is: ", prompt)
#     # delay 5 seconds to simulate long-running process
#     return {"file_size": len(file)}
#     # return {"message": "Hello World"}

from uuid import uuid4
from fastapi import FastAPI, File, UploadFile, status
from fastapi.exceptions import HTTPException
import aiofiles
import os

CHUNK_SIZE = 1024 * 1024  # adjust the chunk size as desired
app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # create a uuid for the user request
    # uuid = uuid4()
    # check if directory "userzipfiles" exists, if not create it
    if not os.path.exists("./userzipfiles"):
        os.makedirs("./userzipfiles")

    try:
        filepath = os.path.join('./userzipfiles', os.path.basename(file.filename))
        async with aiofiles.open(filepath, 'wb') as f:
            while chunk := await file.read(CHUNK_SIZE):
                await f.write(chunk)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='There was an error uploading the file')
    finally:
        await file.close()

    return {"message": f"Successfuly uploaded {file.filename}"}