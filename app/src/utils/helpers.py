# validate user
from datetime import datetime

import jwt
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm.session import Session

from app.src.user.models import User
from app.src.utils.db import get_db
from app.src.utils.settings import settings


def is_authenticated(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(401, detail="Unauthorised user")
        token = token.split(" ")[-1]

        data = jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
        user_id = data.get("_id")
        exp_time = data.get("exp")
        current_time = datetime.now().timestamp()
        if current_time > exp_time:
            raise HTTPException(401, detail="Token expired")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(401, detail="Unauthorised user")
        return user

    except jwt.InvalidTokenError:
        raise HTTPException(401, detail="Unauthorised user")
