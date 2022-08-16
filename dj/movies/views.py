import django.http

# Create your views here.


def movie_list(req: django.http.HttpRequest):
    d = {"name": "Aditi Rai"}
    return django.http.JsonResponse(d, status=200)


# Movie list should come from Database

# There will be an extra parameter in query `domain` based on filter the movies
# for a user

# Optional Query. Sort: [release-date, rating, updated_on]
