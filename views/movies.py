from flask import request
from flask_restx import Resource, Namespace

from dao.model.movie import MovieSchema
from implemented import movie_service
from constants import MOVIES_PER_PAGE
# from decorators import auth_required, admin_required


movie_ns = Namespace('movies')


@movie_ns.route('/')
class MoviesView(Resource):
    # @auth_required
    def get(self):
        # получаем квери параметры из адр.строки
        page = request.args.get('page')
        status = request.args.get('status')
        filters = {
            "status": status
        }
        all_movies = movie_service.get_all(filters)
        result = MovieSchema(many=True).dump(all_movies)

        # пагинация для movies
        if page is not None:
            page = int(page)-1
            result = result[page*MOVIES_PER_PAGE:(page+1)*MOVIES_PER_PAGE]

        return result, 200

    # @admin_required
    def post(self):
        req_json = request.json
        movie = movie_service.create(req_json)
        return "", 201, {"location": f"/movies/{movie.id}"}


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    # @auth_required
    def get(self, bid):
        b = movie_service.get_one(bid)
        sm_d = MovieSchema().dump(b)
        return sm_d, 200

    # @admin_required
    def put(self, bid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = bid
        movie_service.update(req_json)
        return "", 204

    # @admin_required
    def delete(self, bid):
        movie_service.delete(bid)
        return "", 204
