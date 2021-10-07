#!/usr/bin/env python3
""" load Intake reports data """

import time
import yaml
from modules.match import match_image
from modules.utilities import get_weaviate_client


NEW_IMAGE = "./data/images/dent.jpg"


def _match_image():
    """ load the data """

    with open('./config.yml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        client = get_weaviate_client(config['weaviate'])
        match_image(client, NEW_IMAGE)



#########################################################################################################
# only the call for the main function below this line
#########################################################################################################


def main():
    """ main """
    start = time.time()

    _match_image()

    end = time.time()
    minutes = round((end-start)/60)
    print("Total time required ------------------------:", minutes, "minutes", round((end-start)%60, 1), "seconds")


if __name__ == '__main__':
    main()
