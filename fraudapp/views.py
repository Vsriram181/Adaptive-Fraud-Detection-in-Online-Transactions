from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
import joblib
import numpy as np
from django import forms

# Load the model, scaler, and feature names
model = joblib.load('model/fraud_detection_model.pkl')
scaler = joblib.load('model/scaler.pkl')
feature_names = ['type', 'amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 'newbalanceDest']

# Home views
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

# def predict(request):
#     return render(request, 'predict.html')

def result_page(request):
    return render(request, 'result.html')

# Predict fraud
def predict(request):
    if request.method == "POST":
        try:
            data = {
                'type': request.POST.get('type'),
                'amount': float(request.POST.get('amount')),
                'oldbalanceOrg': float(request.POST.get('oldbalanceOrg')),
                'newbalanceOrig': float(request.POST.get('newbalanceOrig')),
                'oldbalanceDest': float(request.POST.get('oldbalanceDest')),
                'newbalanceDest': float(request.POST.get('newbalanceDest'))
            }
            type_encoder = joblib.load('model/type_encoder.pkl')
            data['type'] = type_encoder.transform([data['type']])[0]
            input_data = np.array([data[feature] for feature in feature_names]).reshape(1, -1)
            scaled_data = scaler.transform(input_data)
            prediction = model.predict(scaled_data)
            result = "Fraudulent" if prediction[0] == 1 else "Not Fraudulent"
        except Exception as e:
            result = "An error occurred during prediction."
        return render(request, 'result.html', {'result': result})
    return render(request, 'predict.html')

# Login view
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('/predict')
        return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

# Register view
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('/login')
    return render(request, 'register.html')
