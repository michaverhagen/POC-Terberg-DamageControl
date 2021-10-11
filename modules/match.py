""" This module contains general query functions """

import weaviate
from modules.utilities import get_weaviate_client
from modules.utilities import generate_uuid


NEAR_IMAGE = """
{
  Get {
    Image (nearImage: {
      image: "%s"
    }) {
      filename
    }
  }
}
"""


NEAR_OBJECT = """
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


def _match_image_nearObject(client, path):

    thing = {}
    thing['filename'] = path
    thing['image'] = weaviate.util.image_encoder_b64(path)
    newuuid = generate_uuid('Image', path)
    client.data_object.create(thing, 'Image', newuuid)

    print("importing", path)
    query = NEAR_OBJECT % (newuuid)
    result = client.query.raw(query)
    if result is not None and 'data' in result and 'Get' in result['data'] and 'Image' in result['data']['Get']:
        for filename in result['data']['Get']['Image']:
            print("    -", filename)


def _match_image_nearImage(client, path):

    encoded_image = weaviate.util.image_encoder_b64(path)
    query = NEAR_IMAGE % (encoded_image)
    result = client.query.raw(query)
    if result is not None and 'data' in result and 'Get' in result['data'] and 'Image' in result['data']['Get']:
        for filename in result['data']['Get']['Image']:
            print("    -", filename)


def match_image(config, path):

    client = get_weaviate_client(config['weaviate'])

    search = 'nearImage'
    if 'data' in config and 'search' in config['data']:
        search = config['data']['search']

    if search == 'nearImage':
        print("Matching images using nearImage ------------:", path)
        _match_image_nearImage(client, path)
    elif search == 'nearObject':
        print("Matching images using nearObject -----------:", path)
        _match_image_nearObject(client, path)
