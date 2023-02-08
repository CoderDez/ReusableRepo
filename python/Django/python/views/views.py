from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..models.models import User



def login_view(req):  
    """view for login page."""
    if req.method == "POST":
        email = req.POST.get("email")
        password = req.POST.get("password")
        user = User.get_user(email, password)
        if user:
            login(req, user)
            return redirect("/reports")
        else:
            return render(
                req, "login.html", {"error_message": "Invalid credentials. Try again."})
    if req.method == "GET":
        if hasattr(req, "user"):
            if isinstance(req.user, User):
                logout(req) 
        return render(req, "login.html")