import os
import io, json
import pandas

cancer_types = ["ACC", "BLCA", "BRCA", "CESC", "CHOL", "COAD", "DLBC", "ESCA"]

data = pandas.read_csv("../cancer_names.tsv", sep="\t",
                           comment="#", header=None)

long_names = {}
for index, row in data.iterrows():
    long_names[row[0]] = row[1]



for cancer in cancer_types:

    datasets = []
    tools = []
    datasets.append({
         "dataset_id":"TCGA:2018-04-05_" + cancer + "_I",
         "role":"input"
      })
    datasets.append({
         "dataset_id":"TCGA:2018-04-05_" + cancer + "_M",
         "role":"metrics_reference"
      })
    for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):
        tools.append({"tool_id":"TCGA:" + participant})
        datasets.append({
         "dataset_id":"TCGA:2018-04-05_" + cancer + "_P_" + participant,
         "role":"participant"
        })
        datasets.append({
            "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_TPR_" + participant,
            "role": "assessment"
        })
        datasets.append({
            "dataset_id": "TCGA:2018-04-05_" + cancer + "_A_precision_" + participant,
            "role": "assessment"
        })

        datasets.append({
            "dataset_id": "TCGA:2018-04-05_" + cancer + "_" + participant + "_Summary",
            "role": "challenge"
        })

    info = {

   "_id":"TCGA:2018-04-05_" + cancer,
   "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4/Challenge",
   "name":"Cancer Driver Genes Prediction Benchmark in " + long_names[cancer],
   "benchmarking_event_id":"TCGA:2018-04-05",
   "is_automated": False,
   "dates":{
      "creation":"2018-04-05T00:00:00Z",
      "modification":"2018-04-05T14:00:00Z",
      "benchmark_start":"2018-04-05T05:00:00Z",
      "benchmark_stop":"2018-04-05T02:00:00Z"
   },
   "dataset_ids": datasets,
   "participants":tools,
   "metrics":[
      {
         "metrics_id":"TCGA:TPR"
      },
      {
         "metrics_id":"TCGA:PPV"
      }
   ],
   "url":"https://cancergenome.nih.gov/",
   "community_id":"TCGA",
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
