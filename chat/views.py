import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services import answer


@require_POST
def chat_response(request):
    try:
        payload = json.loads(request.body)
        message = str(payload.get("message", "")).strip()
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"detail": "Solicitud inválida."}, status=400)
    if not message:
        return JsonResponse({"detail": "Escribe una consulta."}, status=400)
    if len(message) > 500:
        return JsonResponse({"detail": "La consulta es demasiado extensa."}, status=400)
    return JsonResponse(answer(message))
