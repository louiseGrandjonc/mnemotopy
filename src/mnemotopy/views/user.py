from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


@require_POST
@csrf_exempt
def change_language(request, status=None):

    parameters = request.POST

    response = HttpResponseRedirect(parameters.get('redirect_url'))

    lang = parameters.get('language',
                          settings.LANGUAGE_CODE)

    if lang in dict(settings.LANGUAGES):
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME,
                            lang)

    return response
