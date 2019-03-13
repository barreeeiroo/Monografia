# Four Factors

En esta carpeta se encuentra el software para el primer bloque del trabajo: machine learning supervisado.  

Se trata de un análisis de los four factors de un equipo dado para obtener cuales son de mayor importancia a la hora de decantar la victoria.

## Estructura de los archivos

En la carpeta `fourFactors/` se puede encontrar los siguientes archivos:

```bash
.
├── fourFactors.csv            - Autogenerado. Contiene los cuatro (ocho en realidad) factores de cada partido.
├── Four Factors.ipynb         - Libreta de Python del análisis de los Four Factors para predecir victorias.
├── generate.py                - Genera los four factors a partir de los datos CSV dados
├── Regresion Logistica.ipynb  - Libreta de Python del análisis (sin buenas conclusiones) de la regresión logística para predecir victorias.
└── script.py                  - Obtiene los pesos de los four factors
```

## iPython Notebooks

- `Four Factors.ipynb`: Libreta principal, contiene todo el trabajo detallado paso a paso y explicado, junto con las primeras conclusiones. La más positiva de todas, acierta todas (o todas excepto una) las victorias del equipo de la muestra de prueba.

- `Regresion Logistica.ipynb`: Libreta secundaria, contiene el trabajo de prueba con la regresión logística para predecir victorias, pero con resultados no muy positivos.

## Uso de los archivos

- `generate.py`: Devuelve 4 listas, cada una con los four factors de cada partido jugado. Los archivos de entrada se encuentran en la carpeta `../scrapper/fourFactors/csv/`, y han de ser generados antes de ejecutar este script de Python. El script de Python general el archivo `fourFactors.csv` que es usado en el script de machine learning.

- `script.py`: Es el script encargado de obtener los pesos y comprobar la fiabilidad del modelo en cuestión. Para poder entenderlo mejor, se recomienda abrir el archivo `Four Factors.ipynb` ya que es un archivo de iPython Notebook con muchos comentarios y Github lo hace más agradable a la lectura.

### Secuencia de archivos

Para poder simular este proyecto, hace falta ejecutar los siguientes archivos en este orden:

1. `php Monografia/scrapper/fourFactors/matches.php` _Opcional: Sólo en caso de querer usar nuevos datos_
2. `python3 Monografia/fourFactors/generate.py` _Opcional: Sólo en caso de querer usar nuevos datos_
3. `python3 Monografia/fourFactors/script.py`

El primero descarga los datos a CSV de forma masiva, el segundo obtiene los four factors y el tercero es el encargado de hacer machine learning.
