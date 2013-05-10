import collections


_Movie = collections.namedtuple("Movie", "movie_id title track_term poster_uri")


MOVIES = {
	'ironman': _Movie(1, "Ironman", "ironman", "ironman.jpg"),
	'great-gatsby': _Movie(2, "The Great Gatsby", "great gatsby", "great-gatsby.jpg"),
	'scary-movie': _Movie(3, "Scary Movie V", "scary movie", "scary-movie.jpg"),
}