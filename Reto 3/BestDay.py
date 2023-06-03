from mrjob.job import MRJob
from mrjob.step import MRStep

class MRBestRatingDay(MRJob):

    def mapper(self, _, line):
        # Dividir la línea en campos
        user, movie, rating, genre, date = line.split(',')
        
        # Emitir la fecha como clave y el rating como valor
        yield date, float(rating)

    def reducer(self, date, ratings):
        # Convertir los ratings en una lista
        ratings_list = list(ratings)
        
        # Verificar si la lista no está vacía
        if len(ratings_list) != 0:
            # Calcular el promedio de los ratings para la fecha dada
            avg_rating = sum(ratings_list) / len(ratings_list)
            
            # Emitir una clave nula y una tupla con la fecha y el promedio de ratings
            yield None, (date, avg_rating)

    def reducer_find_best_day(self, _, date_avg_rating_pairs):
        # Encontrar el mejor día de calificación basado en el promedio de ratings
        best_day = max(date_avg_rating_pairs, key=lambda x: x[1])
        
        # Emitir la etiqueta 'Best rating day' y el mejor día encontrado
        yield 'Best rating day', best_day

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_best_day)
        ]

if __name__ == '__main__':
    MRBestRatingDay.run()
