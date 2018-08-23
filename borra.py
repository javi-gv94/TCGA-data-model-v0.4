from datauri import DataURI
import json

datasets = {
   "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
   "contentVersion": "1.0.0.0",
   "parameters": {
       "stringToTest": {
           "type": "string",
           "defaultValue": "Hello"
       },
       "dataFormattedString": {
           "type": "string",
           "defaultValue": "data:;base64,SGVsbG8sIFdvcmxkIQ=="
       }
   },
   "resources": [],
   "outputs": {
       "dataUriOutput": {
           "value": "[dataUri(parameters('stringToTest'))]",
           "type" : "string"
       },
       "toStringOutput": {
           "type": "string",
           "value": "[dataUriToString(parameters('dataFormattedString'))]"
       }
   }
}

json_data = json.dumps(45.61)

made = DataURI.make('application/json', charset='us-ascii', base64=True, data=json_data)

print (made)

