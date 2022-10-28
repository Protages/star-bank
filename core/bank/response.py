from rest_framework.views import Response as RESTResponse
# from core.settings import ACCESS_CONTROL_ALLOW_ORIGIN


class Response(RESTResponse):
    """Custom Response with header
    Access-Control-Allow-Origin = settings.ACCESS_CONTROL_ALLOW_ORIGIN"""

    def __init__(self, data=None, status=None,
                 template_name=None, headers={},
                 exception=False, content_type=None):
        # headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        # headers['Access-Control-Allow-Credentials'] = 'true'
        # headers['Access-Control-Allow-Headers'] = 'content-type'
        super().__init__(data, status, template_name, headers, exception, content_type)
