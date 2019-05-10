import os
import io, json
import pandas
import id_generator


def run(cancer_types, long_names, mongo_tool_ids, tool_contact):

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

        # get challenge dataset_id
        challenge_data_id, last_challenge_dataset = IDGenerator.get_new_OEB_id("002", "D", last_challenge_dataset)

        # generate array with all related datasets and object with participants metrics results
        involved_datasets = []

        inline_data = {

            "visualization": { "type":"2D-plot",
                               "x_axis": "OEBM0020000002",
                               "y_axis": "OEBM0020000001"
                               },
            "challenge_participants": []
        }

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


            # read files which containes metrics values
            with io.open("out/Dataset_assessment_" + cancer + "_" + participant + "_TPR_" + A_data_id_TPR + ".json", mode='r', encoding="utf-8") as f:
                assess_file = json.load(f)
                metric1 = assess_file["datalink"]["inline_data"]["value"]

            with io.open("out/Dataset_assessment_" + cancer + "_" + participant + "_precision_" + A_data_id_precision + ".json", mode='r', encoding="utf-8") as f:
                assess_file = json.load(f)
                metric2 = assess_file["datalink"]["inline_data"]["value"]

            inline_data["challenge_participants"].append( {
                "tool_id": tool_id,
                "metric_x": metric1,
                "metric_y": metric2,
            })

            ###############################################################################
            involved_datasets.append({
                "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_TPR_" + participant,
            })

            involved_datasets.append({
                "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_precision_" + participant,
            })

        # append reference and input datasets
        involved_datasets.append({
                               "dataset_id": "OEBD002000000L",
                           })
        involved_datasets.append({
            "dataset_id": "TCGA:2018-04-05_" + cancer + "_M",
        })


        info = {

            "_id": "TCGA:2018-04-05_" + cancer + "_Aggregation",
            "datalink":{
               "inline_data": inline_data,
                "schema_url": "https://raw.githubusercontent.com/inab/OpenEBench_scientific_visualizer/js/benchmarking_data_model/inline_data_visualizer.json"
            },
            "type":"aggregation",
            "visibility": "public",
            "version":"unknown",
            "name":"Summary dataset for challenge: " + long_names[cancer],
            "description":"Summary dataset with information about challenge " + long_names[cancer] + " (e.g. input/output datasets, metrics...) in participant " + participant,
            "dates":{
               "creation":"2018-04-05T00:00:00Z",
               "modification":"2018-04-05T14:00:00Z"
            },
            "depends_on":{
                "tool_id": "TCGA:aggregate_benchmark",
               "rel_dataset_ids": involved_datasets,
            },
            "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Dataset",
            "community_ids":["OEBC002"],
            "challenge_ids": ["TCGA:2018-04-05_" + cancer],
            "dataset_contact_ids":[
                "Eduard.Porta",
                "Matthew.Bailey",
                "Collin.Tokheim",
                "Loris.Mularoni",
                "Juri.Reimand",
                "David.Tamborero",
                "Nathan.Dees"
            ]
        }

        # print info
        filename = "Dataset_Aggregation_" + cancer + "_" + challenge_data_id + ".json"
        # print filename

        with open("out/" + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":


    cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA", "GBM", "HNSC", "KICH", "KIRC",
                    "KIRP", "LAML", "LGG", "LIHC", "LUAD", "LUSC", "MESO", "OV", "PAAD", "PCPG", "PRAD",
                    "READ", "SARC", "SKCM", "STAD", "TGCT", "THCA", "THYM", "UCEC", "UCS", "UVM", "ALL"]

    data = pandas.read_csv("../cancer_names.tsv", sep="\t",
                           comment="#", header=None)

    long_names = {}
    for index, row in data.iterrows():
        long_names[row[0]] = row[1]

    #read file which containes tool ids already pushed to mongo
    with io.open("../mongo_tools_ids.txt", mode='r', encoding="utf-8") as f:
        mongo_tool_ids = json.load(f)

    # read file which containes tool contact
    with io.open("../tools_contacts.txt", mode='r', encoding="utf-8") as f:
        tool_contact = json.load(f)


    run(cancer_types, long_names, mongo_tool_ids, tool_contact)