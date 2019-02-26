from __future__ import division
import os
import pandas
import math
import io, json
import id_generator

def compute_metrics(input_dir, gold_standard, cancer_type, all_cancer_genes):

    participants_datasets = {}

    # print os.listdir(input_dir + "participants/")
    for participant in os.listdir(input_dir + "participants/"):
        # print participant
        if os.path.isfile(input_dir + "participants/" + participant + "/" + cancer_type + ".txt") == False:
            # print "#################no data", cancer_type
            participants_datasets[participant] = [0,0]
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

        all_cancer_genes[participant] = list(set().union(predicted_genes, all_cancer_genes[participant]))

        # TRUE POSITIVE RATE
        overlapping_genes = set(predicted_genes).intersection(gold_standard)
        TPR = len(overlapping_genes)/len(gold_standard)

        #ACCURACY/ PRECISION
        if len(predicted_genes) == 0:
            acc = 0
        else:
            acc = len(overlapping_genes) / len(predicted_genes)

        participants_datasets[participant] = [TPR, acc]

    return participants_datasets, all_cancer_genes

def run(cancer_types, long_names, mongo_tool_ids, mongo_datRef_ids):

    ## create dict that will store info about all combined cancer types
    all_cancer_genes = {}
    for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):
        all_cancer_genes[participant] = []

    last_challenge = "0000000"
    last_event = "000007S"
    last_participant_dataset = "0000000"
    last_ref_dataset = "000007S"
    last_tool = "0000008"
    last_assessment_dataset = "000008R"

    IDGenerator = id_generator.IDGenerator()

    for cancer in cancer_types:

        challenge_id, last_challenge = IDGenerator.get_new_OEB_id("002", "X", last_challenge)

        # get metrics reference dataset id - incoming
        ref_data_id, last_ref_dataset = IDGenerator.get_new_OEB_id("002", "D", last_ref_dataset)


        data = pandas.read_csv("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/"+ cancer + ".txt",
                               comment="#", header=None)
        gold_standard = data.iloc[:, 0].values

        participants_datasets, all_cancer_genes = compute_metrics("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/", gold_standard, cancer, all_cancer_genes)

        for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):

            # if participant is not in mongo, asign new temporary id
            if participant in mongo_tool_ids:
                tool_id = mongo_tool_ids[participant]
            else:
                tool_id, last_tool = IDGenerator.get_new_OEB_id("002", "T", last_tool)

            # get participant dataset id - incoming
            participant_data_id, last_participant_dataset = IDGenerator.get_new_OEB_id("002", "D", last_participant_dataset)

            #get data-uri value of the 2 metrics
            metric1 = participants_datasets[participant][0]
            metric2 = participants_datasets[participant][1]

            #print metrics1 assesment file

            # get assessment dataset id for metric 1
            A_data_id, last_assessment_dataset = IDGenerator.get_new_OEB_id("002", "D", last_assessment_dataset)

            info = {
                "_id":A_data_id,
               "orig_id":"TCGA:2018-04-05_" + cancer + "_A_TPR_" + participant,
               "description":"Assessment dataset for applying Metric 'True Positive Rate' to " + participant + " predictions in " + long_names[cancer],
               "dates":{
                  "creation":"2018-04-05T00:00:00Z",
                  "modification":"2018-04-05T14:00:00Z"
               },
               "type":"assessment",
               "datalink":{
                  "uri": { "inline_data": {"value": metric1}},
                  "attrs":["inline"],
                  "status":"ok",
                  "validation_date":"2018-04-05T00:00:00Z"
               },
               "depends_on":{
                  "tool_id":tool_id,
                  "metrics_id":"OEBM0020000002",
                  "rel_dataset_ids":[
                     {
                        "dataset_id":participant_data_id,
                     },
                     {
                        "dataset_id":ref_data_id,
                     }
                  ]
               },
               "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Dataset",
               "community_id":"OEBC002",
               "challenge_id": [challenge_id],
               "version":"1",
               "name":"Assesment of Metric TPR in " + participant,
               "dataset_contact_ids":[
                  "Matthew.Bailey",
                  "Eduard.Porta",
                  "Collin.Tokheim"
               ]
            }

            # print info
            filename = "Dataset_assessment_" + cancer + "_" + participant + "_TPR_" + A_data_id + ".json"
            print filename

            with open("out/" + filename, 'w') as f:
                json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

            # print metrics2 assessment file

            # get assessment dataset id for metric 2
            A_data_id, last_assessment_dataset = IDGenerator.get_new_OEB_id("002", "D", last_assessment_dataset)

            info = {

                "_id": A_data_id,
                "orig_id": "TCGA:2018-04-05_" + cancer + "_A_precision_" + participant,
                "description": "Assessment dataset for applying Metric 'Positive Predictive Value' to " + participant + " predictions in " +
                               long_names[cancer],
                "dates": {
                    "creation": "2018-04-05T00:00:00Z",
                    "modification": "2018-04-05T14:00:00Z"
                },
                "type": "assessment",
                "datalink": {
                    "uri": { "inline_data": {"value": metric2}},
                    "attrs":["inline"],
                    "status": "ok",
                    "validation_date": "2018-04-05T00:00:00Z"
                },
                "depends_on": {
                    "tool_id": tool_id,
                    "metrics_id": "OEBM0020000001",
                    "rel_dataset_ids":[
                     {
                        "dataset_id":participant_data_id,
                     },
                     {
                        "dataset_id":ref_data_id,
                     }
                  ]
                },
                "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Dataset",
                "community_id": "OEBC002",
                "challenge_id": [challenge_id],
                "version": "1",
                "name": "Assesment of Metric precision-PPV in " + participant,
                "dataset_contact_ids": [
                    "Matthew.Bailey",
                    "Eduard.Porta",
                    "Collin.Tokheim"
                ]
            }

            # print info
            filename = "Dataset_assessment_" + cancer + "_" + participant + "_precision_" + A_data_id + ".json"
            print filename

            with open("out/" + filename, 'w') as f:
                json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))


    get_metrics_across_all_cancers(all_cancer_genes, last_assessment_dataset, last_participant_dataset, last_tool)


def get_metrics_across_all_cancers(all_cancer_genes, last_assessment_dataset, last_participant_dataset, last_tool):


    # plot chart for results across all cancer types

    IDGenerator = id_generator.IDGenerator()

    data = pandas.read_csv("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/ALL.txt",
                               comment="#", header=None)
    gold_standard = data.iloc[:, 0].values

    cancer = "ALL"
    challenge_id = "OEBX002t00000Z"
    ref_data_id = "OEBD002t00008R"

    participants_datasets = {}
    for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):

        #get set of predicted genes store in all_cancer_genes
        predicted_genes = all_cancer_genes[participant]
        # TRUE POSITIVE RATE
        overlapping_genes = set(predicted_genes).intersection(gold_standard)
        TPR = len(overlapping_genes) / len(gold_standard)

        # ACCURACY/ PRECISION
        if len(predicted_genes) == 0:
            acc = 0
        else:
            acc = len(overlapping_genes) / len(predicted_genes)

        participants_datasets[participant] = [TPR, acc]

        # if participant is not in mongo, asign new temporary id
        if participant in mongo_tool_ids:
            tool_id = mongo_tool_ids[participant]
        else:
            tool_id, last_tool = IDGenerator.get_new_OEB_id("002", "T", last_tool)

        # get participant dataset id - incoming
        participant_data_id, last_participant_dataset = IDGenerator.get_new_OEB_id("002", "D", last_participant_dataset)

        # get data-uri value of the 2 metrics
        metric1 = participants_datasets[participant][0]
        metric2 = participants_datasets[participant][1]

        # print metrics1 assesment file

        # get assessment dataset id for metric 1
        A_data_id, last_assessment_dataset = IDGenerator.get_new_OEB_id("002", "D", last_assessment_dataset)

        info = {
            "_id": A_data_id,
            "orig_id": "TCGA:2018-04-05_" + cancer + "_A_TPR_" + participant,
            "description": "Assessment dataset for applying Metric 'True Positive Rate' to " + participant + " predictions in " +
                           long_names[cancer],
            "dates": {
                "creation": "2018-04-05T00:00:00Z",
                "modification": "2018-04-05T14:00:00Z"
            },
            "type": "assessment",
            "datalink": {
                "uri": {"inline_data": {"value": metric1}},
                "attrs": ["inline"],
                "status": "ok",
                "validation_date": "2018-04-05T00:00:00Z"
            },
            "depends_on": {
                "tool_id": tool_id,
                "metrics_id": "OEBM0020000002",
                "rel_dataset_ids": [
                    {
                        "dataset_id": participant_data_id,
                    },
                    {
                        "dataset_id": ref_data_id,
                    }
                ]
            },
            "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Dataset",
            "community_id": "OEBC002",
            "challenge_id": [challenge_id],
            "version": "1",
            "name": "Assesment of Metric TPR in " + participant,
            "dataset_contact_ids": [
                "Matthew.Bailey",
                "Eduard.Porta",
                "Collin.Tokheim"
            ]
        }

        # print info
        filename = "Dataset_assessment_" + cancer + "_" + participant + "_TPR_" + A_data_id + ".json"
        print filename

        with open("out/" + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

        # print metrics2 assessment file

        # get assessment dataset id for metric 2
        A_data_id, last_assessment_dataset = IDGenerator.get_new_OEB_id("002", "D", last_assessment_dataset)

        info = {

            "_id": A_data_id,
            "orig_id": "TCGA:2018-04-05_" + cancer + "_A_precision_" + participant,
            "description": "Assessment dataset for applying Metric 'Positive Predictive Value' to " + participant + " predictions in " +
                           long_names[cancer],
            "dates": {
                "creation": "2018-04-05T00:00:00Z",
                "modification": "2018-04-05T14:00:00Z"
            },
            "type": "assessment",
            "datalink": {
                "uri": {"inline_data": {"value": metric2}},
                "attrs": ["inline"],
                "status": "ok",
                "validation_date": "2018-04-05T00:00:00Z"
            },
            "depends_on": {
                "tool_id": tool_id,
                "metrics_id": "OEBM0020000001",
                "rel_dataset_ids": [
                    {
                        "dataset_id": participant_data_id,
                    },
                    {
                        "dataset_id": ref_data_id,
                    }
                ]
            },
            "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Dataset",
            "community_id": "OEBC002",
            "challenge_id": [challenge_id],
            "version": "1",
            "name": "Assesment of Metric precision-PPV in " + participant,
            "dataset_contact_ids": [
                "Matthew.Bailey",
                "Eduard.Porta",
                "Collin.Tokheim"
            ]
        }

        # print info
        filename = "Dataset_assessment_" + cancer + "_" + participant + "_precision_" + A_data_id + ".json"
        print filename

        with open("out/" + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))




if __name__ == "__main__":


    cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA", "GBM", "HNSC", "KICH", "KIRC",
                    "KIRP", "LAML", "LGG", "LIHC", "LUAD", "LUSC", "MESO", "OV", "PAAD", "PANCAN", "PCPG", "PRAD",
                    "READ", "SARC", "SKCM", "STAD", "TGCT", "THCA", "THYM", "UCEC", "UCS", "UVM"]

    data = pandas.read_csv("../cancer_names.tsv", sep="\t",
                           comment="#", header=None)

    long_names = {}
    for index, row in data.iterrows():
        long_names[row[0]] = row[1]

    #read file which containes tool ids already pushed to mongo
    with io.open("../mongo_tools_ids.txt", mode='r', encoding="utf-8") as f:
        mongo_tool_ids = json.load(f)

    # read file which containes dataset ids already pushed to mongo
    with io.open("../reference_datasets_mongo_ids.txt", mode='r', encoding="utf-8") as f:
        mongo_datRef_ids = json.load(f)


    run(cancer_types, long_names, mongo_tool_ids, mongo_datRef_ids)