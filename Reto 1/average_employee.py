from mrjob.job import MRJob

class MRMeanSalaryByEmployee(MRJob):

    def mapper(self, _, line):
        # Dividir la línea en campos
        id_employee, sector, salary, year = line.split(',')
        
        # Emitir el id del empleado como clave y el salario como valor
        yield id_employee, float(salary)

    def reducer(self, id_employee, salaries):
        # Calcular el promedio de salarios
        total_salary = 0
        num_salaries = 0
        
        # Iterar sobre los salarios y calcular el total y el número de salarios
        for salary in salaries:
            total_salary += salary
            num_salaries += 1
        
        # Emitir el id del empleado y el salario promedio
        yield id_employee, total_salary / num_salaries

if __name__ == '__main__':
    MRMeanSalaryByEmployee.run()
