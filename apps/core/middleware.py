UTM_KEYS = ("utm_source", "utm_medium", "utm_campaign")


class UTMMiddleware:
    """Remember ad campaign tags so a lead is attributed to the right campaign
    even when the visitor browses several pages before submitting a form."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        utm = {k: request.GET[k][:100] for k in UTM_KEYS if k in request.GET}
        if utm:
            request.session["utm"] = utm
        return self.get_response(request)
