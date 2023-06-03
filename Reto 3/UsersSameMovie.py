from mrjob.job import MRJob

class MRMovieUsers(MRJob):

    def mapper(self, _, line):
        # Dividir la línea en campos
        user, movie, rating, genre, date = line.split(',')
        
        # Emitir la película como clave y una tupla con el usuario y la calificación como valor
        yield movie, (user, float(rating))

    def reducer(self, movie, user_rating_pairs):
        # Inicializar variables para contar el número de usuarios y el total de calificaciones de la película
        num_users = 0
        total_rating = 0
        
        # Iterar sobre las tuplas de usuario y calificación
        for user, rating in user_rating_pairs:
            # Incrementar el contador de usuarios
            num_users += 1
            # Sumar la calificación al total de calificaciones
            total_rating += rating
        
        # Emitir la película como clave y una tupla con el número de usuarios y el promedio de calificaciones
        yield movie, (num_users, total_rating / num_users)

if __name__ == '__main__':
    MRMovieUsers.run()
