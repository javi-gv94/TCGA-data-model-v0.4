import os
import io, json
import id_generator


def run(cancer_types, mongo_ids, out_dir):

    last_challenge = "0000000"
    last_test_event = "0000000"
    last_participant_dataset = "0000000"
    last_tool = "0000008"

    IDGenerator = id_generator.IDGenerator()

    for cancer in cancer_types:

        challenge_id, last_challenge = IDGenerator.get_new_OEB_id("002", "X", last_challenge)

        for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):

            #if participant is not in mongo, asign new temporary id
            if participant in mongo_ids:
                tool_id = mongo_ids[participant]
            else:
                tool_id, last_tool = IDGenerator.get_new_OEB_id("002", "T", last_tool)

            #get test event id
            Tevent_id, last_test_event = IDGenerator.get_new_OEB_id("002", "A", last_test_event)

            # get participant dataset id
            participant_data_id, last_participant_dataset = IDGenerator.get_new_OEB_id("002", "D", last_participant_dataset)

            info = {


                "_id": "TCGA:2018-04-05_" + cancer + "_testEvent_" + participant,
                "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/TestAction",
                "action_type":"TestEvent",
                "tool_id":"TCGA:" + participant,
                "involved_datasets":[
                   {
                      "dataset_id": "TCGA:2018-04-05_input",
                      "role": "incoming"
                   },
                   {
                        "dataset_id": "TCGA:2018-04-05_" + cancer + "_P_" + participant,
                        "role": "outgoing"
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
            filename = "TestEvent_" + cancer + "_" + participant + "_" + Tevent_id + ".json"
            # print filename

            with open(out_dir + filename, 'w') as f:
                json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":


    cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA", "GBM", "HNSC", "KICH", "KIRC",
                    "KIRP", "LAML", "LGG", "LIHC", "LUAD", "LUSC", "MESO", "OV", "PAAD", "PCPG", "PRAD",
                    "READ", "SARC", "SKCM", "STAD", "TGCT", "THCA", "THYM", "UCEC", "UCS", "UVM", "ALL"]
    #read file which containes tool ids already pushed to mongo
    with io.open("../mongo_tools_ids.txt", mode='r', encoding="utf-8") as f:
        mongo_ids = json.load(f)

    # Assuring the output directory does exist
    out_dir = "out/test_events/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)


    run(cancer_types, mongo_ids,out_dir)