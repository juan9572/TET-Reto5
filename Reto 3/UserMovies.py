from mrjob.job import MRJob

class MRUserMovies(MRJob):

    def mapper(self, _, line):
        # Dividir la línea en campos
        user, movie, rating, genre, date = line.split(',')
        
        # Emitir el usuario como clave y una tupla con la película y la calificación como valor
        yield user, (movie, float(rating))

    def reducer(self, user, movie_rating_pairs):
        # Inicializar variables para contar el número de películas y el total de calificaciones del usuario
        num_movies = 0
        total_rating = 0
        
        # Iterar sobre las tuplas de película y calificación
        for movie, rating in movie_rating_pairs:
            # Incrementar el contador de películas
            num_movies += 1
            # Sumar la calificación a la calificación total
            total_rating += rating
        
        # Emitir el usuario como clave y una tupla con el número de películas y el promedio de calificaciones
        yield user, (num_movies, total_rating / num_movies)

if __name__ == '__main__':
    MRUserMovies.run()
