from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout
from django.contrib import messages
# from django.contrib.auth.views import LogoutView

def register(request):
  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username') 
      messages.success(request,f'{username} has been registered. Continue to login')
      return redirect('user-login')
  else:
    form = CreateUserForm()
  context = {
      'form':form,
  }
  return render(request, 'user/register.html',{'form':form})

def profile(request):
  return render(request,'user/profile.html')

def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/profile_update.html', context)

def UserLogoutView(request):
  logout(request)
  return render(request,'user/logout.html',{})

# def register(request):
#   form = UserCreationForm()
#   return render(request, 'user/register.html',{'form':form})

# user/views.py

# class CustomLogoutView(LogoutView):
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)
