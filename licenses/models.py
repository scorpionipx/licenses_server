from django.contrib.auth.models import User as DjangoUser

from django.db import models


class Application(models.Model):
    """
    Application
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
        verbose_name='Name',
        max_length=64,
        default='',
        blank=False,
        null=False,
        unique=True,
        help_text='Application\'s name.',
    )

    description = models.TextField(
        verbose_name='Description',
        max_length=1024,
        default='',
        blank=False,
        null=False,
        unique=False,
        help_text='Application\'s description.',
    )
    # ==================================================================================================================

    # relations
    # ==================================================================================================================
    author = models.ForeignKey(
        verbose_name='Author',
        to=DjangoUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        unique=False,
        related_name='created_applications',
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
        ordering = ('name', )
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'

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


class License(models.Model):
    """
    License
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
    archived = models.BooleanField(
        verbose_name='Archived',
        default=False,
        help_text='Archived.',
    )

    description = models.TextField(
        verbose_name='Description',
        max_length=1024,
        default='',
        blank=False,
        null=False,
        unique=False,
        help_text='License\'s description.',
    )

    expiry_date = models.DateField(
        verbose_name='ExpiryDate',
    )

    serial_no = models.CharField(
        max_length=64,
        verbose_name='SerialNo',
        blank=False,
        null=False,
        unique=True,
        default='',
        help_text='Serial number.',
    )
    # ==================================================================================================================

    # relations
    # ==================================================================================================================
    application = models.ForeignKey(
        to=Application,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        unique=False,
        related_name='licenses',
        verbose_name='Application',
    )

    author = models.ForeignKey(
        verbose_name='Author',
        to=DjangoUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        unique=False,
        related_name='created_licenses',
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
        verbose_name = 'License'
        verbose_name_plural = 'Licenses'

    def __repr__(self):
        """__repr__

            Object's string representation.
        :return: object's string representation
        :rtype: str
        """
        _str = f'{self.application.name}: {self.serial_no}'
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


class Constraint(models.Model):
    """
    Constraint
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
    data = models.TextField(
        verbose_name='Data',
        max_length=2048,
        default='',
        blank=False,
        null=False,
        unique=False,
        help_text='Constraint\'s data.',
    )
    # ==================================================================================================================

    # relations
    # ==================================================================================================================
    author = models.ForeignKey(
        verbose_name='Author',
        to=DjangoUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        unique=False,
        related_name='created_constraints',
    )

    license = models.ForeignKey(
        to=License,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        unique=False,
        related_name='constraints',
        verbose_name='License',
    )
    # ==================================================================================================================


class Event(models.Model):
    """
    Event
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
    type_choices = (
        ('--', 'N/A'),
        ('00', 'Other'),
        ('01', 'Registered'),
        ('02', 'Archived'),
        ('03', 'Changed Expiry Date'),
    )

    type = models.CharField(
        max_length=2,
        verbose_name='Type',
        blank=False,
        null=False,
        unique=False,
        choices=type_choices,
        default='--',
        help_text='Event\'s type',
    )

    note = models.TextField(
        max_length=256,
        verbose_name='Note',
        blank=False,
        null=False,
        unique=False,
        default='',
        help_text='Maximum 256 characters allowed!',
    )
    # ==================================================================================================================

    # relations
    # ==================================================================================================================
    license = models.ForeignKey(
        to=License,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        unique=False,
        related_name='events',
        verbose_name='License',
    )

    author = models.ForeignKey(
        verbose_name='Author',
        to=DjangoUser,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        unique=False,
        related_name='created_license_events',
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
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __repr__(self):
        """__repr__

            Object's string representation.
        :return: object's string representation
        :rtype: str
        """
        _str = f'{self.application.name}: {self.get_type_display()}'
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
