""" This module parses ex-factory excel file from PVM """

import os
import uuid
import weaviate
import time
import base64
from modules.utilities import generate_uuid
from modules.utilities import check_batch_result
from modules.utilities import DEFAULT_TYPES
from modules.utilities import VERBOSE

DEFAULT_MAX_BATCH = 1000


def _import_reports(instance: dict, client: weaviate.client, reports: list):

    maxbatch = DEFAULT_MAX_BATCH
    if instance is not None and 'max_batch_size' in instance:
        maxbatch = instance['max_batch_size']

    errorcount = totalcount = batchcount = 0
    client.batch.shape
    for report in reports:
        newuuid = generate_uuid('Report', report['vId'])
        client.batch.add_data_object(report, 'Report', report['vId'])
        batchcount += 1
        totalcount += 1
        if batchcount >= maxbatch:
            result = client.batch.create_objects()
            errorcount += check_batch_result(result)
            print("Reports imported in Weaviate ---------------:", totalcount, "errors:", errorcount, end='\r')
            client.batch.shape
            batchcount = 0

    if batchcount > 0:
        result = client.batch.create_objects()
        errorcount += check_batch_result(result)
    print("Reports imported in Weaviate ---------------:", totalcount, "errors:", errorcount)


def _import_damages(instance: dict, client: weaviate.client, damages: list):

    maxbatch = DEFAULT_MAX_BATCH
    if instance is not None and 'max_batch_size' in instance:
        maxbatch = instance['max_batch_size']

    errorcount = totalcount = batchcount = 0
    for damage in damages:
        newuuid = generate_uuid('Damage', damage['reportId']+str(damage['damageId']))
        client.batch.add_data_object(damage, 'Damage', newuuid)
        batchcount += 1
        totalcount += 1
        if batchcount >= maxbatch:
            print("Damages imported in Weaviate ---------------:", totalcount, 'errors:', errorcount, end='\r')
            result = client.batch.create_objects()
            errorcount += check_batch_result(result)
            client.batch.shape
            batchcount = 0

    if batchcount > 0:
        result = client.batch.create_objects()
        errorcount += check_batch_result(result)

    print("Damages imported in Weaviate ---------------:", totalcount, 'errors:', errorcount)


def _import_images(instance: dict, client: weaviate.client, images: list):

    maxbatch = DEFAULT_MAX_BATCH
    if instance is not None and 'max_batch_size' in instance:
        maxbatch = instance['max_batch_size']

    errorcount = totalcount = batchcount = 0
    for image in images:
        thing = {}
        thing['filename'] = image['filename']
        thing['image'] = weaviate.util.image_encoder_b64("./data/images/dent.jpg")
        #thing['image'] = weaviate.util.image_encoder_b64(image['filename'])

        newuuid = generate_uuid('Image', image['filename'])
        client.batch.add_data_object(thing, 'Image', newuuid)
        batchcount += 1
        totalcount += 1
        if batchcount >= maxbatch:
            print("Images imported in Weaviate ----------------:", totalcount, 'errors:', errorcount, end='\r')
            result = client.batch.create_objects()
            errorcount += check_batch_result(result)
            client.batch.shape
            batchcount = 0

    if batchcount > 0:
        result = client.batch.create_objects()
        errorcount += check_batch_result(result)

    print("Images imported in Weaviate ----------------:", totalcount, 'errors:', errorcount)


def _crossref_damages(instance: dict, client: weaviate.client, damages: list):

    maxbatch = DEFAULT_MAX_BATCH
    if instance is not None and 'max_batch_size' in instance:
        maxbatch = instance['max_batch_size']

    client.batch.shape
    errorcount = totalcount = batchcount = 0
    for damage in damages:
        ruuid = damage['reportId']
        duuid = generate_uuid('Damage', damage['reportId']+str(damage['damageId']))
        client.batch.add_reference(duuid, 'Damage', "ofReport", ruuid)
        client.batch.add_reference(ruuid, 'Report', "hasDamages", duuid)
        totalcount += 2
        batchcount += 2
        if batchcount >= maxbatch:
            print("Damages cross reference --------------------:", totalcount, end='\r')
            result = client.batch.create_references()
            client.batch.shape
            batchcount = 0
    if batchcount > 0:
        result = client.batch.create_references()
    print("Damages cross reference --------------------:", totalcount)


def _crossref_images(instance: dict, client: weaviate.client, images: list):

    maxbatch = DEFAULT_MAX_BATCH
    if instance is not None and 'max_batch_size' in instance:
        maxbatch = instance['max_batch_size']

    client.batch.shape
    errorcount = totalcount = batchcount = 0
    for image in images:
        iuuid = generate_uuid('Image', image['filename'])
        duuid = generate_uuid('Damage', image['ofDamage'])
        client.batch.add_reference(iuuid, 'Image', "ofDamage", duuid)
        client.batch.add_reference(duuid, 'Damage', "hasImages", iuuid)
        totalcount += 2
        batchcount += 2
        if batchcount >= maxbatch:
            print("Damages cross reference --------------------:", totalcount, end='\r')
            result = client.batch.create_references()
            client.batch.shape
            batchcount = 0
    if batchcount > 0:
        result = client.batch.create_references()
    print("Damages cross reference --------------------:", totalcount)


def import_data(config: dict, client: weaviate.client, data: dict):

    instance = config['weaviate']

    _import_reports(instance, client, data['reports'])
    _import_damages(instance, client, data['damages'])
    _import_images(instance, client, data['images'])
    _crossref_damages(instance, client, data['damages'])
    _crossref_images(instance, client, data['images'])
