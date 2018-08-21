import os
import io, json


cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA"]

for cancer in cancer_types:

    for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):

        #print metrics1 metricsevent file
        info = {

            "_id":"TCGA:2018-04-05_" + cancer + "_metricsEvent_" + participant + "_TPR",
            "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4#TestAction",
            "action_type":"MetricsEvent",
            "tool_id":"TCGA:" + participant,
            "metrics_id":"TCGA:TPR",
            "received_datasets":[
               {
                  "dataset_id":"TCGA:2018-04-05_" + cancer + "_M",
                  "role":"metrics_reference"
               },
               {
                  "dataset_id": "TCGA:2018-04-05_" + cancer + "_P_" + participant,
                    "role": "participant"
               },
               {
                  "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_TPR_" + participant,
                  "role":"assessment"
               }
            ],
            "challenge_id": "TCGA:2018-04-05_" + cancer,
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
        filename = "MetricsEvent_" + cancer + "_" + participant + "_TPR.json"
        # print filename

        with open("out/" + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

        # print metrics2 metricsevent file
        info = {

            "_id": "TCGA:2018-04-05_" + cancer + "_metricsEvent_" + participant + "_precision",
            "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4#TestAction",
            "action_type": "MetricsEvent",
            "tool_id": "TCGA:" + participant,
            "metrics_id": "TCGA:PPV",
            "received_datasets": [
                {
                    "dataset_id": "TCGA:2018-04-05_" + cancer + "_M",
                    "role": "metrics_reference"
                },
                {
                    "dataset_id": "TCGA:2018-04-05_" + cancer + "_P_" + participant,
                    "role": "participant"
                },
                {
                    "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_precision_" + participant,
                    "role": "assessment"
                }
            ],
            "challenge_id": "TCGA:2018-04-05_" + cancer,
            "dates": {
                "creation": "2018-04-05T00:00:00Z",
                "reception": "2018-04-05T00:00:00Z"
            },
            "test_contact_ids": [
                "Matthew.Bailey",
                "Eduard.Porta",
                "Collin.Tokheim"
            ],
            "metadata": [
                {
                    "target": "",
                    "description": ""
                }
            ]
        }

        # print info
        filename = "MetricsEvent_" + cancer + "_" + participant + "_precision.json"
        # print filename

        with open("out/" + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))
