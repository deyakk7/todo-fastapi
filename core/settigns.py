from decouple import config

ALGORYTHM = config("ALGORYTHM")
SECRET_KEY = config("SECRET_KEY")
ACCESS_TOKEN_EXPIRES_DAY = 7