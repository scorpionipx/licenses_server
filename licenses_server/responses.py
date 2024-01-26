from django.shortcuts import render


DEFAULT_FORBIDDEN_TEMPLATE = 'forbidden.html'

FORBIDDEN_TEMPLATE = DEFAULT_FORBIDDEN_TEMPLATE


def forbidden_response(request, context, template='', ):
    """forbidden_response

        Build Forbidden Response.
    :param request: Django request
    :param context: template context
    :type context: dict
    :param template: template to render
    :type template: str
    :return: forbidden response
    :rtype: str
    """
    if not template:
        template = FORBIDDEN_TEMPLATE

    return render(
        request=request,
        template_name=template,
        context=context,
        status=403,  # forbidden
    )
