"""Tools for processing source csv into usable metadata files
"""
import re
from csv import DictReader, DictWriter
from pathlib import Path

source = "../_data/shadowfigures.tsv"
imagedir = Path("../objects")

images = []
objects = []
with open(source, mode="r", encoding="utf-8") as f:
    reader = DictReader(f, delimiter='\t')
    for row in reader:
        object = {}
        objectid = f"object_{row['objectno'].rjust(3, '0')}"
        object['objectid'] = objectid
        object['title'] = row['objecttype']
        object['subject'] = row['objecttype']
        object['display_template'] = 'record'
        description = re.sub(r"\n", " ", row['description'])
        object['description'] = description
        object['notes'] = row['notes']
        # objects.append(object)
        images = []
        for i,imagename in enumerate(row['imagename'].split('|')):
            filename = Path(imagename.lower())
            if (imagedir / filename).is_file():
                
                image = {}
                image['objectid'] = f"{objectid}_{i}"
                image['parentid'] = objectid
                image['title'] = f"{str(filename)} containing {objectid}"
                image['display_template'] = 'image'
                image['format'] = f"image/{filename.suffix[1:]}"
                image['object_location'] = f"/objects/{filename}"
                image['image_small'] = f"/objects/small/{filename.stem}_sm{filename.suffix}"
                image['image_thumb'] = f"/objects/thumbs/{filename.stem}_th{filename.suffix}"
                image['image_alt_text'] = f"image containing {objectid}"
                images.append(image)
                if len(images) == 1:
                    object['display_template'] = 'item'
                    object['image_thumb'] = images[0]['image_thumb']

                elif len(images) > 1:
                    object['display_template'] = 'compound_object'
                    object['image_thumb'] = images[0]['image_thumb']
        objects.append(object)
        objects = objects + images
                


with open("../_data/metadata.csv", "w", newline='', encoding="utf-8") as out:
    writer = DictWriter(out, fieldnames=['objectid', 'parentid', 'title','subject','display_template','format','object_location','image_small','image_thumb','image_alt_text','description', 'notes'])
    writer.writeheader()
    for object in objects:
        writer.writerow(object)
        
