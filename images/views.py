from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# Create your views here.


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)

        if form.is_valid():
            # Here the form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the new image  created
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully!')

            # redirect to the newly created image
            return redirect(new_item.get_absolute_url())
            # TODO: Implement the canonical URL for the image object instance
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


"""You expect initial data via GET in order to create an instance of the form. 
This data will consist of the url and title attributes of an image from an external
website and will be provided via GET by the JavaScript tool that you will create later."""


def image_detail(request, id, slug):
    #  A simple view to display an image
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'section': 'images',
                                                        'image': image})


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            # If the action was to like the image
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})
# AJAX actions:consists of sending and retrieving data from the server asynchronously, without reloading the whole page.
