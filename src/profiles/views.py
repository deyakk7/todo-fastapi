from src.auth.dependencies import db_dependency
from src.profiles.models import Profile


def create_profile(db: db_dependency, user_id: int):
    profile = Profile(user_id=user_id)

    db.add(profile)
    db.commit()
    db.refresh(profile)
