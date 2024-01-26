from django.urls import path

from mails.model_based_views import (
    mail_group as mail_group_views,
)


plain_receivers_path = path(
    r'mail_group_plain_receivers/<int:pk>/',
    mail_group_views.PlainReceiversView.as_view(),
    name='mail_group_plain_receivers',
)


URL_PATTERNS = [
    plain_receivers_path,
]
