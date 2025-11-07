from django.shortcuts import render
from .forms import UserCreationForm, RegisterForm
from django.shortcuts import redirect
from django.contrib.auth import logout


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})
def logout_view(req):
    logout(req)
    return redirect("login")    
   
        
# Create your views here.
