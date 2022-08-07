from user import User
import hmac

USERS=[
    User(1,'bob','pass123')
]

USER_NAME_MAPPING={
    u.username: u for u in USERS
}

USER_ID_MAPPING={
    u.id: u for u in USERS
}

def authenticate(username,password):
    user = USER_NAME_MAPPING.get(username,None)
    if user and hmac.compare_digest(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return USER_ID_MAPPING.get(user_id,None)