from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel
from .populate import initiate

from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    data = {"userName":""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
@csrf_exempt
def registration(request):
    context = {}
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))
    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

def get_cars(request):
    """
    Function to retrieve a list of car models with their respective makes.

    Returns:
    JsonResponse: A JSON response containing a list of dictionaries,
    each dictionary representing a car model with keys 'CarModel' and 'CarMake'.
    """
    # Count the number of car makes
    count = CarMake.objects.filter().count()
    print(count)
    # If no car makes exist, initiate the process
    if(count == 0):
        initiate()
    # Fetch car models with their related car makes
    car_models = CarModel.objects.select_related('car_make')
    # Prepare the list of cars (models with makes)
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})


def get_dealerships(request, state="All"):
    """
    Fetches dealership data based on the provided state, i.e.:
    It will use the get_request implemented in the restapis.py passing the /fetchDealers endpoint.

    If no state is provided, it fetches dealerships for 'All' states.

    Args:
        request: The HTTP request object.
        state (str, optional): The state for which to fetch dealerships. Defaults to "All".

    Returns:
        Response: A JSON response containing the dealership data and a status code.
    """
    # Construct the endpoint URL based on the state
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    # Make the request to fetch dealerships
    dealerships = get_request(endpoint)
    # Return the dealership data as a JSON response
    return JsonResponse({"status":200,"dealers":dealerships})


def get_dealer_reviews(request, dealer_id):
    """
    Fetches and returns details of a specific dealer.

    Args:
        request: HTTP request object.
        dealer_id (int): ID of the dealer.

    Returns:
        JsonResponse: A JSON response containing dealer details.
    """
    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})


def get_dealer_details(request, dealer_id):
    """
    Function to fetch details of a dealer given their ID.

    Parameters:
    request (HttpRequest): The incoming HTTP request.
    dealer_id (int): The unique identifier of the dealer.

    Returns:
    Response: A JSON response containing the dealer details or an error message.
    """
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def add_review(request):
    """
    Endpoint to add a review.

    This function checks if the user is authenticated. If authenticated,
    it extracts the review data from the request body, attempts to post the review,
    and returns a JSON response with the status. If the user is not authenticated,
    it returns an unauthorized status.

    Args:
        request: The HTTP request object.

    Returns:
        Response: A JSON response indicating success or failure.
    """
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})
