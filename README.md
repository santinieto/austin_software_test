DESCRIPCIONES DEL PROYECTO

CARPETAS
    - tasks: En esta carpeta esta guardado el README donde se explica la actividad a realizar
    - seatmaps: En esta carpeta estan los archivos provistos para llevar a cabo la actividad
    - scripts: En esta carpeta están los scripts aportados como soluciones a la actividad
        - seatmap_parser.py: Script principal que parsea los archivos .xml a .json
        - seatmap_parser.ipynb: Script de Jupyter con propositos de debug con el que fue diseñado el script final
    - results: En esta carpeta se guardan los archivos .json obtenidos como salida de los scripts mencionados

MODO DE EJECUCION
Para correr los scripts se deben llevar a cabo los siguientes pasos:
    1 - Abrir un terminal o consola que disponga de Python (para este proyecto utilize Python3)
    2 - Ubicarse dentro de la carpeta scripts/ que se encuentra dentro de este repositorio
    3 - Correr el script principal como:
        $ python seatmap_parser.py <filename>
        Donde <filename> puede ser "seatmap1.xml" o "seatmap2.xml"
    4 - Corroborar los resultados (archivos .json) que se obtienen como salida, los cuales se encuentran dentro de la
        carpeta results/ de este repositorio

NOTAS:
    - Para poder correr los scripts desde cualquier punto podria proveerse el path absoluto que apunta a los .xml
      pero ese depende de cada equipo
    - El script "seatmap_parser.ipynb" es un script de Jupyter creado a través de Anaconda Navigator, se va a necesitar la
      aplicacion Jupyter para correrlo de manera efectiva