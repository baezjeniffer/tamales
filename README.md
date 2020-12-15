# Tamales INC
## Requerimientos
* Tener instalado Docker
## Despliegue
1. Clonar repositorio de github: git clone https://github.com/baezjeniffer/tamales 
2. Entrar a carpeta **tamales**, que fue creada después de haber ejecutado el comando anterior
3. Ejecutar los siguientes comandos en forma secuencial: 

```
docker build -t tamales:latest .
docker run -d -p 5000:5000 tamales
```
4. Una vez levantado el Docker podrá consumir los siguientes servicios:

### ETL endpoint

URL: 127.0.0.1:5000/reprocesamiento

Request body:
{"date_exec":"YYYYMMDD"}

Respond body:

{"Flag":"True"} -> en caso de que la ejecución sea exitosa

{"Flag":"False"} -> en caso de que la ejecución no sea exitosa

Este servicio procesa la información cruda centralizando los datos de Tamales_Inc y TeInvento_Inc generando los archivos con la información procesada.

### Modelo endpoint

URL: 127.0.0.1:5000/model

Request body:
{"date":"YYYY-MM-DD","id_product":numeric_value}

Ejemplo: {"date":"2019-01-01","id_product"::85899345920}

Respond body:

{"Flag":"True","Result":prediction_value} -> en caso de que la ejecución sea exitosa

{"Flag":"False","Result":None} -> en caso de que la ejecución no sea exitosa

Este servicio genera la predicción del modelo con las ventas y categpria calórica basados en la fecha y el identificador del producto.

### Orquestador
El orquestador es a través de un cron de Linux que se inicia al levantar el Docker y será ejecutado al final del día (23:59) de cada Domingo. El cron iniciará el proceso ETL que consume los datos de los 6 días previos a la fecha de ejecucióny genera los datos procesados (métricas y generación de modelo estrella).

## Ventajas:
1. Se utilizó Docker con el objetivo de que el despliegue sea agnóstico en cualquier sistema operativo o nube que tenga instalado Docker.
2. El reprocesamiento de datos puede hacerse en cualquier momento debido a que se cuenta con un servicio al igual que el modelo.
3. Docker nos permite ser escalable, sin embargo serían necesarias otras herramientas para orquestar los contenedores.


## Desventajas:
1. Tiene que desarrollarse métricas de calidad de información.
2. Debe haber solo un archivo por semana.
3. El almacenamiento está de manera local, lo cual impide la disponibilidad para otros usuarios, por lo que sería necesario un motor de base de datos debido al modelo de almacenamiento estrella propuesto o un storage como S3.

## Notas:
Se agrega un ejemplo de los datos procesados en la carpeta procesado/generador/ para tamales_inc y teinvento_inc.

