import os
import io, json


cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA"]

for cancer in cancer_types:

    datasets = [
                    {
                        "dataset_id": "TCGA:2018-04-05_" + cancer + "_I",
                        "role": "input"
                    },
                    {
                        "dataset_id": "TCGA:2018-04-05_" + cancer + "_M",
                        "role": "metrics_reference"
                    },
               ]

    for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):

        datasets.append({
                    "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_TPR_" + participant,
                    "role": "assessment"
                })

        datasets.append({
                    "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_precision_" + participant,
                    "role": "assessment"
                })

    datasets.append({
                        "dataset_id": "TCGA:2018-04-05_" + cancer + "_Summary",
                        "role": "challenge"
                    })
    info = {

        "_id": "TCGA:2018-04-05_" + cancer + "_do_summary",
        "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4#TestAction",
        "action_type": "StatisticsEvent",
        "received_datasets": datasets,
        "challenge_id": "TCGA:" + cancer + "_2018-04-05",
        "dates":{
           "creation": "2018-04-05T00:00:00Z",
           "reception": "2018-04-05T00:00:00Z"
        },
        "test_contact_ids": [
            "Matthew.Bailey",
            "Eduard.Porta",
            "Collin.Tokheim"
        ],
        "metadata":[
           {
              "target":"",
              "description":""
           }
        ]
    }

    # print info
    filename = "StatisticsEvent_" + cancer + ".json"
    # print filename

    with open("out/" + filename, 'w') as f:
        json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))
