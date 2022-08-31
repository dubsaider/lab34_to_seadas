## Python enviroment

```bash
python -m venv .env
. .env/bin/ativate
```

## Download

Download GDAL and rasterio libraries for your version of Python.

https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal

https://www.lfd.uci.edu/~gohlke/pythonlibs/#rasterio

## Installation

Installation in Python enviroment.

```bash
pip install numpy
pip install "path to GDAL library"
pip install "path to rasterio library"
pip install pyproj
pip install pycstruct
```

## Run script

Run script in Python enviroment.

```bash
python main.py "path to file .pro" "name of output file"
```

## Cloud mask script

Run script in Python enviroment.

```bash
python main.py "path to file .pro" "name of output file" "cloud temperature threshold"
```
