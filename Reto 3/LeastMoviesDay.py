from mrjob.job import MRJob
from mrjob.step import MRStep

class MRLeastMoviesDay(MRJob):

    def mapper(self, _, line):
        # Dividir la línea en campos
        user, movie, rating, genre, date = line.split(',')
        
        # Emitir la fecha como clave y el valor 1 para contar las películas en ese día
        yield date, 1

    def reducer(self, date, counts):
        # Emitir una clave nula y una tupla con la fecha y la suma de los conteos de películas
        yield None, (date, sum(counts))

    def reducer_find_min_day(self, _, date_count_pairs):
        # Encontrar el día con la menor cantidad de películas
        min_day = min(date_count_pairs, key=lambda x: x[1])
        
        # Emitir la etiqueta 'Least movies day' y el día con la menor cantidad de películas
        yield 'Least movies day', min_day

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_min_day)
        ]

if __name__ == '__main__':
    MRLeastMoviesDay.run()
