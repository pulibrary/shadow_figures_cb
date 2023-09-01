import urllib.parse
import os
from pathlib import Path
from functools import partial

sample_string = "https://puliiif-staging.s3.amazonaws.com/ealshadowobjects/dscn0086.tif"

base_url = "https://puliiif-staging.princeton.edu/iiif/2"

foo = "ealshadowfigures%2Fdsc_0017/full/full/0/default.jpg"

image_name = "DSCN3617.JPG"

bucket = Path("ealshadowobjects")

def identifier_from_image_name(image_name):
    return urllib.parse.quote_plus(f"{bucket}/{os.path.splitext(image_name)[0].lower()}")

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
    return object_uri(identifier=identifier_from_image_name(image_name),
                      size="full")

def image_small(image_name):
    return object_uri(identifier=identifier_from_image_name(image_name),
                      size="800,")

def image_thumb(image_name):
    return object_uri(identifier=identifier_from_image_name(image_name),
                      size="400,")

def iiif_full(image_name):
    identifier = identifier_from_image_name(image_name)
    return iiif_uri(scheme="https",
                    server="puliiif-staging.princeton.edu",
                    prefix="iiif/2",
                    identifier=identifier,
                    region="full",
                    size="full",
                    rotation=0,
                    quality="default",
                    format="jpg")

def iiif_small(image_name):
    identifier = identifier_from_image_name(image_name)
    return iiif_uri(scheme="https",
                    server="puliiif-staging.princeton.edu",
                    prefix="iiif/2",
                    identifier=identifier,
                    region="full",
                    size="800,",
                    rotation=0,
                    quality="default",
                    format="jpg")

def iiif_thumb(image_name):
    identifier = identifier_from_image_name(image_name)
    return iiif_uri(scheme="https",
                    server="puliiif-staging.princeton.edu",
                    prefix="iiif/2",
                    identifier=identifier,
                    region="full",
                    size="400,",
                    rotation=0,
                    quality="default",
                    format="jpg")


def extant_images(names_string, flags_string):
    images = names_string.split('|')
    flags = flags_string.split('|')
    if len(images) != len(flags):
        raise(ValueError("image list and flag list are not the same size"))
    return [fname for fname, flag in zip(images, flags) if flag == 'YES']
