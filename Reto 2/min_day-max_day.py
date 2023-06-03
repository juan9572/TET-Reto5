from mrjob.job import MRJob

class MRMinMaxPriceByCompany(MRJob):

    def mapper(self, _, line):
        # Dividir la línea en campos
        company, price, date = line.split(',')
        
        # Emitir la empresa como clave y una tupla con el precio y la fecha como valor
        yield company, (float(price), date)

    def reducer(self, company, price_date_pairs):
        # Obtener el primer par de precio y fecha como mínimo y máximo inicial
        min_price_date = max_price_date = next(price_date_pairs)
        
        # Iterar sobre los pares de precio y fecha restantes
        for price_date in price_date_pairs:
            if price_date[0] < min_price_date[0]:
                min_price_date = price_date
            elif price_date[0] > max_price_date[0]:
                max_price_date = price_date
        
        # Emitir la empresa y las tuplas de precio y fecha mínimos y máximos
        yield company, (min_price_date, max_price_date)

if __name__ == '__main__':
    MRMinMaxPriceByCompany.run()
