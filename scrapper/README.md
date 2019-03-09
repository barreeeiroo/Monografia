# Scrapper

En esta carpeta se encuentra el software para convertir los datos de la web RealGM Basketball a los adecuados para su manipulación en Python.  

El software para sacar los datos de RealGM fue primero diseñado para convertirlos a JSON, y es por eso que se obtienen los datos en un JSON y posteriormente se convierte a un CSV.

## Estructura de los archivos

En la carpeta `scrapper/`, se puede encontrar los siguientes archivos:

```bash
.
├── fourFactors
│   ├── csv
│   │   └── output##*.csv - Autogenerado. Cada archivo contiene los datos de un equipo para el partido ##. Si la letra es A se trata del equipo deseado, y si es B del rival.
│   └── out.json          - Autogenerado. Contiene todos los mismos datos que los CSV.
├── matches.1.php         - Script para convertir obtener los datos adecuados para el análsis de los four factors. Los resultados salen en la carpeta fourFactors/
└── dom.php               - Librería para parsear facilmente el formato HTML
```

## Uso de los archivos

- `matches.1.php`: En la variable `$URL` se coloca la URL de la temporada de la que se quiere obtener los datos, y se ejecuta con `php matches.php`. Comenzará a mapear todos los partidos de la temporada en cuestión, y generará un archivo llamado `fourFactors/out.json` y varios `fourFactors/csv/output##*.csv` para poder trabajar con estos.