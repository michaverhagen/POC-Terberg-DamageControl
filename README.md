# POC-Terberg-DamageControl
Proof of concept for Terberg - intake damage control
- `./data/reports/` this directory contains the dagame reports files
- `./data/data_configuration.xlsx` is the file that is used to generate the schema. Note that the schema is generated at every run (!), so manually overwriting the schema in the `./schema/schema.json` does not work!

### Install the dependencies
```
pip install -r requirements.txt
```

### Spin up the Weaviate instance of your choice
There currently is are two docker files in the `./docker/` directory, spin up the docker of your choice:

```
$ docker-compose -f ./docker/docker-c11y.yml up
# or
$ docker-compose -f ./docker/docker-images.yml up
```

Make sure the `config.yml` file in the home directory points to the right vectorizer (lines 4 and 5):
```
  1 weaviate:
  2     url: 'http://localhost:8080'
  3     schema: './schema/schema.json'
  4     #module_name: 'text2vec-transformers'
  5     module_name: 'text2vec-contextionary'
  6     username: "WEAVIATE_USERNAME"
  7     password: "WEAVIATE_PASSWORD"
  8     debug: False
  9     verbose: True
 10     delay: 2.0
 11     max_batch_size: 100
 12
 13 data:
 14     config: './data/data_configuration.xlsx'
 15     reports: './data/reports/'   # must be a directory
 16     search: "nearImage"
 17     #search: "nearObject"
 18     #max_reports: -1
 19     max_reports: 2

```

### Load the data
```
$ ./loaddata.py
```

### Find the match
```
$ ./match.py
```
