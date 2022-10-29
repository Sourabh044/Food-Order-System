from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserRegisterForm
# Create your views here.
def Register_User(request):
    if request.method=='POST':
        print(request.POST)
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(f'User saved')
        else:
            return HttpResponse(form.errors.as_data())
    else:
        form = UserRegisterForm()
        return render(request,'accounts/register-user.html', {'form':form})
