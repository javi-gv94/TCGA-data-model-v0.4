import os
import io, json
import id_generator


def run(cancer_types, mongo_tool_ids, mongo_datRef_ids, out_dir):

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

        for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):

            # if participant is not in mongo, asign new temporary id
            if participant in mongo_tool_ids:
                tool_id = mongo_tool_ids[participant]
            else:
                tool_id, last_tool = IDGenerator.get_new_OEB_id("002", "T", last_tool)


            # get participant dataset id - incoming
            participant_data_id, last_participant_dataset = IDGenerator.get_new_OEB_id("002", "D",
                                                                                       last_participant_dataset)


            #print metrics1 metricsevent file

            # get metrics 1 event id
            Mevent_id, last_event = IDGenerator.get_new_OEB_id("002", "A", last_event)

            # get metrics1 assessment dataset id - outgoing
            A_data_id, last_assessment_dataset = IDGenerator.get_new_OEB_id("002", "D", last_assessment_dataset)

            info = {

                "_id": "TCGA:2018-04-05_" + cancer + "_metricsEvent_" + participant + "_TPR",
                "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/TestAction",
                "action_type":"MetricsEvent",
                "tool_id":"TCGA:" + participant,
                "involved_datasets":[
                   {
                      "dataset_id":"TCGA:2018-04-05_" + cancer + "_M",
                      "role":"incoming"
                   },
                   {
                      "dataset_id": "TCGA:2018-04-05_" + cancer + "_P_" + participant,
                        "role": "incoming"
                   },
                   {
                      "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_TPR_" + participant,
                      "role":"outgoing"
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
                ]
            }

            # print info
            filename = "MetricsEvent_" + cancer + "_" + participant + "_TPR_" + Mevent_id + ".json"
            # print filename

            with open(out_dir + filename, 'w') as f:
                json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))

            ###########################################################################################################
            # print metrics2 metricsevent file

            # get metrics 2 event id
            Mevent_id, last_event = IDGenerator.get_new_OEB_id("002", "A", last_event)

            # get metrics2 assessment dataset id
            A_data_id, last_assessment_dataset = IDGenerator.get_new_OEB_id("002", "D", last_assessment_dataset)

            info = {

                "_id": "TCGA:2018-04-05_" + cancer + "_metricsEvent_" + participant + "_precision",
                "_schema": "https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/TestAction",
                "action_type": "MetricsEvent",
                "tool_id": "TCGA:" + participant,
                "involved_datasets":[
                   {
                      "dataset_id":"TCGA:2018-04-05_" + cancer + "_M",
                      "role":"incoming"
                   },
                   {
                      "dataset_id": "TCGA:2018-04-05_" + cancer + "_P_" + participant,
                        "role": "incoming"
                   },
                   {
                      "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_precision_" + participant,
                      "role":"outgoing"
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
                ]
            }

            # print info
            filename = "MetricsEvent_" + cancer + "_" + participant + "_precision_" + Mevent_id + ".json"
            # print filename

            with open(out_dir + filename, 'w') as f:
                json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":


    cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA", "GBM", "HNSC", "KICH", "KIRC",
                    "KIRP", "LAML", "LGG", "LIHC", "LUAD", "LUSC", "MESO", "OV", "PAAD", "PCPG", "PRAD",
                    "READ", "SARC", "SKCM", "STAD", "TGCT", "THCA", "THYM", "UCEC", "UCS", "UVM", "ALL"]

    #read file which containes tool ids already pushed to mongo
    with io.open("../mongo_tools_ids.txt", mode='r', encoding="utf-8") as f:
        mongo_tool_ids = json.load(f)

    # read file which containes dataset ids already pushed to mongo
    with io.open("../reference_datasets_mongo_ids.txt", mode='r', encoding="utf-8") as f:
        mongo_datRef_ids = json.load(f)

    # Assuring the output directory does exist
    out_dir = "out/metrics_events/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)


    run(cancer_types, mongo_tool_ids, mongo_datRef_ids, out_dir)