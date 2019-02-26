import os
import io, json
import pandas
import id_generator


def run(cancer_types, long_names, mongo_tool_ids):

    last_challenge = "0000000"
    last_tool = "0000008"
    last_assessment_dataset = "000008R"
    last_challenge_dataset = "00000OB"
    last_ref_dataset = "000007S"

    IDGenerator = id_generator.IDGenerator()

    for cancer in cancer_types:

        challenge_id, last_challenge = IDGenerator.get_new_OEB_id("002", "X", last_challenge)

        # get metrics reference dataset id - incoming
        ref_data_id, last_ref_dataset = IDGenerator.get_new_OEB_id("002", "D", last_ref_dataset)

        for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):

            # if participant is not in mongo, asign new temporary id
            if participant in mongo_tool_ids:
                tool_id = mongo_tool_ids[participant]
            else:
                tool_id, last_tool = IDGenerator.get_new_OEB_id("002", "T", last_tool)

            # get assessment dataset id for metric 1
            A_data_id_TPR, last_assessment_dataset = IDGenerator.get_new_OEB_id("002", "D", last_assessment_dataset)
            # get assessment dataset id for metric 2
            A_data_id_precision, last_assessment_dataset = IDGenerator.get_new_OEB_id("002", "D", last_assessment_dataset)

            # get challenge dataset_id
            challenge_data_id, last_challenge_dataset = IDGenerator.get_new_OEB_id("002", "D", last_challenge_dataset)

            # read files which containes metrics values
            with io.open("out/Dataset_assessment_" + cancer + "_" + participant + "_TPR_" + A_data_id_TPR + ".json", mode='r', encoding="utf-8") as f:
                assess_file = json.load(f)
                metric1 = assess_file["datalink"]["uri"]["inline_data"]["value"]

            with io.open("out/Dataset_assessment_" + cancer + "_" + participant + "_precision_" + A_data_id_precision + ".json", mode='r', encoding="utf-8") as f:
                assess_file = json.load(f)
                metric2 = assess_file["datalink"]["uri"]["inline_data"]["value"]

            info = {

                "_id": challenge_data_id,
                "orig_id":"TCGA:2018-04-05_" + cancer + "_" + participant + "_Summary",
                "datalink":{
                   "uri": { "inline_data": {"metricX": metric1, "metricY": metric2}}
                },
                "type":"challenge",
                "version":"unknown",
                "name":"Summary dataset for challenge: " + long_names[cancer],
                "description":"Summary dataset with information about challenge " + long_names[cancer] + " (e.g. input/output datasets, metrics...) in participant " + participant,
                "dates":{
                   "creation":"2018-04-05T00:00:00Z",
                   "modification":"2018-04-05T14:00:00Z"
                },
                "depends_on":{
                    "tool_id": tool_id,
                   "rel_dataset_ids": [
                               {
                                   "dataset_id": "OEBD002000000L",
                               },
                               {
                                   "dataset_id": ref_data_id,
                               },
                                {
                                    "dataset_id": A_data_id_TPR,
                                },
                                {
                                    "dataset_id": A_data_id_precision,
                                }
                           ],
                },
                "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Dataset",
                "community_id":"OEBC002",
                "challenge_id": [challenge_id],
                "dataset_contact_ids":[
                   "Matthew.Bailey",
                    "Eduard.Porta",
                    "Collin.Tokheim"
                ]
            }

            # print info
            filename = "Dataset_Challenge_" + cancer + "_" + participant + "_" + challenge_data_id + ".json"
            # print filename

            with open("out/" + filename, 'w') as f:
                json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":


    cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA", "GBM", "HNSC", "KICH", "KIRC",
                    "KIRP", "LAML", "LGG", "LIHC", "LUAD", "LUSC", "MESO", "OV", "PAAD", "PANCAN", "PCPG", "PRAD",
                    "READ", "SARC", "SKCM", "STAD", "TGCT", "THCA", "THYM", "UCEC", "UCS", "UVM", "ALL"]

    data = pandas.read_csv("../cancer_names.tsv", sep="\t",
                           comment="#", header=None)

    long_names = {}
    for index, row in data.iterrows():
        long_names[row[0]] = row[1]

    #read file which containes tool ids already pushed to mongo
    with io.open("../mongo_tools_ids.txt", mode='r', encoding="utf-8") as f:
        mongo_tool_ids = json.load(f)


    run(cancer_types, long_names, mongo_tool_ids)