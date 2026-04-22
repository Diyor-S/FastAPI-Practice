import secrets  # imported secrets to actually get to compare at constant time two values - [str, str] or [byte, byte]
import uuid

from fastapi import APIRouter, Depends, HTTPException, status  # APIRouter for routes , Depends for dependency injection
# system  HTTPException for throwing exceptions , and status to showing status code when those exceptions occur.
from fastapi.security import HTTPBasic, HTTPBasicCredentials  # Http Basic for basic username, password authentication
# HTTPBasicCredentials is what actually stores username and password stuff.
from typing import Annotated, Any # Annotated for type hints.
from fastapi import Header, Response, Cookie  # Header to receive data from the response header
from time import time


router = APIRouter()  # creating an instance of APIRouter class through it now we can access attributes, and methods
# of APIRouter class.

security = HTTPBasic()  # Creating an instance of HTTPBasic which defines the method __call__, which accepts


# an 'instance' - 'self' in this case 'security' and request. Method __call__ returns an instance of
# 'HTTPBasicCredentials' - return HTTPBasicCredentials(username=username, password=password) ---> this means that
# when I just take a reference as 'security' to HTTPBasic class. Here, 'security' is an instance of HTTPBasic still.
# However, when I actually call this instance 'security', yeah it is callable because of that __call__ method. And later
# on, I am using Depends(security) which calls this security(request) etc I do not know deep down yet. This then, gives
# me an instance of the HTTPBasicCredentials with both username, and password coming from the request.
# So then I am creating another reference to the return value of this Depends(security) to access its 2 attributes
# which are 'username' and 'password'.


# Here 'I' think not the 'Fact', just my opinion. Since 'router' is an 'instance' of the class 'APIRouter', I can access
# attributes, and methods of that class through this instance. And I confirmed that class APIRouter has the method not
# only 'get', but also 'put', 'post' etc. So when I checked the source code, there were a whole novel of parameters only
# a handful of which were required positional parameters. And here I think @router.get(path) does this:
# router.get(path)(get_auth_basic_credentials(params)) - I am not sure about this syntax I will double-check it, yet I
# believe this a decorator. And I already confirmed the fact that actually get returns a CallableDecorator,
# to precise, it is 'self.api_route' that is being returned with all the params being passed. And when I went even
# deeper this method 'api_route' defines the 'decorator' - 'inner' function. This decorator before it returns just my
# function get_auth_basic_credentials for example, it first calls another method 'self.add_api_route' and 'api_route'
# then returns a decorator which returns my function, respectively. So what should I understand from this, is that
# I should really master those decorators, generators, because I am still lacking in not only implementation, but also
# the understanding the decorators at least in the source code.

# Looks like I was a bit wrong:
# my_func = router.get(path | other params)(my_func) -> my_func without params. The reason is I would have been calling
# it immediately after I return my func which is not the intended output. Though I still do not get when actually my
# func is being called. Well, I get it that it happens when the request comes. But the issue is I can't quite visualize
# this stuff to completely comprehend the logic.
# get_auth_basic_credentials = router.get("/basic-auth/")(get_auth_basic_credentials)
@router.get("/basic-auth/")
def get_auth_basic_credentials(credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> dict:
    # So as I already said, this returns us the credentials which is just a reference to the actual instance of class
    # HTTPBasicCredentials.
    # And then, I am just accessing the attributes defined in the class HTTPBasicCredentials which are based on the
    # __call__(security, request) - __call__ method of the HTTPBasic.
    return {
        "message": "Hi",
        "username": credentials.username,
        "password": credentials.password
    }


# These are the sample fake credentials of the 'existing users' in the db haha.
usernames_to_passwords = {
    "admin": "admin",
    "john": "secret"
}

header_auth_token_to_username = {
    "token1": "admin",
    "token2": "alice"
}


def get_auth_user_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    # to get the user's username we again use security -> HTTPBasic() ,
    # This is just an exception that was made to not repeat the stuff 2 times.
    unauthorized_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    # The main thing is to actually get to password from our fake db -> dict. so there is a method get that actually
    # allows us to receive the value by key of the dict.
    correct_password = usernames_to_passwords.get(credentials.username)
    # This check is important because it lets the program know that the value we check later on via secrets is
    # guaranteed to not be None, otherwise we raise an exception and exit the func.
    if correct_password is None:
        raise unauthorized_exception

    # Here we are comparing the stuff the password we got from the request and the one we store in our db. If
    # everything it is not true we throw an Exception.
    if not secrets.compare_digest(credentials.password.encode("UTF-8"), correct_password.encode("UTF-8")):
        raise unauthorized_exception
    # Just return the username from the request. Since it would mean that all checks were passed successfully.
    return credentials.username


# Implementation with static token fake token1 and token2 in a dict.
# What is going on here is, the function accepts static token required positional argument. The type of this param is str, and it is
# received via the header section in our swagger with the pseudo name 'header-auth-token'. If the token hasn't been got, then throw an
# exception. At the end, return the 'value' which is the username by the key 'static_token'
def get_username_by_auth_static_token(static_token: Annotated[str, Header(alias="header-auth-token")]) -> str:
    if static_token not in header_auth_token_to_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid auth token",
        )
    return header_auth_token_to_username[static_token]


@router.get("/basic-auth-username/")
def demo_auth_basic_username(auth_username: Annotated[str, Depends(get_auth_user_username)]):
    # Here via get_auth_user_username as a Dependency making a reference auth_username to it.
    return {
        "message": "Hi " + auth_username,
        "username": auth_username,
    }

# Here, the username is being passed via get_auth_user_username. 'Depends' calls this function for me and makes sure that it got the
# token from header and as a result returns the username of the user in the fake 'db'.
@router.get("/http-header-auth/")
def demo_auth_some_http_username(username: Annotated[str, Depends(get_username_by_auth_static_token)]):
    return {
        "message": "Hi " + username,
        "username": username
    }


# COOKIE implementation of auth.
COOKIE: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


# This function return part first calls 'uuid4()' from the 'uuid' module. And because 'uuid4' returns an 'instance' of class 'UUID',
# the 'hex' attribute of class 'UUID' can be accessed. By the way 'hex' is a method that returns a string.
# To conclude, 'uuid.uuid4()' -> 'UUID' class object, while adding .hex calls the method that returns now 'str'.
def generate_session_id():
    return uuid.uuid4().hex


# This function receives a required positional argument 'session_id' which is derived from browsers 'Cookie' -> request headers.
# I am not sure with the internals of this cookie yet. But I believe, here alias is being given for the 'COOKIE_SESSION_ID_KEY'
# which is just a pseudo name of it which can be seen in the network -> request headers.
# I was not sure about the difference between 'request' and 'response' headers, so I just googled it. And the difference was request is
# what client asks, while the response is what server gives.
def get_session_data(session_id: Annotated[str, Cookie(alias=COOKIE_SESSION_ID_KEY)]) -> dict:
    # So validation logic of 'session_id' if not inside of fake 'db' , in this case it just a dict and for dict it looks
    # through the keys. If not found among the keys, then throw an exception and exit the function.
    if session_id not in COOKIE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session id or it is missing",
        )
    # Otherwise, just return the user_data from the dict
    return COOKIE[session_id]


# Here, the function accepts two required positional arguments. One is a response, while the other is username which is got as a result
# of the get_auth_username function's execution. Or username can be retrieved via token not just Basic auth as well.
@router.post("/login-cookie/")
def demo_auth_login_set_cookie(
        response: Response,
        username: Annotated[str, Depends(get_auth_user_username)]
        # username: Annotated[str, Depends(get_username_by_auth_static_token)]
) -> dict:
    # Calling the function to generate session_id
    session_id = generate_session_id()
    # Setting the 'session_id' as the key and the value as a dictionary to store the user data.
    COOKIE[session_id] = {
        "username": username,
        "signed_at": int(time())
    }
    # Setting the response headers 'Set Cookie' field to make sure the browser is being instructed
    # that session based approach is being used
    # and the fact that it should put 'Cookie' field in the request headers in the future.
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)

    return {"result": "success"}


# Here, the dictionary under the key 'session_id' is being passed.
# And then with the try except showing the data of the user based on the session_id.
@router.get("/check-cookie/")
def demo_auth_check_cookie(user_session_data: Annotated[dict, Depends(get_session_data)]):
    try:
        username = user_session_data["username"]
        return {
            "message": f"Hi, {username}!",
            **user_session_data
        }
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user data not found"
        )


# This function accepts:
#       'session_id' -> to remove it from the fake 'db',
#       'response' -> to remove the "Set Cookie" field from the response headers
#       'user_session_data' -> to get the username to say bye to the client and to show the details of the last user.
@router.get("/logout-cookie/")
def demo_auth_logout_cookie(
        session_id: Annotated[str, Cookie(alias=COOKIE_SESSION_ID_KEY)],
        response: Response,
        user_session_data: Annotated[dict, Depends(get_session_data)],
) -> dict:
    # pop() -> here, removes the key 'session_id' from the dictionary -> fake 'db'.
    COOKIE.pop(session_id)
    # response.delete_cookie() -> is responsible for removing the 'Set Cookie' field from the response headers.
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]

    return {
        "message": f"Bye, {username}",
        **user_session_data
    }
