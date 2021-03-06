import os
import io, json
import pandas
import id_generator


def run(cancer_types, long_names, urls, out_dir):


    IDGenerator = id_generator.IDGenerator()

    last_used = "0000000"

    for cancer in cancer_types:
        # get schema alphanumeric id
        challenge_id, last_used = IDGenerator.get_new_OEB_id("002", "X", last_used)
        info = {

       "_id":"TCGA:2018-04-05_" + cancer,
       "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Challenge",
       "acronym": cancer,
       "name":"Cancer Driver Genes Prediction Benchmark in " + long_names[cancer],
       "benchmarking_event_id":"TCGA:2018-04-05",
       "is_automated": False,
       "dates":{
          "creation":"2018-04-05T00:00:00Z",
          "modification":"2018-04-05T14:00:00Z",
          "benchmark_start":"2018-04-05T05:00:00Z",
          "benchmark_stop":"2018-04-05T02:00:00Z"
       },
       "metrics_categories": [

           {
               "category": "assessment",
               "description": "metrics used to benchmark the performance of cancer genes predictors in Challenge "+ long_names[cancer] +
                                ", generating the assessment datatseta",
               "metrics" : [
                   {
                       "metrics_id": "TCGA:TPR",
                       "tool_id": "TCGA:compute_TPR"
                   },
                   {
                       "metrics_id": "TCGA:precision",
                       "tool_id": "TCGA:compute_precision"
                   }
               ]
           },
           {
               "category": "aggregation",
               "description": "metrics used to aggregate the assessment data of all cancer genes predictors participating in challenge " +
                              long_names[cancer] + " in a consolidated Aggregation dataset",
               "metrics": [
                   {
                       "metrics_id": "TCGA:aggregation",
                       "tool_id": "TCGA:aggregate_benchmark"
                   }
               ]
           }
       ],
       "url":urls[cancer],
       "challenge_contact_ids":[
          "Matthew.Bailey",
          "Eduard.Porta",
          "Collin.Tokheim"
       ],
       "references":[
          "doi:10.1016/j.cell.2018.02.060"
       ]
        }

        # print info
        filename = "Challenge_" + cancer + "_" + challenge_id + ".json"
        # print filename

        with open(out_dir + filename, 'w') as f:
            json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":


    cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA", "GBM", "HNSC", "KICH", "KIRC",
                    "KIRP", "LAML", "LGG", "LIHC", "LUAD", "LUSC", "MESO", "OV", "PAAD", "PCPG", "PRAD",
                    "READ", "SARC", "SKCM", "STAD", "TGCT", "THCA", "THYM", "UCEC", "UCS", "UVM", "ALL"]

    data = pandas.read_csv("../cancer_names.tsv", sep="\t",
                           comment="#", header=None)

    long_names = {}
    urls = {}
    for index, row in data.iterrows():
        long_names[row[0]] = row[1]
        urls[row[0]] = row[2]

    # Assuring the output directory does exist
    out_dir = "out/Challenges/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    run(cancer_types, long_names, urls, out_dir)


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