from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegistrationForm , UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from . models import profile
from django.contrib.auth.models import User

# Create your views here.


def register(request):
    if request.method == 'POST': ##This line of code checks if the requests method is post
        form = UserRegistrationForm(request.POST) #this line assigns the UserRegistrationForm to a variabe 'form'
        if form.is_valid(): #this ine checks if the form data is valid
            form.save() #this line saves the form dtat to the data base
            username = form.cleaned_data.get('username')
            #messages.success(request, f'Account created for {username}')
            return redirect('login') #this line redirects the user to the login page

    else:
        form = UserRegistrationForm() #it returns an empty form
    return render(request,'users/register.html',{'form':form}) #returns back the registration page
    #this else statement will be carried out only
    # if; |the method is not post,|the form is data is not valid



@login_required #this line redirects the user to the login page when offline but wants to view d profile
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }


    return render(request, 'users/profile.html', context)





def point(request):
    model = profile
    if request.method == 'POST':
        user_profile = get_object_or_404(profile, id=request.user.id)
        user_profile +=2
        user_profile.save()

        return redirect('home')