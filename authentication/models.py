from __future__ import unicode_literals
from datetime import timedelta
from uuid import uuid4

from django.db import models
from django.contrib.auth import authenticate, get_user_model
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone

now = timezone.now

def default_valid_date():
        return now() + timedelta(settings.ACCOUNT_ACTIVATION_DAYS)


TOKEN_PATTERN = ('(?P<token>[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}'
                 '-[0-9a-z]{12})')


class UniqueTokenManager(models.Manager):  # this might end up in `utils`

    def __init__(self, token_field):
        self.token_field = token_field
        super(UniqueTokenManager, self).__init__()

    def create(self, **kwargs):
        assert self.token_field not in kwargs, 'Token field already filled.'
        kwargs[self.token_field] = str(uuid4())
        return super(UniqueTokenManager, self).create(**kwargs)


class AbstractToken(models.Model):

    token = models.CharField(max_length=36, unique=True)
    valid_until = models.DateTimeField(default=default_valid_date)

    objects = UniqueTokenManager(token_field='token')

    class Meta:
        abstract = True


class EmailConfirmationRequest(AbstractToken):

    email = models.EmailField()

    def get_authenticated_user(self):
        user, _created = get_user_model().objects.get_or_create(email=self.email)
        return authenticate(user=user)

    def get_reset_password_url(self):
        return reverse('registration:reset_password', kwargs={'token': self.token})
