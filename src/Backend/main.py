from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Endpoints import router
import pandas
import uvicorn
import numpy as np


app = FastAPI() #FastAPI server always goes in main

 
origins = [
    "http://localhost:3000", #frontend host port //allow to send from
    "http://127.0.0.1:3000"   # Alternative frontend URL //only these 2 links will be allowed to send and fetch data from backend
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router) #without this our endpoints.py wont work, think of it as starting up the router to allow endpoints to happen













if __name__ == "__main__":
    import uvicorn #server that where running fastapi on
    uvicorn.run(app, host="127.0.0.1", port = 5000)