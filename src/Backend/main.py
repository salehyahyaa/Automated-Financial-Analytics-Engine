from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Endpoints import router
import pandas 
import numpy as np


app = FastAPI()


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allowing frontend to call backend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include all API endpoints
app.include_router(router)   

# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)