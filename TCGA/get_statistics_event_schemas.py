import os
import io, json
import id_generator
import pandas


def run (cancer_types, mongo_tool_ids):

    last_challenge = "0000000"
    last_event = "00000NC"
    last_tool = "0000008"
    last_assessment_dataset = "000008R"
    last_challenge_dataset = "00000OB"

    IDGenerator = id_generator.IDGenerator()

    for cancer in cancer_types:

        challenge_id, last_challenge = IDGenerator.get_new_OEB_id("002", "X", last_challenge)

        for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):

            # if participant is not in mongo, asign new temporary id
            if participant in mongo_tool_ids:
                tool_id = mongo_tool_ids[participant]
            else:
                tool_id, last_tool = IDGenerator.get_new_OEB_id("002", "T", last_tool)

            # get stat event id
            Sevent_id, last_event = IDGenerator.get_new_OEB_id("002", "A", last_event)

            # get assessment dataset id for metric 1
            A_data_id_TPR, last_assessment_dataset = IDGenerator.get_new_OEB_id("002", "D", last_assessment_dataset)
            # get assessment dataset id for metric 2
            A_data_id_precision, last_assessment_dataset = IDGenerator.get_new_OEB_id("002", "D", last_assessment_dataset)

            #get outgoing dataset_id
            challenge_data_id, last_challenge_dataset = IDGenerator.get_new_OEB_id("002", "D", last_challenge_dataset)

            info = {

                "_id":Sevent_id,
                "orig_id": "TCGA:2018-04-05_" + cancer + "_" + participant + "_do_summary",
                "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/TestAction",
                "tool_id": tool_id,
                "action_type": "StatisticsEvent",
                "involved_datasets": [

                            {
                                "dataset_id": A_data_id_TPR,
                                "role": "incoming"
                            },
                            {
                                "dataset_id": A_data_id_precision,
                                "role": "incoming"
                            },
                            {
                                "dataset_id": challenge_data_id,
                                "role": "outgoing"
                            }
                       ],
                "challenge_id": challenge_id,
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
            filename = "StatisticsEvent_" + cancer + "_" + participant + "_" + Sevent_id + ".json"
            # print filename

            with open("out/" + filename, 'w') as f:
                json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":


    cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA", "GBM", "HNSC", "KICH", "KIRC",
                    "KIRP", "LAML", "LGG", "LIHC", "LUAD", "LUSC", "MESO", "OV", "PAAD", "PANCAN", "PCPG", "PRAD",
                    "READ", "SARC", "SKCM", "STAD", "TGCT", "THCA", "THYM", "UCEC", "UCS", "UVM", "ALL"]

    data = pandas.read_csv("../cancer_names.tsv", sep="\t",
                           comment="#", header=None)


    # read file which containes tool ids already pushed to mongo
    with io.open("../mongo_tools_ids.txt", mode='r', encoding="utf-8") as f:
        mongo_ids = json.load(f)

    # read file which contains download links with participant predictions
    with io.open("../participant_data_urls.txt", mode='r', encoding="utf-8") as f:
        download_urls = json.load(f)

    run(cancer_types, mongo_ids)