from fastapi import FastAPI
from Routes import fileProcessing_route, HTML_route

app = FastAPI()

# Include the routes from routes.py
app.include_router(HTML_route.router)
app.include_router(fileProcessing_route.router)
