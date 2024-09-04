"""Generate metadata csv for CollectionBuilder from external datafile.

The raw data is in a tsv file
"""
import re
from csv import DictReader, DictWriter
from pathlib import Path
import urllib.parse
import os
from functools import partial


source = "/Users/wulfmanc/repos/gh/pulibrary/shadow_figures_cb/_data/metadata_old.csv"

def extracted_file_name(url) -> str:
    match = re.search(r".*?%2F(.*?)/", url)
    if match:
        return match.group(1).lower()
    else:
        return "NOIMAGE"

def small(url) -> str:
    fname = extracted_file_name(url)
    return f"/objects/small/{fname}_sm.jpg"


def thumb(url) -> str:
    fname = extracted_file_name(url)
    return f"/objects/thumbs/{fname}_th.jpg"


def full(url) -> str:
    fname = extracted_file_name(url)
    return f"/objects/{fname.upper()}.JPG"



rows = []
with open(source, 'r') as f:
    reader = DictReader(f)
    for row in reader:
        fname = row['image_thumb']
        row['image_thumb'] = thumb(fname)
        row['image_small'] = small(fname)
        row['object_location'] = full(fname)
        rows.append(row)

fieldnames = [k for k in rows[0].keys()]

with open('/tmp/mdnew.csv', 'w') as f:
    writer = DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    
