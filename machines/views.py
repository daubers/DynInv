from django.http import HttpResponse

# Create your views here.


def health_check(request):
    html = "<html><body>Ok</body></html>"
    return HttpResponse(html)
