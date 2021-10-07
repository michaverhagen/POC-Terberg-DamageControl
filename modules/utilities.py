""" This modules contains general utility functions """

import os
import datetime
import uuid
import re
import weaviate
from weaviate import wcs


DEFAULT_WEAVIATE = 'http://localhost:8080'
DEFAULT_MAX_BATCH = 1000
DEFAULT_TYPES = ["string", "int", "number", "boolean", "text", "date"]

VERBOSE = False


def generate_uuid(classname, identifier):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, classname + identifier))


def remove_special_characters(text):
    """ This function cleans text from unwanted characters """
    cleartext = ""
    if text != "":
        cleartext = text.replace('\n', ' ')
        cleartext = cleartext.replace('_', ' ')
    return cleartext


def find_class_by_name(schema, classname):
    found = None
    for temp in schema['classes']:
        if temp['class'] == classname:
            found = temp
            break

    return found


def find_property_by_name(schema, name, classname):
    found = None
    for temp in schema['classes']:
        if temp['class'] == classname:
            for prop in temp['properties']:
                if prop['name'] == name:
                    found = prop
                    break
        if found is not None:
            break

    return found


def find_property_by_column(schema, column, classname):
    found = None
    for temp in schema['classes']:
        if temp['class'] == classname:
            for prop in temp['properties']:
                if prop['description'] == column:
                    found = prop
                    break
        if found is not None:
            break

    return found


def check_batch_result(results: dict):
    """
    checks the outcome of a batch request to Weaviate
    Parameters
    ----------
    results: dict
        A dict that contains the outcome of a batch request
    """

    errorcount = 0
    if results is not None:
        for result in results:
            if 'result' in result and 'errors' in result['result']:
                if 'error' in result['result']['errors']:
                    for message in result['result']['errors']['error']:
                        errorcount += 1
                        #print(message['message'])
    return errorcount


def load_schema(client, config):
    """
    loads the schema into Weaviate
    Parameters
    ----------
    client: weaviate.client
        The weaviate client
    config: dict
        A dict that contains the parameters
    """

    path = "./schema/schema.json"
    if 'schema' in config['weaviate']:
        path = config['weaviate']['schema']

    if client.schema.contains():
        client.schema.delete_all()
    client.schema.create(path)


def get_weaviate_client(instance: dict) -> weaviate.client:
    """
    Gets the Weaviate client
    Parameters
    ----------
    instance: weaviate.client
        The weaviate client
    Returns
    -------
    client: weaviate.client
        the Weaviate client
    """

    if instance is None:
        return None

    auth = username = password = client = None
    if 'username' in instance and 'password' in instance:
        username = os.getenv(instance['username'])
        password = os.getenv(instance['password'])
        if username is not None and password is not None:
            auth = weaviate.AuthClientPassword(username, password)

    if 'url' in instance:
        if auth is not None:
            client = weaviate.Client(instance['url'], auth_client_secret=auth)
        else:
            client = weaviate.Client(instance['url'])

    elif 'wcs' in instance:
        if auth is not None:
            my_wcs = WCS(auth)
            try:
                result = my_wcs.get_cluster_config(instance['wcs'])
                weaviatepath = 'https://'+result['meta']['PublicURL']
            except:
                config = {}
                config['id'] = instance['wcs']
                config['configuration'] = {}
                config['configuration']['requiresAuthentication'] = True
                config['configuration']['tier'] = "sandbox"
                weaviatepath = my_wcs.create(config=config)
            client = weaviate.Client(weaviatepath, auth_client_secret=auth)

    else:
        client = weaviate.Client(DEFAULT_WEAVIATE)

    return client
