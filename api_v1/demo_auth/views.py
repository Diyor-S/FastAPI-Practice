import secrets  # imported secrets to actually get to compare at constant time two values

from fastapi import APIRouter, Depends, HTTPException, status  # APIRouter for routes , Depends for dependency injection
# system  HTTPException for throwing exceptions , and status to showing status code when those exceptions occur.
from fastapi.security import HTTPBasic, HTTPBasicCredentials  # Http Basic for basic username, password authentication
# HTTPBasicCredentials is what actually stores username and password stuff.
from typing import Annotated  # Annotated for type hints.

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


@router.get("/basic-auth-username/")
def demo_auth_basic_username(auth_username: Annotated[str, Depends(get_auth_user_username)]):
    # Here via get_auth_user_username as a Dependency making a reference auth_username to it.
    return {
        "message": "Hi",
        "username": auth_username,
    }
