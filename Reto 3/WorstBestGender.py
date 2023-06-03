from mrjob.job import MRJob
from mrjob.step import MRStep

class MRBestWorstMovieByGenre(MRJob):

    def mapper(self, _, line):
        # Dividir la línea en campos
        user, movie, rating, genre, date = line.split(',')
        
        # Emitir una clave compuesta por el género y la película, y la calificación como valor
        yield (genre, movie), float(rating)

    def reducer(self, keys, ratings):
        # Convertir los valores de las calificaciones en una lista
        ratings_list = list(ratings)
        
        # Calcular el promedio de las calificaciones
        if ratings_list:
            avg_rating = sum(ratings_list) / len(ratings_list)
            
            # Emitir el género como clave y una tupla con la película y el promedio de calificaciones como valor
            yield keys[0], (keys[1], avg_rating)

    def reducer_find_best_worst(self, genre, movie_avg_ratings):
        # Convertir los valores de las películas y los promedios de calificaciones en una lista
        movie_avg_ratings = list(movie_avg_ratings)
        
        # Encontrar la mejor y peor película basada en el promedio de calificaciones
        if movie_avg_ratings:
            best_movie = max(movie_avg_ratings, key=lambda x: x[1])
            worst_movie = min(movie_avg_ratings, key=lambda x: x[1])
            
            # Emitir el género como clave y una tupla con la mejor y peor película como valor
            yield genre, (best_movie, worst_movie)

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_best_worst)
        ]

if __name__ == '__main__':
    MRBestWorstMovieByGenre.run()
