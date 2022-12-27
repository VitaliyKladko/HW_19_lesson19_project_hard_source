from dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self, filters: dict):
        """
        В сервис из вьюхи поступает dict, который имеет, либо не имеет status(new), происходит проверка и отдаются
        нужные фильмы
        """
        if filters.get('status') is not None and filters.get('status') == 'new':
            movies = self.dao.get_order_by_status()
        else:
            movies = self.dao.get_all()
        return movies

    def create(self, movie_d):
        return self.dao.create(movie_d)

    def update(self, movie_d):
        self.dao.update(movie_d)
        return self.dao

    def delete(self, rid):
        self.dao.delete(rid)
