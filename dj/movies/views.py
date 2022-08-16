import django.http

# Create your views here.


def movie_list(req: django.http.HttpRequest):
    d = {"name": "Aditi Rai"}
    return django.http.JsonResponse(d, status=200)
