from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ALGORYTHM = config("ALGORYTHM")
SECRET_KEY = config("SECRET_KEY")
ACCESS_TOKEN_EXPIRES_DAY = 7
