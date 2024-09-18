"""Change urls to objects directory


"""
import re
from csv import DictReader, DictWriter
from pathlib import Path
import urllib.parse
import os
from functools import partial


source = "../_data/shadowfigures.tsv"
# source = "../_data/metadata_old.csv"

# imagedir = Path("../objects")

bucket = Path("ealshadowobjects")

def identifier_from_image_name(image_name):
    return urllib.parse.quote_plus(f"{bucket}/{os.path.splitext(image_name)[0]}")

def iiif_uri(scheme, server, prefix, identifier, region, size, rotation, quality, format):
    return f"{scheme}://{server}/{prefix}/{identifier}/{region}/{size}/{rotation}/{quality}.{format}"

object_uri = partial(iiif_uri,
              scheme="https",
              server="puliiif-staging.princeton.edu",
              prefix="iiif/2",
              region="full",
              rotation=0,
              quality="default",
              format="jpg")

def object_location(image_name):
    return "/objects/" + image_name 

def image_small(image_name):
    return "/objects/small/" + image_name.replace(".JPG","_sm.jpg")

def image_thumb(image_name):
    return "/objects/thumbs/" + image_name.replace(".JPG","_th.jpg")


def extant_images(names_string, flags_string, objects_string):
    images = names_string.split('|')
    flags = flags_string.split('|')
    objects = objects_string.split('|')
   # print(objects_string)
    if len(images) != len(flags):
        raise(ValueError("image list and flag list are not the same size"))
    return [[fname, objs] for fname, objs, flag in zip(images, objects, flags) if flag == 'YES']

def object_title(description):
    pattern = re.compile(r"^([^\.]+)")
    try:
        title = pattern.match(description)[0]
    except IndexError:
        result = "Untitled"
    return title


objects = []
all_images = dict()
with open(source, mode="r", encoding="utf-8") as f:
    reader = DictReader(f, delimiter='\t')
    for row in reader:
        object = {}
        objectid = f"object_{row['objectno'].rjust(4, '0')}"
        objectname = f"Object {row['objectno']}"
        object['objectid'] = objectid
        object['identifier'] = row['objectno']
        object['title'] = object_title(row['description'])
        object['subject'] = row['objecttype']
        object['dimensions'] = row['dimensions']
        object['display_template'] = 'record'
        description = re.sub(r"\n", " ", row['description'])
        object['description'] = description
        object['notes'] = row['notes']
        # objects.append(object)
        images = []
        real_images = extant_images(row['imagename'], row['imageexists'], row['imagecomments'])
        try:
            thumbnail = image_thumb(real_images[0][0])
        except IndexError:
            thumbnail = None
            print(f"no images for {objectid}")

        #if len(real_images) == 1:
        #    object['display_template'] = 'item'
        #else:
        object['display_template'] = 'compound_object'
        object['image_thumb'] = thumbnail

        for i,(image_name, other_objects) in enumerate(real_images):
            image = {}
            image['objectid'] = f"{objectid}_{i}"
            image['parentid'] = objectid

            if not(image_name) in all_images:
                all_images[image_name] = len(all_images) + 1

            filename = Path(image_name)
            #image['title'] = f"Image {all_images[image_name]} containing {objectname}"
            image['display_template'] = 'image'
            image['format'] = "image/jpg" # as delivered by IIIF server
            image['object_location'] = object_location(image_name).lower()
            image['image_small'] = image_small(image_name).lower()
            image['image_thumb'] = image_thumb(image_name).lower()
            image['image_alt_text'] = f"image containing {objectid}"

            image['identifier'] = row['objectno']

            other_objects = other_objects.replace(" ","")
            other_objects_a = other_objects.split(",")
            other_objects = ""
            for object_name in other_objects_a:
                obj_num = '{:04d}'.format(int(re.search(r'\d+', object_name).group()))
                if f"object_{obj_num}" != objectid:
                    if other_objects != "":
                        other_objects += ";"
                    other_objects += f"object_{obj_num}"
            image['other_objects'] = other_objects
            images.append(image)

        objects.append(object)
        objects = objects + images


if __name__ == '__main__':
    outfile = "../_data/metadata.csv"
    #outfile = "/tmp/cb_test.csv"
    with open(outfile, "w", newline='', encoding="utf-8") as out:
        writer = DictWriter(out, fieldnames=['objectid', 'parentid', 'title','identifier','subject','dimensions','display_template','format','object_location','image_small','image_thumb','image_alt_text','description', 'notes', 'other_objects'])
        writer.writeheader()
        for object in objects:
            writer.writerow(object)
