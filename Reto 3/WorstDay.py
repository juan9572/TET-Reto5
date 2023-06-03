from mrjob.job import MRJob
from mrjob.step import MRStep

class MRWorstRatingDay(MRJob):

    def mapper(self, _, line):
        # Dividir la línea en campos
        user, movie, rating, genre, date = line.split(',')
        
        # Emitir la fecha como clave y la calificación como valor
        yield date, float(rating)

    def reducer(self, date, ratings):
        # Convertir los valores de las calificaciones en una lista
        ratings_list = list(ratings)
        
        # Calcular el promedio de las calificaciones
        if ratings_list:
            avg_rating = sum(ratings_list) / len(ratings_list)
            
            # Emitir None como clave y una tupla con la fecha y el promedio de calificaciones como valor
            yield None, (date, avg_rating)
        else:
            # Si no hay calificaciones, emitir None como clave y una tupla con la fecha y 0 como valor
            yield None, (date, 0)

    def reducer_find_worst_day(self, _, date_avg_rating_pairs):
        # Encontrar el peor día de calificaciones basado en el promedio de calificaciones
        worst_day = min(date_avg_rating_pairs, key=lambda x: x[1])
        
        # Emitir 'Worst rating day' como clave y el peor día como valor
        yield 'Worst rating day', worst_day

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_worst_day)
        ]

if __name__ == '__main__':
    MRWorstRatingDay.run()
