import os
import io, json
import pandas

cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA"]


data = pandas.read_csv("../cancer_names.tsv", sep="\t",
                           comment="#", header=None)

long_names = {}
for index, row in data.iterrows():
    long_names[row[0]] = row[1]

for cancer in cancer_types:

    info = {
        "_id":"TCGA:2018-04-05_" + cancer + "_M",
        "datalink":{
           "uri":"https://portal.gdc.cancer.gov/",
           "attrs":["archive"],
           "validation_date":"2018-04-05T00:00:00Z",
           "status":"ok"
        },
        "type":"metrics_reference",
        "version":"unknown",
        "name":"Metrics Reference Dataset for " + long_names[cancer],
        "description":"List of genes (described by TCGA community) that can be used as 'gold standard' in " + long_names[cancer] + " benchmark ",
        "dates":{
           "creation":"2018-04-05T00:00:00Z",
           "modification":"2018-04-05T14:00:00Z"
        },
        "depends_on":{
           "rel_dataset_ids":[
              {
                 "dataset_id":"TCGA:2018-04-05_" + cancer + "_I",
              }
           ]
        },
        "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/Dataset",
        "community_id":"TCGA",
        "dataset_contact_ids":[
           "Matthew.Bailey",
           "Eduard.Porta",
           "Collin.Tokheim"
        ]
    }

    # print info
    filename = "Dataset_Metrics_Ref_" + cancer + ".json"
    # print filename

    with open("out/" + filename, 'w') as f:
        json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))
