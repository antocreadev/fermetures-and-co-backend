from datetime import datetime
from os import makedirs
from typing import Annotated

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy.orm import Session
from sqlalchemy_file.storage import StorageManager
from starlette_admin.contrib.sqla import Admin, ModelView

from src.config import DESCRIPTION, TAGS_METADATA, TITLE
from src.database import create_database, engine
from src.models.models import *
from src.routes.auth import router as auth_router
from src.routes.models import router as models_router
from src.routes.user import router as user_router
from src.schemas.user import UserResponse

# Configure Storage
makedirs("./src/upload/attachment", 0o777, exist_ok=True)
container = LocalStorageDriver("./src/upload").get_container("attachment")
StorageManager.add_storage("default", container)


app = FastAPI(
    title=TITLE,
    description=DESCRIPTION,
    openapi_tags=TAGS_METADATA
)

create_database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

admin = Admin(engine)

admin.add_view(ModelView(Utilisateur))
admin.add_view(ModelView(Adresse))
admin.add_view(ModelView(Commande))
admin.add_view(ModelView(Produit))
admin.add_view(ModelView(Bois))
admin.add_view(ModelView(RAL))
admin.add_view(ModelView(Image))






admin.mount_to(app)

@app.get("/", tags=["Server"])
async def root():
    return {"message": "API T is online, welcome to the API documentation at /docs or /redocs"}

@app.get("/unixTimes", tags=["Server"])
async def read_item():
    unix_timestamp = datetime.now().timestamp()
    return {"unixTime": unix_timestamp}

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(models_router, prefix="/models", tags=["Models"])