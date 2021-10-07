""" This module contains general query functions """

import weaviate
from modules.utilities import generate_uuid



TEMPLATE = """
{
  Get {
    Image (nearObject: {
      id: "%s"
    }) {
      filename
    }
  }
}
"""


def match_image(client, path):

    thing = {}
    thing['filename'] = path
    thing['image'] = weaviate.util.image_encoder_b64(path)
    newuuid = generate_uuid('Image', path)
    client.data_object.create(thing, 'Image', newuuid)

    print("importing", path)
    query = TEMPLATE % (newuuid)
    result = client.query.raw(query)
    if result is not None and 'data' in result and 'Get' in result['data'] and 'Image' in result['data']['Get']:
        for filename in result['data']['Get']['Image']:
            print("    -", filename)
