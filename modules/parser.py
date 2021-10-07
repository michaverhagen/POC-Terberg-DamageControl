""" This module parses datapoints from an different file types """

import os
import json
import zipfile

from modules.utilities import generate_uuid
from modules.utilities import remove_special_characters
from modules.utilities import find_class_by_name
from modules.utilities import find_property_by_column
from modules.utilities import DEFAULT_TYPES


def _debug_print(data):
    #print(data['types'])
    #print(data['additionalTypes'])
    #print("REF_COUNT:", REF_COUNT)
    pass


def _parse_report(report, data):

    added = False
    if report is not None and 'vId' in report:
        if 'damages' in report and len(report['damages']) > 0:
            added = True
            newreport = {}
            newreport['vId'] = report['vId']
            newreport['licensePlate'] = report['licensePlate']
            data['reports'].append(newreport)

            for damage in report['damages']:
                newdamage = {}
                newdamage['reportId'] = report['vId']
                if 'damageId' in damage:
                    newdamage['damageId'] = damage['damageId']

                if 'damagedPart' in damage:
                    newdamage['damagePart'] = damage['damagedPart']

                if 'damageDescr' in damage:
                    newdamage['damageDescription'] = damage['damageDescr']

                if 'proposedSolution' in damage:
                    newdamage['proposwedSolution'] = damage['proposedSolution']

                if 'estimatedCost' in damage:
                    newdamage['estimatedCost'] = damage['estimatedCost']

                #if 'imagesOfDamage' in damage:
                    #newdamage['damagePart'] = damage['damagePart']

                data['damages'].append(newdamage)

    return added


def parse_data(config):
    data = {}
    data['reports'] = []
    data['damages'] = []

    max_reports = -1
    if 'max_reports' in config['data']:
        max_reports = config['data']['max_reports']

    if 'reports' in config['data']:
        file = open(config['data']['reports'])
        reportlist = json.load(file)

        added = count = 0
        for report in reportlist:
            count += 1
            if _parse_report(report, data):
                added += 1

            if max_reports > 0 and added > max_reports:
                break

        print("Reports processed --------------------------:", count-1)
        print("Reports added with damages -----------------:", added-1)

    _debug_print(data)

    return data
