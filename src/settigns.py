from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

UPLOAD_AVATAR = BASE_DIR / 'upload/images/avatar'
UPLOAD_AVATAR_URL = '/media/avatar/'

DEFAULT_AVATAR = UPLOAD_AVATAR / 'default.jpg'
DEFAULT_AVATAR_URL = UPLOAD_AVATAR_URL + 'default.jpg/'


ALGORYTHM = config("ALGORYTHM")
SECRET_KEY = config("SECRET_KEY")
ACCESS_TOKEN_EXPIRES_DAY = 7
