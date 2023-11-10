import weaviate

client = weaviate.Client("http://localhost:8080")

schema = {
    "classes": [
        {
            "class": "Document",
            "description": "A BEIR document.",
            "vectorIndexType": "hnsw",
            "properties": [
                {
                    "name": "document",
                    "dataType": ["text"],
                    "description": "The text content in the BEIR document.",
                },
                {
                    "name": "DocID",
                    "dataType": ["int"],
                    "description": "The Document ID (these are mapped from the original BEIR doc ids to a sequential index).",
                }
            ]
        }
    ]
}

client.schema.create(schema)