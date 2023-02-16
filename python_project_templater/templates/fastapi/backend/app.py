from fastapi import FastAPI

from . import api


tags_metadata = []

app = FastAPI(
    title='backend',
    description='description',
    version='0.1.0',
)

app.include_router(api.router)
