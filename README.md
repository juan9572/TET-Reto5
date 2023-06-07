# TET_Reto_N5

## Tabla de contenidos:
---

1.  [Información de la asignatura](#información-de-la-asignatura)

2. [Datos del estudiante](#datos-del-estudiante)

3. [Descripción y alcance del proyecto](#descripción-y-alcance-del-proyecto)

4. [Paso a paso del despliegue](#paso-a-paso-del-despliegue)

5. [Referencias](#referencias) 

## Información de la asignatura
---

 -  **Nombre de la asignatura:** Tópicos especiales en telemática.
-   **Código de la asignatura:**  C2361-ST0263-4528
-   **Departamento:** Departamento de Informática y Sistemas (Universidad EAFIT).
-   **Nombre del profesor:** Juan Carlos Montoya Mendoza.
-  **Correo electrónico del docente:** __[jcmontoy@eafit.edu.co](mailto:jcmontoy@eafit.edu.co)__.

## Datos del estudiante
---

-   **Nombre del estudiante:** Juan Pablo Rincon Usma.
-  **Correo electrónico del estudiante:** __[jprinconu@eafit.edu.co](mailto:jprinconu@eafit.edu.co)__.

## Descripción y alcance del proyecto
---


El reto consiste en procesar grandes volúmenes de datos utilizando técnicas de map/reduce en un cluster de EMR (Elastic MapReduce). EMR es un servicio de AWS que permite procesar grandes conjuntos de datos de manera distribuida utilizando el paradigma de map/reduce.

El objetivo principal es realizar operaciones de transformación y análisis en datos de gran escala de manera eficiente y escalable. Esto implica dividir el conjunto de datos en bloques más pequeños, distribuirlos en un clúster de EMR y ejecutar tareas de map/reduce en paralelo en los nodos del clúster.

El enfoque de map/reduce se basa en dos fases principales: la fase de map y la fase de reduce. En la fase de map, los datos se dividen en pares clave-valor y se procesan de forma independiente en cada nodo del clúster. En la fase de reduce, los resultados intermedios generados por la fase de map se combinan y se realiza un procesamiento adicional para obtener los resultados finales.

## Paso a paso del despliegue
---
1. Configurar las credenciales de AWS para acceder a los servicios de AWS. Abre el archivo ~/.aws/credentials y asegúrate de incluir las siguientes líneas con tus propias credenciales:

>[default]
aws_access_key_id = SECRET_ACCES_KEY
aws_secret_access_key = SECRET_KEY
aws_session_token = SECRET_KEY

2.  Descargar e instalar la AWS CLI para Windows y agregarla a las variables de entorno. Puedes seguir las instrucciones en el siguiente enlace: AWS CLI - Guía de instalación
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

3. Crear un bucket en Amazon S3 para almacenar los datos del reto. Ejecuta el siguiente comando para crear el bucket:
	```bash
	aws s3 mb s3://bucket.reto5
	```
	![a](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/1.png)

4. Crear las carpetas necesarias en el bucket de S3 utilizando los siguientes comandos:
	```bash
	aws s3api put-object --bucket bucket.reto5 --key logs/
	aws s3api put-object --bucket bucket.reto5 --key inputs/
	aws s3api put-object --bucket bucket.reto5 --key outputs/
	aws s3api put-object --bucket bucket.reto5 --key scripts/
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/2.png)

5. Crear un grupo de seguridad en EC2 para permitir conexiones SSH. Ejecuta los siguientes comandos:
	```bash
	aws ec2 create-security-group --group-name ssh-my-ip --description "For SSHing from my IP" --vpc-id $VPC_ID
	aws ec2 authorize-security-group-ingress --group-id $SEC_GP --protocol tcp --port 22 --cidr 0.0.0.0/0
	```
	
6. Crear el clúster de EMR con la configuración deseada. Utiliza el siguiente comando como ejemplo:
	```bash
	aws emr create-cluster --name reto5-cluster --applications Name=Hadoop Name=Hive Name=Spark Name=Hue --release-label emr-5.33.0 --use-default-roles --instance-count 3 --instance-type m4.large --ebs-root-volume-size 12 --log-uri s3://bucket.reto5/logs --ec2-attributes KeyName=MasterKey,AdditionalMasterSecurityGroups=sg-095464fa5ce8a06ce --no-auto-terminate
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/5.png)

7. Obtener el DNS del clúster de EMR mediante el siguiente comando:
	```bash
	aws emr describe-cluster --cluster-id $ID_CLUSTER
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/6.png)
8.  Conectarse al clúster utilizando SSH. Ejecuta el siguiente comando con tu propia dirección DNS y clave:
	```bash
	ssh hadoop@ec2-107-21-66-81.compute-1.amazonaws.com -i MasterKey.pem
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/7.png)
9. Clonar el repositorio en el clúster utilizando los siguientes comandos:
	```bash
	sudo yum install git python3-pip && sudo pip3 install mrjob
	sudo git clone https://github.com/ST0263/st0263-2023-1.git
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/8.png)
10. Ejecutar el programa de la versión serial-secuencial utilizando el siguiente comando:
	```bash
	cd st0263-2023-1/Laboratorio\ N6-MapReduce/wordcount/
	sudo python wordcount-local.py ../../datasets/gutenberg-small/*.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/9.png)
11. Ejecutar el programa de la versión map/reduce utilizando el siguiente comando:
	```bash
	python wordcount-mr.py ../../datasets/gutenberg-small/*.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/10.png)
12. Ejecutar el programa de mrjob en Hadoop utilizando los siguientes pasos:

* Crear la carpeta en hadoop donde se almacenaran los datasets
	```bash
	hdfs dfs -mkdir /user/hadoop/datasets/
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/25.png)
* Nos movemos a la ruta donde estan los datasets y copiamos los datos en hadoop:
	```bash
	cd st0263-2023-1/
	hdfs dfs -copyFromLocal ./datasets/* /user/hadoop/datasets/
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/26.png)
* Ejecutar el siguiente comando para lanzar el trabajo en EMR:
	```bash
	python wordcount-mr.py hdfs:///user/hadoop/datasets/gutenberg-small/*.txt -r hadoop --output-dir hdfs:///user/hadoop/results --hadoop-streaming-jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/27.png)
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/28.png)
* Confirmamos la salida del archivo:
	```bash
	hdfs dfs -ls /user/hadoop/results
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/29.png)
	```bash
	hdfs dfs -cat /user/hadoop/results/part-00000
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/30.png)

13. Para el Reto 1, descargar el repositorio y ejecutar los siguientes programas y comandos:
* Salario promedio por Sector Económico (SE):
	```bash
	python average_se.py ../../st0263-2023-1/datasets/otros/dataempleados.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/12.png)
* El salario promedio por Empleado:
	```bash
	python average_employee.py.py ../../st0263-2023-1/datasets/otros/dataempleados.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/13.png)
* Número de SE por Empleado que ha tenido a lo largo de la estadística:
	```bash
	python se_employee.py ../../st0263-2023-1/datasets/otros/dataempleados.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/14.png)
14. Para el Reto 2, ejecutar los siguientes programas y comandos:
* Por acción, día con el menor valor y día con el mayor valor:
	```bash
	python min_day-max_day.py ../../st0263-2023-1/datasets/otros/dataempresas.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/15.png)
* Listado de acciones que siempre han subido o se mantienen estables:
	```bash
	python crescent_actions.py ../../st0263-2023-1/datasets/otros/dataempresas.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/16.png)
* Día Negro: Obtener el día en el que la mayor cantidad de acciones tienen el menor valor de acción (desplome):
	```bash
	python black_day.py ../../st0263-2023-1/datasets/otros/dataempresas.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/17.png)
15. Para el Reto 3, ejecutar los siguientes programas y comandos:
* Número de películas vistas por usuario y valor promedio de calificación:
	```bash
	python UserMovies.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/18.png)
* Día en que se han visto más películas:
	```bash
	python MostMoviesDay.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/19.png)
* Día en que se han visto menos películas::
	```bash
	python LeastMoviesDay.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/20.png)
* Número de usuarios que ven una misma película y el rating promedio:
	```bash
	python UsersSameMovie.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/21.png)
* Día en que se ha dado la peor evaluación promedio por los usuarios:
	```bash
	python WorstDay.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/22.png)
* Día en que se ha dado la mejor evaluación por los usuarios:
	```bash
	python BestDay.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/23.png)
* La mejor y peor película evaluada por género:
	```bash
	python WorstBestGender.py ../../st0263-2023-1/datasets/otros/datapeliculas.txt
	```
	![enter image description here](https://raw.githubusercontent.com/juan9572/TET_Reto_N5/main/Static/24.png)
## Referencias
---

- [How to Create Interactive AWS Elastic Map Reduce (EMR) Clusters using the AWS CLI](https://thecodinginterface.com/blog/create-aws-emr-with-aws-cli/)
- [AWS CLI for Windows]([https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html))
