import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    """
    This function constructs a GET request to a specified backend URL with optional parameters (i.e.:
    This function calls GET method in requests library with a URL and any URL parameters such as dealerId.)

    Parameters:
    endpoint (str): The endpoint path to append to the backend URL.
    **kwargs: Optional keyword arguments representing query parameters. 
    
    **kwargs works just like *args, 
    but instead of accepting positional arguments it accepts keyword (or named) arguments, e.g.:

    def concatenate(**kwargs):
        result = ""
        # Iterating over the Python kwargs dictionary
        for arg in kwargs.values():
            result += arg
        return result

    print(concatenate(a="Real", b="Python", c="Is", d="Great", e="!"))


    Returns:
    dict: The JSON response from the server.

    Raises:
    Exception: If a network error occurs during the request.
    """
    params = ""
    # Construct query string from kwargs
    if(kwargs):
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url)) # Use flush=True for immediate output in non-interactive mode
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except:
        # If any error occurs
        print("Network exception occurred")

# def analyze_review_sentiments(text):
# request_url = sentiment_analyzer_url+"analyze/"+text
# Add code for retrieving sentiments

# def post_review(data_dict):
# Add code for posting review
