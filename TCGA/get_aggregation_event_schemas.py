import os
import io, json
import id_generator
import pandas


def run (cancer_types):

    last_challenge = "0000000"
    last_event = "00000NC"
    last_tool = "0000008"
    last_assessment_dataset = "000008R"
    last_challenge_dataset = "00000OB"

    IDGenerator = id_generator.IDGenerator()

    for cancer in cancer_types:

        challenge_id, last_challenge = IDGenerator.get_new_OEB_id("002", "X", last_challenge)
        # get stat event id
        Sevent_id, last_event = IDGenerator.get_new_OEB_id("002", "A", last_event)

        #generate array with all incoming assessment datasets aun aoutgoing aggregation dataset
        involved_datasets = []

        for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):

            involved_datasets.append({
                "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_TPR_" + participant,
                "role": "incoming"
            })

            involved_datasets.append({
                "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_precision_" + participant,
                "role": "incoming"
            })
        # append test action outgoing dataset
        involved_datasets.append({
            "dataset_id": "TCGA:2018-04-05_" + cancer + "_Aggregation",
            "role": "outgoing"
        })



        info = {

            "_id": "TCGA:2018-04-05_" + cancer + "_do_aggregation",
            "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/TestAction",
            "tool_id": "TCGA:aggregate_benchmark",
            "action_type": "AggregationEvent",
            "involved_datasets": involved_datasets,
            "challenge_id": "TCGA:2018-04-05_" + cancer,
            "dates":{
               "creation": "2018-04-05T00:00:00Z",
               "reception": "2018-04-05T00:00:00Z"
            },
            "test_contact_ids": [
                "Matthew.Bailey",
                "Eduard.Porta",
                "Collin.Tokheim"
            ]
        }

        # print info
        filename = "AggregationEvent_" + cancer + "_" + Sevent_id + ".json"
        # print filename

        with open("out/" + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":


    cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA", "GBM", "HNSC", "KICH", "KIRC",
                    "KIRP", "LAML", "LGG", "LIHC", "LUAD", "LUSC", "MESO", "OV", "PAAD", "PCPG", "PRAD",
                    "READ", "SARC", "SKCM", "STAD", "TGCT", "THCA", "THYM", "UCEC", "UCS", "UVM", "ALL"]

    data = pandas.read_csv("../cancer_names.tsv", sep="\t",
                           comment="#", header=None)


    # read file which containes tool ids already pushed to mongo
    with io.open("../mongo_tools_ids.txt", mode='r', encoding="utf-8") as f:
        mongo_ids = json.load(f)


    run(cancer_types)