import os
import io, json
import pandas
import id_generator


def run(cancer_types, long_names):

    tools = []
    last_used = "0000000"

    IDGenerator = id_generator.IDGenerator()

    for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):
        tool_id, last_used = IDGenerator.get_new_OEB_id("002", "T", last_used)
        tools.append({"tool_id":tool_id})

    last_used = "0000000"
    for cancer in cancer_types:
        # get schema alphanumeric id
        challenge_id, last_used = IDGenerator.get_new_OEB_id("002", "X", last_used)

        info = {

       "_id":challenge_id,
       "orig_id": "TCGA:2018-04-05_" + cancer,
       "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Challenge",
       "name":"Cancer Driver Genes Prediction Benchmark in " + long_names[cancer],
       "benchmarking_event_id":"OEBE002t000001",
       "is_automated": False,
       "dates":{
          "creation":"2018-04-05T00:00:00Z",
          "modification":"2018-04-05T14:00:00Z",
          "benchmark_start":"2018-04-05T05:00:00Z",
          "benchmark_stop":"2018-04-05T02:00:00Z"
       },
       "url":"https://cancergenome.nih.gov/",
       "community_id":"OEBC002",
       "participants" :tools,
       "challenge_contact_ids":[
          "Matthew.Bailey",
          "Eduard.Porta",
          "Collin.Tokheim"
       ],
       "references":[
          "10.1016/j.cell.2018.02.060"
       ]
        }

        # print info
        filename = "Challenge_" + cancer + ".json"
        # print filename

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

    run(cancer_types, long_names)


#################################################################

    # datasets = []
    # tools = []
    # datasets.append({
    #      "dataset_id":"TCGA:2018-04-05_" + cancer + "_I",
    #      "role":"input"
    #   })
    # datasets.append({
    #      "dataset_id":"TCGA:2018-04-05_" + cancer + "_M",
    #      "role":"metrics_reference"
    #   })
    # for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):
    #     tools.append({"tool_id":"TCGA:" + participant})
    #     datasets.append({
    #      "dataset_id":"TCGA:2018-04-05_" + cancer + "_P_" + participant,
    #      "role":"participant"
    #     })
    #     datasets.append({
    #         "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_TPR_" + participant,
    #         "role": "assessment"
    #     })
    #     datasets.append({
    #         "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_precision_" + participant,
    #         "role": "assessment"
    #     })
    #
    #     datasets.append({
    #         "dataset_id": "TCGA:2018-04-05_" + cancer + "_" + participant + "_Summary",
    #         "role": "challenge"
    #     })