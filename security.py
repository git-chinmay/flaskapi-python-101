from models.user import UserModel
from hmac import compare_digest


def authentication(username, password):
    """Check the provided username matches the name inside username_mapping
     and if matches retunr the user object"""

    user = UserModel.find_by_username(username)
    # Simple == compare will also work but hmac is popularily use in authectivation context
    if user and compare_digest(user.password, password):
        return user

def identity(payload):
    """payload: JWT token send from postman call as header
       Check the provided payload's identity matches the userid inside userid_mapping
       and if matches retunr the userid object"""
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
