from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from bookmarks.common.decorators import ajax_required
from .models import Contact
from bookmarks.actions.utils import create_action
from bookmarks.actions.models import Action
# Create your views here.


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            # authenticate() checks user credentials and returns a User object if they are correct.
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # login() sets the user in the current session.
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')

    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.value_list('id', flat=True)
    # To get the list of users the current user is following

    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    return render(request, 'account/dashboard.html', {'section': 'dashboard',
                                                      'actions': actions})


'''Django offers a QuerySet method called select_related() that allows you to retrieve related objects for one-to-many relationships. 
The select_related method is for ForeignKey and OneToOne fields. It works by performing a SQL JOIN and including the fields of the related
object in the SELECT statement.

Django offers a different QuerySet method called prefetch_related that works for many-to-many and many-to-one relationships in addition to the relationships supported by select_related(). The prefetch_related() method performs
a separate lookup for each relationship and joins the results using Python. It also supports the prefetching of GenericRelation and GenericForeignKey'''


def register(request):
    # user_form = UserRegistrationForm()

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but don't save yet
            new_user = user_form.save(commit=False)

            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # the set_password() method of the user model handles hashing
            new_user.save()

            # Create the user profile
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account!')
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit_form(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'An error occurred when updating your profile')
            # You can learn more about the messages framework at:
            # https://docs.djangoproject.com/en/3.0/ref/contrib/messages/.
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'account/edit_form.html', {'user_form': user_form,
                                                      'profile_form': profile_form})


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    # Django User model contains an is_active flag to designate whether the user account is considered active
    return render(request, 'account/user/list.html', {'section': 'people',
                                                      'users': users})
# TODO: improve it by adding pagination in the same way as you did for the image_list view.


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username, is_active=True)
    return render(request, 'account/user/detail.html', {'section': 'people',
                                                        'user': user})


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})

        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
# This view is quite similar to the image_like view
