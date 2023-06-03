from mrjob.job import MRJob

class MRMeanSalaryBySE(MRJob):

    def mapper(self, _, line):
        # Dividir la línea en campos
        id_employee, sector, salary, year = line.split(',')
        
        # Emitir el sector como clave y el salario como valor
        yield sector, float(salary)

    def reducer(self, sector, salaries):
        # Calcular el promedio de salarios
        total_salary = 0
        num_salaries = 0
        
        # Iterar sobre los salarios y calcular el total y el número de salarios
        for salary in salaries:
            total_salary += salary
            num_salaries += 1
        
        # Emitir el sector y el salario promedio
        yield sector, total_salary / num_salaries

if __name__ == '__main__':
    MRMeanSalaryBySE.run()
