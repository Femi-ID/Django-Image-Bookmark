from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# from common.decorators import ajax_required
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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


# @ajax_required
@login_required
@require_POST  # Ensures only POST requests for this route
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            # If the action is to 'like' the image
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'error'})
# AJAX actions:consists of sending and retrieving data from the server asynchronously, without reloading the whole page.
# JsonResponse, returns an HTTP response as application/json content type, converts the given object into a JSON output.


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range, return an empty page
            return HttpResponse('')
        # If page is out of range, deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html', {'section': 'images', 'images': images})
        # This template will only contain the images of the requested page
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})
    # This template will extend the base.html template to display the whole page
    # and will include the list_ajax.html template to include the list of images.
