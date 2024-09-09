"""Tools for processing source csv into usable metadata files
"""
import re
from csv import DictReader, DictWriter
from pathlib import Path

source = "../_data/shadowfigures.tsv"
imagedir = Path("../objects")

records = []
objects = []
with open(source, mode="r", encoding="utf-8") as f:
    reader = DictReader(f, delimiter='\t')
    for row in reader:
        records.append(row)
        
