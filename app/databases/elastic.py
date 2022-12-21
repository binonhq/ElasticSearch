import json

import requests
from elasticsearch import Elasticsearch


class Elastic:
    def __init__(self):
        self.es = Elasticsearch(hosts="http://localhost:9200")
        self.headers = {
            'Content-Type': 'application/json'
        }

    def load_data(self, data_list, index=None):
        if index and self.es.indices.exists(index=index):
            self.es.indices.delete(index=index)
        i = 1
        for data in data_list:
            data = dict(data)
            print(i)
            print(data)
            self.es.index(
                index=index,
                body=data
            )
            i += 1
        return True

    def autocomplete(self, query, index=None):
        if not index:
            index = "_all"
        payload = {
            "query": {
                "match": {
                    "name": {
                        "query": query,
                        "fuzziness": "auto"
                    }
                }
            }
        }
        payload = json.dumps(payload)
        url = f"http://localhost:9200/{index}/_search"
        response = requests.request("GET", url, headers=self.headers, data=payload)
        titles = []
        if response.status_code == 200:
            response = json.loads(response.text)
            options = response["hits"]["hits"]
            search_id = 1
            for option in options:
                titles.append(
                    {'search_id': search_id,
                     'id': option["_source"]["id"],
                     'name': option["_source"]["name"],
                     'type': option["_source"]["tags"]}
                )
                search_id += 1
                # titles = json.dumps(titles)
        return titles
