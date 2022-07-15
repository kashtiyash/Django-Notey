from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from users.forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method =="POST":
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Your account has been created successfully! You are able to log in ")
            return redirect('login')
        
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == "POST":
        update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
                            request.POST,
                            request.FILES,
                            instance=request.user.profile)
        if update_form.is_valid() and profile_form.is_valid():
            update_form.save()
            profile_form.save()

            messages.success(request, f"Your account has been updated!")
            return redirect('profile')

    else:
        update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'update_form': update_form,
        'profile_form': profile_form,

    }

    return render(request, 'users/profile.html', context)



