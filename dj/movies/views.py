import django.http

# Create your views here.


def movie_list(req: django.http.HttpRequest):
    # Request

    """
    optional page_number: default 0
    optional count: default 5
    """

    # Response

    """
    page_number
    count: default value: 3, or from request
    previous: /movie/?p_no=<page_number-1>&count=<count>
    next: /movie/?p_no=<page_number>&count=<count>
    movies
        get the list of movies by request filter
    """

    d = {"name": "Aditi Rai"}
    return django.http.JsonResponse(d, status=200)


# Movie list should come from Database

# There will be an extra parameter in query `domain` based on filter the movies
# for a user

# Optional Query. Sort: [release-date, rating, updated_on]
