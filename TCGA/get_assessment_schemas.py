import os
import pandas
import math
from datauri import DataURI
import json

cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA"]


data = pandas.read_csv("../cancer_names.tsv", sep="\t",
                           comment="#", header=None)

long_names = {}
for index, row in data.iterrows():
    long_names[row[0]] = row[1]

def compute_metrics(input_dir, gold_standard, cancer_type):

    participants_datasets = {}

    for participant in os.listdir(input_dir + "participants/"):

        if os.path.isfile(input_dir + "participants/" + participant + "/" + cancer_type + ".txt") == False:

            continue
        data = pandas.read_csv(input_dir + "participants/" + participant + "/" + cancer_type + ".txt", sep='\t',
                               comment="#", header=0)

        #filter data by q-value
        if participant == "MutSig2CV":

            filtered_data = data.loc[data['qvalue'] <= 0.1]

            predicted_genes = filtered_data.iloc[:, 0].values

        elif participant == "ActiveDriver":

            filtered_data = data.loc[data['qvalue'] <= 0.0001]

            predicted_genes = filtered_data.iloc[:, 0].values

        elif participant == "MuSiC":

            filtered_data = data.loc[data['pvalue'] <= math.exp(-8)]
            filtered_data = filtered_data[filtered_data['info'] == "FILTER=PASS"]

            predicted_genes = filtered_data.iloc[:, 0].values

        else:

            filtered_data = data.loc[data['qvalue'] <= 0.05]

            predicted_genes = filtered_data.iloc[:, 0].values

        # predicted_genes = data.iloc[:, 0].values

        # TRUE POSITIVE RATE
        overlapping_genes = set(predicted_genes).intersection(gold_standard)
        TPR = len(overlapping_genes)/len(gold_standard)

        #ACCURACY/ PRECISION
        if len(predicted_genes) == 0:
            acc = 0
        else:
            acc = len(overlapping_genes) / len(predicted_genes)

        participants_datasets[participant] = [TPR, acc]

    return participants_datasets



for cancer in cancer_types:


    data = pandas.read_csv("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/"+ cancer + ".txt",
                           comment="#", header=None)
    gold_standard = data.iloc[:, 0].values

    participants_datasets = compute_metrics("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/", gold_standard, cancer)

    for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):

        #get data-uri value of the 2 metrics
        metric1 = DataURI.make('application/json', charset='us-ascii', base64=True, data=json.dumps(participants_datasets[participant][0]))
        metric2 = DataURI.make('application/json', charset='us-ascii', base64=True, data=json.dumps(participants_datasets[participant][1]))

        #print metrics1 assesment file
        info = {
           "_id":"TCGA:2018-04-05_" + cancer + "_A_TPR_" + participant,
           "description":"Assessment dataset for applying Metric 'True Positive Rate' to " + participant + " predictions in " + long_names[cancer],
           "dates":{
              "creation":"2018-04-05T00:00:00Z",
              "modification":"2018-04-05T14:00:00Z"
           },
           "type":"assessment",
           "datalink":{
              "uri":metric1,
              "attrs":["inline"],
              "status":"ok",
              "validation_date":"2018-04-05T00:00:00Z"
           },
           "depends_on":{
              "tool_id":"TCGA:" + participant,
              "metrics_id":"TCGA:TPR",
              "rel_dataset_ids":[
                 {
                    "dataset_id":"TCGA:2018-04-05_" + cancer + "_I",
                 },
                 {
                    "dataset_id":"TCGA:2018-04-05_" + cancer + "_M",
                 }
              ]
           },
           "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/Dataset",
           "community_id":"TCGA",
           "version":"1",
           "name":"Assesment of Metric TPR in " + participant,
           "dataset_contact_ids":[
              "Matthew.Bailey",
              "Eduard.Porta",
              "Collin.Tokheim"
           ]
        }

        # print info
        filename = "Dataset_assessment_" + cancer + "_" + participant + "_TPR.json"
        # print filename

        with open("out/" + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

        # print metrics2 assessment file
        info = {
            "_id": "TCGA:2018-04-05_" + cancer + "_A_precision_" + participant,
            "description": "Assessment dataset for applying Metric 'Positive Predictive Value' to " + participant + " predictions in " +
                           long_names[cancer],
            "dates": {
                "creation": "2018-04-05T00:00:00Z",
                "modification": "2018-04-05T14:00:00Z"
            },
            "type": "assessment",
            "datalink": {
                "uri": metric2,
                "attrs":["inline"],
                "status": "ok",
                "validation_date": "2018-04-05T00:00:00Z"
            },
            "depends_on": {
                "tool_id": "TCGA:" + participant,
                "metrics_id": "TCGA:PPV",
                "rel_dataset_ids": [
                    {
                        "dataset_id": "TCGA:2018-04-05_" + cancer + "_I",
                    },
                    {
                        "dataset_id": "TCGA:2018-04-05_" + cancer + "_M",
                    }
                ]
            },
            "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/Dataset",
            "community_id": "TCGA",
            "version": "1",
            "name": "Assesment of Metric precision-PPV in " + participant,
            "dataset_contact_ids": [
                "Matthew.Bailey",
                "Eduard.Porta",
                "Collin.Tokheim"
            ]
        }

        # print info
        filename = "Dataset_assessment_" + cancer + "_" + participant + "_precision.json"
        # print filename

        with open("out/" + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))
