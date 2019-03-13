# Scraper

En esta carpeta se encuentra el software para convertir los datos de la web RealGM Basketball a los adecuados para su manipulación en Python.  

El software para sacar los datos de RealGM fue primero diseñado para convertirlos a JSON, y es por eso que se obtienen los datos en un JSON y posteriormente se convierte a un CSV.

## Estructura de los archivos

En la carpeta `scraper/` se puede encontrar los siguientes archivos:

```bash
.
├── clustering
│   ├── matches.php       - Script para obtener los datos de todos los jugadores de una liga.
│   ├── out#.json         - Autogenerado. Archivo con los datos de una página de los jugadores.
│   ├── out.csv           - Autogenerado. Archivo con todos los datos de todos los jugadores en formato CSV.
│   └── out.json          - Autogenerado. Archivo con todos los datos de todos los jugadores.
├── dom.php               - Librería para parsear facilmente el formato HTML
└── fourFactors
    ├── csv
    │   └── output##*.csv - Autogenerado. Cada archivo contiene los datos de un equipo para el partido ##. Si la letra es A se trata del equipo deseado, y si es B del rival.
    ├── dom.php               - 
    ├── matches.php       - Script para convertir obtener los datos adecuados para el análsis de los four factors. Los resultados salen en la carpeta fourFactors/
    └── out.json          - Autogenerado. Contiene todos los mismos datos que los CSV.
```

## Uso de los archivos

- `fourFactors/matches.php`: En la variable `$SEASON` se coloca la temporada de la que se quiere obtener los datos y en `$TEAM` el equipo, y se ejecuta con `php matches.php`. Comenzará a mapear todos los partidos de la temporada en cuestión, y generará un archivo llamado `fourFactors/out.json` y varios `fourFactors/csv/output##*.csv` para poder trabajar con estos. En los archivos CSV, `##` significa el número de partido de la temporada, y `*` será o bien A (si se trata de los datos del equipo deseado) o bien B (si son los del oponente).

- `clustering/matches.php`: En la variable `$SEASON` se coloca la temporada de la que se quiere obtener los datos y en `$LEAGUE` el ID de la liga, y se ejecuta con `php matches.php`. Comenzará a mapear todos los jugadores de la temporada en cuestión, y generará varios archivos llamado `clustering/out#.json` (siendo `#` un contador de las páginas mapeadas) y un `clustering/out.json` y `clustering/out.csv` que es una combinación de los anteriores. Se trabajará con el CSV.
