from arango import ArangoClient


class Arango:
    def __init__(self):
        self.cli = ArangoClient(hosts="http://178.128.93.195:8529/")
        self.db = self.cli.db('GraphDatabase', username='read', password='read_only123')

    def get_document(self, collection, key):
        query = f"for doc in {collection} filter doc._key=={key} return doc"
        doc = self.db.aql.execute(query)
        return doc

    def get_project(self):
        result = []
        projects = self.db.aql.execute(f"""
            for doc in project_ngram
            filter NOT_NULL(doc.name)
            return {{
                "id": doc._key,
                "name": doc.name,
                "tags": {{
                    "projects": 1
                    }},
                "type": "projects",
                "description" : doc.description,

            }}""")
        result += projects
        return result

    def get_smart_contract(self):
        result = []
        smart_contracts = self.db.aql.execute(query=f"""
                    for doc in sc_inv_ngram
                    filter NOT_NULL(doc.name)
                    return {{           
                       "id": doc._key,
                       "name": doc.name,
                       "tags": doc.tags,
                       "type": "smart_contracts"
                    }}
                    """, batch_size=1000)
        result += smart_contracts
        return result


#
# if __name__ == "__main__":
#     db = Arango()
#     rs = db.get_project()
#     for i in rs:
#         print(i)
#         print(list(i["tags"].keys()))
#     # print(rs)

pj_obj = {
    "id": "doc._key",
    "name": "doc.name",
    "tags": {
        "projects": 1
    },
    "type": "projects",
    "description": "doc.description",
}
cntx_obj = {
    "id": "doc._key",
    "name": "doc.name",
    "tags": "doc.tags",
    "type": "smart_contracts"
}
