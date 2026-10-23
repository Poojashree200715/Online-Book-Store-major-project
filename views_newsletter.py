from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .models_newsletter import Subscriber


@require_POST
def subscribe(request):
    email = request.POST.get('email', '').strip().lower()
    try:
        validate_email(email)
    except ValidationError:
        messages.error(request, 'Please enter a valid email address.')
    else:
        _, created = Subscriber.objects.get_or_create(email=email)
        if created:
            messages.success(request, 'Thanks for subscribing!')
        else:
            messages.info(request, 'You are already subscribed.')

    next_url = request.META.get('HTTP_REFERER', '/')
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = '/'
    return redirect(next_url)
