# Descargador de SVG de MuseScore

Este script permite descargar imágenes SVG de una página de MuseScore y combinarlas en un archivo PDF.

## Requisitos

- Python 3.x

- Bibliotecas necesarias:

- `requests`

- `selenium`

- `webdriver-manager`

- `beautifulsoup4`

- `cairosvg`

- `PyPDF2`

Puedes instalar las bibliotecas necesarias usando pip:

```
pip  install  -r requirements.txt
```

## Uso

- Clona o descarga este repositorio.

- Abre una terminal y navega al directorio donde se encuentra el script.

- Ejecuta el script pasando la URL de la página de MuseScore como parámetro:

  `python3  script.py  https://musescore.com/user/73972/scores/1352796`

#### Nota: Asegúrate de no incluir comillas alrededor de la URL.

## Descripción

El script realiza las siguientes acciones:

- Carga la página de MuseScore especificada en la URL.

- Busca imágenes SVG dentro de los elementos del scroller.

- Descarga las imágenes SVG encontradas.

- Convierte las imágenes SVG a un archivo PDF.

- El archivo PDF se guarda con el título de la página de MuseScore.
