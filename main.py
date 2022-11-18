from datetime import datetime
import uvicorn
import io
import primePy.primes as primes
from PIL import Image
import PIL.ImageOps
from passlib.context import CryptContext
from fastapi import FastAPI, Depends, File
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
manual_db = {
    "user1": {
        "username": "user1",
        "hashed_password": "$2b$12$N4VmRvBAPix/lqZORd7VlucaR8OnBm.R9JDIqj.r3LNFjGODX0fwK" #123456qwerty
    }
}

@app.get("/")
async def root():
    return {"HOME"}

@app.get("/date")
async def get_date(token: str = Depends(oauth2_scheme)):
   now = datetime.now()
   return {now.strftime("%m/%d/%Y, %H:%M:%S")}

class UserInDB(BaseModel):
    username: str
    hashed_password: str


def get_user(db, username: str) -> UserInDB:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(username, password):
    user = get_user(manual_db, username)

    if user:
        password_check = pwd_context.verify(password, user.hashed_password)
        return password_check
    else:
        return False

@app.get("/prime/{number}")
async def is_prime(number):
       if number.isnumeric():
            number = int(number)
            if number == 1:
                return {False}
            if number < 9223372036854775807:
                return {primes.check(number)}
            else:
                return {'Provided number 2 big'}
       else:
           return {'Provide int value'}


@app.post("/picture/invert/")
async def Image_inverter(file: bytes = File(...)):
    jpg = PIL.ImageOps.invert(Image.open(io.BytesIO(file)))
    jpg_display = io.BytesIO()
    jpg.save(jpg_display, format="JPEG")
    jpg_display.seek(0)
    return StreamingResponse(content=jpg_display, media_type="image/jpeg")


@app.post('/token')
def login(form_data: OAuth2PasswordRequestForm= Depends()):
    username = form_data.username
    password = form_data.password
    if authenticate_user(username, password):
        return {'Hello, %s' % username}
    else:
        return {'Invalid user'}


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")

