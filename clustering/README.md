# Clustering

En esta carpeta se encuentra el software para el segundo bloque del trabajo: machine learning nosupervisado.  

Esta parte del trabajo consiste en la clasificación de jugadores en función de sus características y aptitudes para su posible fichaje por parte de un equipo.

## Estructura de los archivos

En la carpeta `clustering/` se puede encontrar los siguientes archivos:

```bash
.
├── Clustering.ipynb  - Libreta de Python con todo el trabajo paso a paso de los dos modelos de clustering.
└── script.py         - Similar a la libreta, pero ejecutable.
```

## iPython Notebooks

- `Clustering.ipynb`: Libreta única, es el trabajo del análisis paso a paso y comentado. En la misma libreta se hace el trabajo del _Clustering Jerárquico_ y del _Clustering K-Means_.

## Uso de los archivos

- `script.py`: Es el script encargado de clasificar los jugadores. Para poder entenderlo mejor, se recomienda abrir el archivo `Clustering.ipynb` ya que es un archivo de iPython Notebook con muchos comentarios y Github lo hace más agradable a la lectura.

### Secuencia de archivos

Para poder simular este proyecto, hace falta ejecutar los siguientes archivos en este orden:

1. `php Monografia/scrapper/clustering/matches.php`
2. `python3 Monografia/clustering/script.py`

El primero descarga los datos y genera el CSV, y el segundo se encarga de ejecutar el análisis de _machine learning_.
