from mrjob.job import MRJob
from mrjob.step import MRStep

class MRBlackDay(MRJob):

    def mapper(self, _, line):
        # Dividir la línea en campos
        company, price, date = line.split(',')
        
        # Emitir la fecha como clave y el precio como valor
        yield date, float(price)

    def reducer(self, date, prices):
        # Encontrar el precio mínimo para la fecha dada
        min_price = min(prices)
        
        # Emitir una clave nula y una tupla con la fecha y el precio mínimo
        yield None, (date, min_price)

    def reducer_find_black_day(self, _, date_minprice_pairs):
        # Encontrar el "Día Negro" (Black Day) basado en el precio mínimo
        black_day = min(date_minprice_pairs, key=lambda x: x[1])
        
        # Emitir la etiqueta 'Black Day' y el "Día Negro" encontrado
        yield 'Black Day', black_day

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_find_black_day)
        ]

if __name__ == '__main__':
    MRBlackDay.run()
