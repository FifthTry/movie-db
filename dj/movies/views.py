import django.http

# Create your views here.


def movie_list(req: django.http.HttpRequest):
    record_response = {"page-number":1,"next":"next", "previous":"previous", "count":5,"list movies":"bj"}

    record_movie = {"id": 1, "title": "Laal Singh Chaddha","release-date": "11 August 2022", "poster": "Laal Singh Chaddha Movies",
         "director": "Advait Chandan", "description": "LAAL SINGH CHADDHA, a simple man whose extraordinary journey will fill you with love, warmth & happiness.", "rating" : 6, "review-count": 2, "list reviews": "bj"  }


    record_review = {"id": 1, "title": "Laal Singh Chaddha", "description": "Very cheap version of the Original movie. Very slow screenplay.Unnecessary things are forced to the movie. Lack of logic, lack of emotions.","reviewer": "imDb", "rating": 5}

    return django.http.JsonResponse([record_response,record_movie,record_review], status=200)

# Movie list should come from Database

# There will be an extra parameter in query `domain` based on filter the movies
# for a user

# Optional Query. Sort: [release-date, rating, updated_on]
