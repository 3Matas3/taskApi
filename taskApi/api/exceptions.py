from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Custom exception handler to make parsable error message with all information
    :param exc:
    :param context:
    :return:
    """
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {"success": False, "error": response.data}

    return response
