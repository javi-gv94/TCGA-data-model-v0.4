import os
import io, json
import pandas
import id_generator


def run(cancer_types, long_names):

    last_dataset = "000007S"

    IDGenerator = id_generator.IDGenerator()

    for cancer in cancer_types:

        # get ref dataset id
        data_id, last_dataset = IDGenerator.get_new_OEB_id("002", "D", last_dataset)

        info = {
            "_id":data_id,
            "datalink":{
               "uri":"https://portal.gdc.cancer.gov/",
               "attrs":["archive"],
               "validation_date":"2018-04-05T00:00:00Z",
               "status":"ok"
            },
            "type":"metrics_reference",
            "version":"unknown",
            "name":"Metrics Reference Dataset for " + long_names[cancer],
            "description":"List of genes (described by TCGA community) that can be used as 'gold standard' in " + long_names[cancer] + " benchmark ",
            "dates":{
               "creation":"2018-04-05T00:00:00Z",
               "modification":"2018-04-05T14:00:00Z"
            },
            "depends_on":{
               "rel_dataset_ids":[
                  {
                     "dataset_id":"OEBD002000000L",
                  }
               ]
            },
            "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/1.0/Dataset",
            "community_id":"OEBC002",
            "dataset_contact_ids":[
               "Matthew.Bailey",
               "Eduard.Porta",
               "Collin.Tokheim"
            ]
        }

        filename = "Dataset_Metrics_Ref_" + cancer + "_" + data_id + ".json"
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

    run(cancer_types, long_names)