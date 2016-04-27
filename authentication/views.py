try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    login as django_login_view, password_change)
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm

from . import forms
from .models import EmailConfirmationRequest
from . import utils

now = timezone.now


def login(request):
    local_host = utils.get_local_host(request)
    return django_login_view(request)


def logout(request):
    auth_logout(request)
    messages.success(request, _('You have been successfully logged out.'))
    return redirect(settings.LOGIN_URL)


def request_reset_password(request):
    local_host = utils.get_local_host(request)
    form = forms.RequestResetPasswordForm(local_host=local_host,
                                              data=request.POST or None)
    if form.is_valid():
        form.send()
        msg = _('A link to reset your passsword has been sent to your email. '
                'Please check your inbox.')
        messages.success(request, msg)
        return redirect(settings.LOGIN_REDIRECT_URL)

    return TemplateResponse(request,
                            'registration/request_password.html',
                            {'form': form})


def reset_password(request, token):
    try:
        email_confirmation_request = EmailConfirmationRequest.objects.get(
            token=token, valid_until__gte=now())
            # TODO: cronjob (celery task) to delete stale tokens
    except EmailConfirmationRequest.DoesNotExist:
        return TemplateResponse(request, 'registration/invalid_token.html')
    user = email_confirmation_request.get_authenticated_user()
    form = forms.SetOrRemovePasswordForm(user=user,
                                         data=request.POST or None)
    if form.is_valid():
        form.save()
        email_confirmation_request.delete()
        messages.success(request, _('Password has been successfully changed. '
                                    'Please login with your new password.'))
        return redirect(settings.LOGIN_REDIRECT_URL)

    return TemplateResponse(
        request, 'registration/set_password.html', {'form': form})


def change_password(request):
    return password_change(
        request, template_name='registration/change_password.html',
        post_change_redirect=reverse('profile:details'))
