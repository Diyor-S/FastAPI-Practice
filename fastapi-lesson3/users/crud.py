from users.schemas import CreateUser


def create_user(user: CreateUser) -> dict:
    # user = user_in.dict() dict() is deprecated in Pydantic v2
    
    # Turning the user_in into a dictionary
    new_user = user.model_dump() # Use model_dump() instead of dict()
    
    return {
        "message": True,
        "user": new_user
    }

    