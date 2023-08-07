from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
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
            return redirect(new_item.get_absolute_url)
            # TODO: Implement the canonical URL for the image object instance

    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.POST)

    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


"""You expect initial data via GET in order to create an instance of the form. 
This data will consist of the url and title attributes of an image from an external
website and will be provided via GET by the JavaScript tool that you will create later."""

