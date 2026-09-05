from django.core.mail import BadHeaderError, send_mail
from django.http import HttpRequest, JsonResponse


def email_server_status(request: HttpRequest) -> JsonResponse:
    try:
        send_mail(
            "Email Server Status Check",
            "This is a test email from the Swing | Status app.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )
        return JsonResponse({"status": "OK", "message": "Email server is operational"})
    except BadHeaderError:
        return JsonResponse(
            {"status": "ERROR", "message": "Invalid header found in email"}
        )
    except Exception as e:
        return JsonResponse(
            {"status": "ERROR", "message": f"Email server error: {str(e)}"}
        )
