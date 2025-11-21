# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""


# pylint: disable=import-outside-toplevel

import os
import shutil
import zipfile
from pathlib import Path

import pandas as pd


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.

    A partir de esta información se deben generar dos archivos CSV:

    - files/output/train_dataset.csv
    - files/output/test_dataset.csv

    Cada archivo debe tener dos columnas:

    * phrase: texto contenido en cada archivo .txt.
    * target: sentimiento asociado ("positive", "negative" o "neutral"),
      correspondiente al nombre del directorio donde se encuentra el archivo.
    """
    base_dir = Path("files")
    zip_path = base_dir / "input.zip"
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"

    # 1. Eliminar extracción anterior (si existe) para evitar duplicados
    if input_dir.exists():
        shutil.rmtree(input_dir)

    # 2. Extraer el ZIP en la carpeta "files"
    with zipfile.ZipFile(zip_path, mode="r") as archivo_zip:
        archivo_zip.extractall(base_dir)

    # 3. Preparar estructuras para almacenar la información
    registros_train = {"phrase": [], "target": []}
    registros_test = {"phrase": [], "target": []}

    # 4. Recorrer estructura de carpetas para construir los datasets
    for subset in ("train", "test"):
        subset_dir = input_dir / subset
        if not subset_dir.exists():
            continue

        for sentiment_dir in subset_dir.iterdir():
            if not sentiment_dir.is_dir():
                continue

            sentimiento = sentiment_dir.name  # positive / negative / neutral

            for txt_path in sentiment_dir.glob("*.txt"):
                texto = txt_path.read_text(encoding="utf-8").strip()

                if subset == "train":
                    registros_train["phrase"].append(texto)
                    registros_train["target"].append(sentimiento)
                else:  # subset == "test"
                    registros_test["phrase"].append(texto)
                    registros_test["target"].append(sentimiento)

    # 5. Crear carpeta de salida y guardar los CSV
    output_dir.mkdir(parents=True, exist_ok=True)

    pd.DataFrame(registros_train).to_csv(
        output_dir / "train_dataset.csv", index=False
    )
    pd.DataFrame(registros_test).to_csv(
        output_dir / "test_dataset.csv", index=False
    )

    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
