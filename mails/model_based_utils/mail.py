import pathlib


from django.conf import settings

from django.core.files.base import ContentFile

from django.template.loader import render_to_string

from django.utils.safestring import mark_safe


from email.mime.text import MIMEText


from os.path import (
    join as join_paths,
)


from smtplib import SMTP


from mails.models import (
    Mail,
    MailGroup,
)


BASE_MODEL_FILES_UPLOAD_DIR = join_paths(settings.MEDIA_ROOT, 'mails')


SMTP_SERVER = settings.IPX_SETTINGS['SMTP']['O365']['SERVER']
SMTP_PORT = settings.IPX_SETTINGS['SMTP']['O365']['PORT']
SMTP_AUTH = (settings.IPX_SETTINGS['SMTP']['O365']['USER'], settings.IPX_SETTINGS['SMTP']['O365']['PASSWORD'])
SMTP_SENDER = settings.IPX_SETTINGS['SMTP']['O365']['SENDER']
SMTP_TLS = settings.IPX_SETTINGS['SMTP']['O365']['TLS']


DEVELOPMENT_RECEIVERS = [
    'danut.popa@continental-corporation.com',
    # 'ioana.pasc@continental-corporation.com',
    # 'gheorghe.chirica@continental-corporation.com',
    # 'radu-eugen.vasile@continental-corporation.com',
    # 'ovidiu-viorel.onisoru@continental-corporation.com',
    # 'oana-elena.cimpoi@continental-corporation.com',
]


MAIL_TEMPLATES_ROOT_DIRECTORY = settings.BASE_DIR.joinpath('mails').joinpath('templates').joinpath('mails')


TEMPLATES_DIR = join_paths(
    settings.BASE_DIR,
    'mails',
    'templates',
    'mails',
)

DEVELOPMENT_TEMPLATES_DIR = join_paths(
    TEMPLATES_DIR,
    'development',
)


def send_mail(app, category, subject, content, receivers, from_header='default', cc=None, bcc=None, mail_groups=None):
    """send_mail

        Send mail via SMTP.
    :param app: related Django Application name - used for mail related data storage
    :type app: str
    :param category: related Django Application Category (sub app) - used for mail related data storage
    :type category: str
    :param subject: mail's subject (title)
    :type subject: str
    :param content: mail's content as plain text or HTML
    :type content: str
    :param receivers: list of receives (<To> field)
    :type receivers: list of str
    :param from_header: mail's header, must be left as default if mail must be sent to Teams Channels (bug on their
    filters)
    :param cc: mail's carbon copy receivers (<Cc> field)
    :type cc: list of str or None
    :param bcc: mail's blind carbon copy receivers (<Bcc> field)
    :type bcc: list of str or None
    :param mail_groups: list of related mail groups
    :type mail_groups: list of MailGroup or None
    """
    try:
        # establish connection to SMTP server
        # ==============================================================================================================
        smtp_server = SMTP(SMTP_SERVER, SMTP_PORT)
        smtp_server.ehlo()
        # ==============================================================================================================

        # enable TLS encryption
        # ==============================================================================================================
        if SMTP_TLS:
            smtp_server.starttls()
        # ==============================================================================================================

        # authenticate
        # ==============================================================================================================
        smtp_server.login(*SMTP_AUTH)
        # ==============================================================================================================

        if mail_groups:
            mail_groups_receivers = []
            for mail_group in mail_groups:
                for user in mail_group.users.all():
                    mail_groups_receivers.append(user.email)
                for address in mail_group.mail_addresses.all():
                    mail_groups_receivers.append(address.address)

            receivers.extend(mail_groups_receivers)
            receivers = list(set(receivers))  # remove duplicates

        # build message
        # ==============================================================================================================
        message = MIMEText(content, 'html')
        message['Subject'] = subject
        if from_header == 'default':
            message['From'] = f'Licenses Server <{SMTP_SENDER}>'
        else:
            message['From'] = from_header
        message['To'] = ', '.join(receivers)

        if cc:
            message['Cc'] = ', '.join(cc)
            receivers.extend(cc)

        if bcc:
            message['Bcc'] = ', '.join(bcc)
            receivers.extend(bcc)
        # ==============================================================================================================

        # send message
        # ==============================================================================================================
        smtp_server.sendmail(SMTP_SENDER, receivers, message.as_string())
        smtp_server.quit()
        sent = True
        # ==============================================================================================================
    except Exception as exception:
        error = f'Failed to send mail! {exception}'
        mail_send_error_handler(error)
        sent = False

    try:
        mail_entry = Mail(
            app=app,
            category=category,
            sender=SMTP_SENDER,
            sent=sent,
            title=subject,
        )

        mail_entry.save()
    except Exception as exception:
        error = f'Failed to save Mail entry! {exception}'
        mail_send_error_handler(error)
        return False

    mail_entry.receivers_file.save('receivers.ipx', ContentFile(', '.join(receivers)))
    mail_entry.content_file.save('content.ipx', ContentFile(content))

    if mail_groups:
        for mail_group in mail_groups:
            mail_entry.mail_groups.add(mail_group)

    return mail_entry


def mail_send_error_handler(error, ret=False):
    """mail_send_error_handler

        Handle mail sending errors.
    :param error: error that occurred
    :type error: str
    :param ret: value to be returned by handler
    :type ret: any
    :rtype: any
    """
    print(error)  # all prints will be reflected on Apache server's error log
    return ret


def render_template(template, context=None, mark_context_safe=False):
    """render_template

    """
    if mark_context_safe:
        if context:
            for key, value in context.items():
                context[key] = mark_safe(value)

    if context:
        context['hils_monitor_version'] = settings.VERSION

    return render_to_string(template, context=context)
