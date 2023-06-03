from mrjob.job import MRJob

class MRStableOrIncreasingCompanies(MRJob):

    def mapper(self, _, line):
        # Dividir la línea en campos
        company, price, date = line.split(',')
        
        # Emitir la empresa como clave y una tupla con la fecha y el precio como valor
        yield company, (date, float(price))

    def reducer(self, company, date_price_pairs):
        # Ordenar las tuplas por fecha
        sorted_pairs = sorted(date_price_pairs, key=lambda x: x[0])
        
        # Verificar si los precios están estables o aumentando
        if all(sorted_pairs[i][1] <= sorted_pairs[i+1][1] for i in range(len(sorted_pairs) - 1)):
            yield company, 'Stable or Increasing'

if __name__ == '__main__':
    MRStableOrIncreasingCompanies.run()
