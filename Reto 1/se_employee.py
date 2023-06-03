from mrjob.job import MRJob
from mrjob.step import MRStep

class MRNumSEByEmployee(MRJob):

    def mapper(self, _, line):
        # Dividir la línea en campos
        id_employee, sector, _, _ = line.split(',')
        
        # Emitir una clave compuesta por el id del empleado y el sector, y un valor nulo
        yield (id_employee, sector), None

    def reducer(self, keys, values):
        # Emitir el id del empleado y el sector
        yield keys[0], keys[1]

    def reducer_count_sectors(self, id_employee, sectors):
        # Contar el número de sectores únicos
        unique_sectors = len(set(sectors))
        
        # Emitir el id del empleado y el número de sectores únicos
        yield id_employee, unique_sectors

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.reducer_count_sectors)
        ]

if __name__ == '__main__':
    MRNumSEByEmployee.run()
