import weaviate
import time

def saveData(data, savePath):
   with open(savePath, 'w') as f:
      for entry in data:
         json.dump(entry, f)
         f.write('\n')

f = open("NQ-0-500k.json")
import json
json_data = json.load(f)
f.close()
json_list = list(json_data)

corpus = []

for json_dict in json_list:
    new_doc_obj = {}
    for key in json_dict.keys():
        new_doc_obj[key] = json_dict[key]
    corpus.append(new_doc_obj)

failed_uploads = []

print(f"Preparing to upload {len(corpus)} documents to Weaviate.")

from weaviate.util import get_valid_uuid
from uuid import uuid4

client = weaviate.Client("http://localhost:8080")

start = time.time()

'''
client.batch.configure(batch_size=100)  # Configure batch
with client.batch as batch:
    for data_obj in data_objs:
        batch.add_data_object(
            data_obj,
            class_name,
            # tenant="tenantA"  # If multi-tenancy is enabled, specify the tenant to which the object will be added.
        )
'''
client.batch.configure(batch_size=100)  # Configure batch
with client.batch as batch:
    for doc in corpus:
        id = get_valid_uuid(uuid4())
        data_properties = {
            "document": doc["document"],
            "docID": doc["DocID"]
        }
        doc_vector = doc["vector"]
        batch.add_data_object(
            data_object = data_properties,
            class_name = "Document",
            vector = doc_vector,
            uuid = id
        )
        '''
        try:
            data_properties = {
                "document": doc["document"],
                "docID": doc["DocID"]
            }
            doc_vector = doc["vector"]
            batch.add_data_object(
                data_object = data_properties,
                class_name = "Document",
                vector = doc_vector,
                uuid = id
            )
        except:
            print("Failed to upload document.")
            failed_uploads.append(doc)
        '''

print(f"Failed to upload {len(failed_uploads)}, saving these to file...")
saveData(failed_uploads, "./failed-uploads.json")


print(f"Uploaded {len(corpus)} documents in {time.time() - start} seconds.")
