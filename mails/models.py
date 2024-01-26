import pathlib


from django.conf import settings

from django.contrib.auth.models import User as DjangoUser

from django.core.validators import (
    RegexValidator,
    EmailValidator,
)

from django.db import models

from django.urls import reverse

from django.utils.text import slugify


from os.path import (
    join as join_paths,
)

BASE_MODEL_FILES_UPLOAD_DIR = join_paths(settings.MEDIA_ROOT, 'mails')


# URL_BASE = settings.URL_BASE


def mail_files_upload_path(instance, file_name):
    """mail_files_upload_path

    """
    path = join_paths(BASE_MODEL_FILES_UPLOAD_DIR, slugify(instance.app), slugify(instance.category),
                      f'{instance.pk}', file_name)
    return path


class Mail(models.Model):
    """Mail

    """
    # model manager type hint
    # ==================================================================================================================
    objects: models.Manager
    # ==================================================================================================================

    # administration related
    # ==================================================================================================================
    created = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    # ==================================================================================================================

    # instance specific
    # ==================================================================================================================
    app = models.CharField(
        max_length=64,
        verbose_name='App',
        blank=False,
        null=False,
        unique=False,
        default='',
        help_text='App that requires this mail.',
    )

    category = models.CharField(
        max_length=64,
        verbose_name='Category',
        blank=True,
        null=False,
        unique=False,
        default='',
        help_text='Sub app category.',
    )

    content_file = models.FileField(
        max_length=255,
        verbose_name='content',
        upload_to=mail_files_upload_path,
        blank=True,
        null=False,
        help_text='Mail content raw.',
    )

    receivers_file = models.FileField(
        max_length=255,
        verbose_name='receivers',
        upload_to=mail_files_upload_path,
        blank=True,
        null=False,
        help_text='Mail receivers, JSON format, divided by received type (to, cc, bcc).',
    )

    sender = models.CharField(
        max_length=256,
        verbose_name='Sender',
        blank=False,
        null=False,
        unique=False,
        default='',
        help_text='Mail sender (e.g.: hilsmonitor@noreply.com).',
    )

    sent = models.BooleanField(
        default=False,
        verbose_name='Sent',
        help_text='Specifies if the mail was sent to the receivers',
    )

    title = models.CharField(
        max_length=256,
        verbose_name='Title',
        blank=False,
        null=False,
        unique=False,
        default='',
    )

    # ==================================================================================================================

    # relations
    # ==================================================================================================================

    # ==================================================================================================================

    @property
    def meta(self):
        """meta

            Provide access to object's protected member meta.
        :return: meta data object
        """
        return self._meta

    class Meta:
        """Meta

            Provide metadata to the framework.
        """
        ordering = ('-created', )
        verbose_name = 'Mail'
        verbose_name_plural = 'Mails'

    def __repr__(self):
        """__repr__

            Object's string representation.
        :return: object's string representation
        :rtype: str
        """
        _str = f'{self.title}'
        return _str

    def __str__(self):
        """__str__

            Object's string representation.
        :return: object's string representation
        :rtype: str
        """
        return self.__repr__()

    def __unicode__(self):
        """__unicode__

            Object's string representation.
        :return: object's string representation
        :rtype: str
        """
        return self.__str__()

    @property
    def receivers(self):
        """receivers

            Get the list of all receivers.
        :return: list of all receivers
        :rtype: list of str
        """
        receivers = []
        return receivers


class MailAddress(models.Model):
    """MailAddress

    """
    # model manager type hint
    # ==================================================================================================================
    objects: models.Manager
    # ==================================================================================================================

    # administration related
    # ==================================================================================================================
    created = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    # ==================================================================================================================

    # instance specific
    # ==================================================================================================================
    address = models.CharField(
        max_length=64,
        verbose_name='Address',
        blank=False,
        null=False,
        unique=True,
        default='',
        validators=[
            EmailValidator,
        ],
        help_text='Email address.'
    )

    description = models.CharField(
        max_length=128,
        verbose_name='Description',
        blank=False,
        null=False,
        unique=False,
        default='',
        help_text='Mail address brief description and purpose (e.g.: person name, group name etc.).',
    )
    # ==================================================================================================================

    # relations
    # ==================================================================================================================
    author = models.ForeignKey(
        to=DjangoUser,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        unique=False,
        related_name='created_mail_addresses',
        verbose_name='Author',
    )

    mail_group = models.ForeignKey(
        to='MailGroup',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        unique=False,
        related_name='mail_addresses',
        verbose_name='Mail group',
    )
    # ==================================================================================================================

    @property
    def meta(self):
        """meta

            Provide access to object's protected member meta.
        :return: meta data object
        """
        return self._meta

    class Meta:
        """Meta

            Provide metadata to the framework.
        """
        ordering = ('-created', )
        verbose_name = 'Mail address'
        verbose_name_plural = 'Mail addresses'

    def __repr__(self):
        """__repr__

            Object's string representation.
        :return: object's string representation
        :rtype: str
        """
        _str = f'{self.address}'
        return _str

    def __str__(self):
        """__str__

            Object's string representation.
        :return: object's string representation
        :rtype: str
        """
        return self.__repr__()

    def __unicode__(self):
        """__unicode__

            Object's string representation.
        :return: object's string representation
        :rtype: str
        """
        return self.__str__()


class MailGroup(models.Model):
    """MailGroup

    """
    # model manager type hint
    # ==================================================================================================================
    objects: models.Manager
    # ==================================================================================================================

    # administration related
    # ==================================================================================================================
    created = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    # ==================================================================================================================

    # instance specific
    # ==================================================================================================================
    name = models.CharField(
        max_length=64,
        verbose_name='Name',
        blank=False,
        null=False,
        unique=True,
        default='',
        validators=[
            RegexValidator(
                regex='^[0-9A-Z_]*$',
                message='Only uppercase letters, digits, blank and underscores allowed!'
            )
        ],
        help_text='Group\'s name. Only uppercase letters, digits and underscores allowed!'
    )

    description = models.TextField(
        max_length=512,
        verbose_name='Description',
        blank=False,
        null=False,
        unique=False,
        default='',
        help_text='Group brief description and purpose.',
    )
    # ==================================================================================================================

    # relations
    # ==================================================================================================================
    author = models.ForeignKey(
        to=DjangoUser,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        unique=False,
        related_name='created_mail_groups',
        verbose_name='Author',
    )

    mails = models.ManyToManyField(
        to='Mail',
        blank=True,
        verbose_name='Mails',
        related_name='mail_groups',
    )

    users = models.ManyToManyField(
        to=DjangoUser,
        blank=True,
        unique=False,
        related_name='mail_groups',
        verbose_name='Users',
    )
    # ==================================================================================================================

    @property
    def meta(self):
        """meta

            Provide access to object's protected member meta.
        :return: meta data object
        """
        return self._meta

    class Meta:
        """Meta

            Provide metadata to the framework.
        """
        ordering = ('-created', )
        verbose_name = 'Mail group'
        verbose_name_plural = 'Mail groups'

    def __repr__(self):
        """__repr__

            Object's string representation.
        :return: object's string representation
        :rtype: str
        """
        _str = f'{self.name}'
        return _str

    def __str__(self):
        """__str__

            Object's string representation.
        :return: object's string representation
        :rtype: str
        """
        return self.__repr__()

    def __unicode__(self):
        """__unicode__

            Object's string representation.
        :return: object's string representation
        :rtype: str
        """
        return self.__str__()

    @property
    def receivers(self):
        """receivers

            Get all receivers related to this Mail Group.
        :return: all receivers related to this Mail Group
        :rtype: list of str
        """
        receivers = [user.email for user in self.users.all()]
        receivers.extend([mail_address.address for mail_address in self.mail_addresses.all()])
        return receivers

    @property
    def receivers_plain_url(self):
        """receivers_plain_url

            Get URL for receivers view.
        :return: URL for plain receivers view
        :rtype: str
        """
        view_name = 'mails:mail_group_plain_receivers'
        url_tail = reverse(view_name, kwargs={'pk': self.pk})
        url = f'{url_tail}'
        return url
