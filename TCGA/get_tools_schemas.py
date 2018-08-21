import os
import io, json

for participant in os.listdir("/home/jgarrayo/PycharmProjects/TCGA_benchmark/input/participants"):
    info = {
       "_id":"TCGA:" + participant,
       "name":participant,
       "description":"Cancer Driver Genes prediction",
       "is_automated": True,
       "community_id":[
          "TCGA"
       ],
       "tool_contact_id":[
          "Eduard.Porta"
       ],
       "activation":{
          "$date":"2018-04-05T00:00:00.000+0000"
       },
       "references":[
          "10.1016/j.cell.2018.02.060"
       ],
       "tool_access":[
          {
             "tool_access_type_id":"other",
          }
       ],
       "_schema":"https://www.elixir-europe.org/excelerate/WP2/json-schemas/0.4#Tool",
       "status":"online"
    }

    # print info
    filename = "Tool_" + participant + ".json"
    # print filename

    with open("out/" + filename, 'w') as f:
        json.dump(info, f, sort_keys=True, indent=4, separators=(',', ': '))
