from flask import Flask, request
from flask_cors import CORS, cross_origin
import requests, json

app = Flask(__name__)
cors = CORS(app)

API_KEY = "59e1a8bdd05f5059f7a2fe4b65ed990c"

DOMAIN = "https://api.themoviedb.org"

@app.route("/")
def test():
    return "hello world!"

@app.route("/home", methods=['GET'])
def get_slideshow_data():
    trending_url = DOMAIN + ("/3/trending/movie/week?api_key=%s" % API_KEY)
    airingtv_url = DOMAIN + ("/3/tv/airing_today?api_key=%s" % API_KEY)
    trending_res = json.loads(requests.get(trending_url).text)
    airingtv_res = json.loads(requests.get(airingtv_url).text)
    trending_top5 = trending_res["results"][:5]
    airingtv_top5 = airingtv_res["results"][:5]
    trending_list = []
    for each in trending_top5:
        movie = dict()
        movie["title"] = each["title"]
        movie["backdrop_path"] = "https://image.tmdb.org/t/p/w780/" + each["backdrop_path"]
        movie["release_date"] = each["release_date"]
        trending_list.append(movie)
    airingtv_list = []
    for each in airingtv_top5:
        tv = dict()
        tv["name"] = each["name"]
        tv["backdrop_path"] = "https://image.tmdb.org/t/p/w780/" + each["backdrop_path"]
        tv["first_air_date"] = each["first_air_date"]
        airingtv_list.append(tv)
    return json.dumps([trending_list, airingtv_list])

@app.route("/search/movie", methods=['GET'])
def search_movie():
    query = request.args.get('query')
    url = DOMAIN + ("/3/search/movie?api_key=%s" % API_KEY) + ("&query=%s" % query) + \
        "&language=en-US&page=1&include_adult=false"
    res = json.loads(requests.get(url).text)
    l = []
    for each in res["results"]:
        movie = dict()
        movie["id"] = each.get("id")
        movie["title"] = each.get("title")
        movie["overview"] = each.get("overview")
        movie["poster_path"] = ("https://image.tmdb.org/t/p/w185" + each.get("poster_path")) \
                                if each.get("poster_path") != None else None
        movie["release_date"] = each.get("release_date")
        movie["vote_average"] = each.get("vote_average")
        movie["vote_count"] = each.get("vote_count")
        movie["genre_ids"] = each.get("genre_ids")
        movie["media_type"] = "movie"
        l.append(movie)
    return json.dumps(l)

@app.route("/search/tv", methods=['GET'])
def search_tv():
    query = request.args.get('query')
    url = DOMAIN + ("/3/search/tv?api_key=%s" % API_KEY) + ("&query=%s" % query) + \
        "&language=en-US&page=1&include_adult=false"
    res = json.loads(requests.get(url).text)
    l = []
    for each in res["results"]:
        tv = dict()
        tv["id"] = each.get("id")
        tv["name"] = each.get("name")
        tv["overview"] = each.get("overview")
        tv["poster_path"] = ("https://image.tmdb.org/t/p/w185" + each.get("poster_path")) \
                                if each.get("poster_path") != None else None
        tv["first_air_date"] = each.get("first_air_date")
        tv["vote_average"] = each.get("vote_average")
        tv["vote_count"] = each.get("vote_count")
        tv["genre_ids"] = each.get("genre_ids")
        tv["media_type"] = "tv"
        l.append(tv)
    return json.dumps(l)

@app.route("/search/multi", methods=['GET'])
def search_multi():
    query = request.args.get('query')
    url = DOMAIN + ("/3/search/multi?api_key=%s" % API_KEY) + ("&query=%s" % query) + \
        "&language=en-US&page=1&include_adult=false"
    res = json.loads(requests.get(url).text)
    l = []
    for each in res["results"]:
        if each["media_type"] != "movie" and each["media_type"] != "tv": continue
        d = dict()
        d["media_type"] = each["media_type"]
        d["id"] = each.get("id")
        if d["media_type"] == "movie":
            d["title"] = each.get("title")
            d["release_date"] = each.get("release_date")
        else: 
            d["name"] = each.get("name")
            d["first_air_date"] = each.get("first_air_date")
        d["overview"] = each.get("overview")
        d["poster_path"] = ("https://image.tmdb.org/t/p/w185" + each.get("poster_path")) \
                                if each.get("poster_path") != None else None
        d["vote_average"] = each.get("vote_average")
        d["vote_count"] = each.get("vote_count")
        d["genre_ids"] = each.get("genre_ids")
        l.append(d)
    return json.dumps(l)

@app.route("/movie/<movie_id>", methods=['GET'])
def get_movie_detail(movie_id):
    url = DOMAIN + ("/3/movie/%s?api_key=%s&language=en-US" % (movie_id, API_KEY))
    res = json.loads(requests.get(url).text)
    movie = dict()
    movie["id"] = res.get("id")
    movie["title"] = res.get("title")
    movie["runtime"] = res.get("runtime")
    movie["release_date"] = res.get("release_date")
    movie["spoken_languages"] = res.get("spoken_languages")
    movie["vote_average"] = res.get("vote_average")
    movie["vote_count"] = res.get("vote_count")
    movie["poster_path"] = ("https://image.tmdb.org/t/p/w185" + res.get("poster_path")) \
                            if res.get("poster_path") != None else None
    movie["backdrop_path"] = ("https://image.tmdb.org/t/p/w780" + res.get("backdrop_path")) \
                            if res.get("backdrop_path") != None else None
    movie["genres"] = res.get("genres")
    movie["overview"] = res.get("overview")
    movie["url"] = "https://www.themoviedb.org/movie/%s" % movie_id

    cast_url = DOMAIN + ("/3/movie/%s/credits?api_key=%s&language=en-US" % (movie_id, API_KEY))
    cast_res = json.loads(requests.get(cast_url).text)
    cast_res = cast_res["cast"][:8] if len(cast_res["cast"]) > 8 else cast_res["cast"]
    cast_list = []
    for each in cast_res:
        cast = dict()
        cast["name"] = each.get("name")
        cast["profile_path"] = ("https://image.tmdb.org/t/p/w185" + each.get("profile_path")) \
                            if each.get("profile_path") != None else None
        cast["character"] = each.get("character")
        cast_list.append(cast)
    movie["casts"] = cast_list

    review_url = DOMAIN + ("/3/movie/%s/reviews?api_key=%s&language=en-US&page=1" % (movie_id, API_KEY))
    review_res = json.loads(requests.get(review_url).text)
    review_res = review_res["results"][:5] if len(review_res["results"]) > 5 else review_res["results"]
    review_list = []
    for each in review_res:
        review = dict()
        review["username"] = each["author_details"].get("username")
        review["content"] = each.get("content")
        review["rating"] = each["author_details"].get("rating")
        review["created_at"] = each.get("created_at")
        review_list.append(review)
    movie["reviews"] = review_list

    return json.dumps(movie)

@app.route("/tv/<tv_show_id>", methods=['GET'])
def get_tv_detail(tv_show_id):
    url = DOMAIN + ("/3/tv/%s?api_key=%s&language=en-US" % (tv_show_id, API_KEY))
    res = json.loads(requests.get(url).text)
    tv = dict()
    tv["id"] = res.get("id")
    tv["name"] = res.get("name")
    tv["episode_run_time"] = res.get("episode_run_time")
    tv["first_air_date"] = res.get("first_air_date")
    tv["spoken_languages"] = res.get("spoken_languages")
    tv["vote_average"] = res.get("vote_average")
    tv["vote_count"] = res.get("vote_count")
    tv["poster_path"] = ("https://image.tmdb.org/t/p/w185" + res.get("poster_path")) \
                            if res.get("poster_path") != None else None
    tv["backdrop_path"] = ("https://image.tmdb.org/t/p/w780" + res.get("backdrop_path")) \
                            if res.get("backdrop_path") != None else None
    tv["genres"] = res.get("genres")
    tv["number_of_seasons"] = res.get("number_of_seasons")
    tv["overview"] = res.get("overview")
    tv["url"] = "https://www.themoviedb.org/tv/%s" % tv_show_id

    cast_url = DOMAIN + ("/3/tv/%s/credits?api_key=%s&language=en-US" % (tv_show_id, API_KEY))
    cast_res = json.loads(requests.get(cast_url).text)
    cast_res = cast_res["cast"][:8] if len(cast_res["cast"]) > 8 else cast_res["cast"]
    cast_list = []
    for each in cast_res:
        cast = dict()
        cast["name"] = each.get("name")
        cast["profile_path"] = ("https://image.tmdb.org/t/p/w185" + each.get("profile_path")) \
                            if each.get("profile_path") != None else None
        cast["character"] = each.get("character")
        cast_list.append(cast)
    tv["casts"] = cast_list

    review_url = DOMAIN + ("/3/tv/%s/reviews?api_key=%s&language=en-US&page=1" % (tv_show_id, API_KEY))
    review_res = json.loads(requests.get(review_url).text)
    review_res = review_res["results"][:5] if len(review_res["results"]) > 5 else review_res["results"]
    review_list = []
    for each in review_res:
        review = dict()
        review["username"] = each["author_details"].get("username")
        review["content"] = each.get("content")
        review["rating"] = each["author_details"].get("rating")
        review["created_at"] = each.get("created_at")
        review_list.append(review)
    tv["reviews"] = review_list

    return json.dumps(tv)

@app.route("/genre", methods=['GET'])
def get_genres():
    movie_url = DOMAIN + ("/3/genre/movie/list?api_key=%s&language=en-US" % (API_KEY))
    movie_res = json.loads(requests.get(movie_url).text)
    l = []
    movie = dict()
    for each in movie_res["genres"]:
        movie[each["id"]] = each["name"]
    tv_url = DOMAIN + ("/3/genre/tv/list?api_key=%s&language=en-US" % (API_KEY))
    tv_res = json.loads(requests.get(tv_url).text)
    tv = dict()
    for each in tv_res["genres"]:
        tv[each["id"]] = each["name"]
    return json.dumps([movie, tv])

if __name__ == '__main__':
    app.run(port=5000)