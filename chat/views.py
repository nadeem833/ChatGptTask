from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import UserProfile , Conversation
from django.http import JsonResponse
from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
API_KEY = os.getenv('API_KEY')
CHATGPT_API_URL = os.getenv('CHATGPT_API_URL')


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        country = request.POST.get('country')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

        if User.objects.filter(username=user_name).exists():
            return JsonResponse({'error': 'That username is taken'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'That email is being used'}, status=400)

        user = User.objects.create_user(username=user_name, email=email, password=password)
        
        if user:
            UserProfile.objects.create(user=user,)

            return JsonResponse({'message': 'You are now registered and can log in' , 'user_name':user_name}, status=201)
        else:
            return JsonResponse({'error': 'Failed to create user'}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request ,username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            response_data = {
                'message': 'You are now logged in',
                'user_id': user.id,
                'email': user.email,
                'username': user.username,
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


# i am adding dummy data here for chatgpt response to save data in DB
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat(request):
    if request.method == 'POST':
        # Extract the message from the request data
        message = request.data.get('message')  # Use request.data for JSON data      

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }

        data = {
            "model": "gpt-3.5-turbo-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }

        try:
            # Make the request to the ChatGPT API
            # response = requests.post(CHATGPT_API_URL, headers=headers, json=data)
            chat_response = "my name is nadeem ia m working in chatgpt task" 

            if chat_response == "my name is nadeem ia m working in chatgpt task":
            # if response.status_code ==200:

                # chat_response = response.json()['choices'][0]['message']['content']
                
                # Save the conversation in the database
                user = request.user
                conversation = Conversation.objects.create(
                    user=user,
                    # user_message="hello write a letter to hr for raise in annual increment",
                    user_message=message,
                    chatgpt_response=chat_response
                )
                conversation.save()

                return JsonResponse({'response': chat_response}, status=200)
            else:
                return JsonResponse({'error': 'Failed to generate response'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == 'POST':
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                # Simply remove the refresh token from the client-side
                # No need to take server-side action as Django SimpleJWT doesn't maintain a token blacklist
                return JsonResponse({'message': 'You are now logged out'}, status=200)
            else:
                return JsonResponse({'error': 'Refresh token not provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


