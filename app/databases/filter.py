from elasticsearch import Elasticsearch
from sanic import json


class SearchFilter:
    def __init__(self, connection_url="http://localhost:9200"):
        self.connection_url = connection_url
        self.es = Elasticsearch(self.connection_url)

    def projects_search_v1(self, search_str, limit=10):
        if search_str is None:
            return None
        index = "projects"
        query = {
            "bool": {
                "must": [
                    {"fuzzy": {
                        "description": {
                            "value": "{}".format(search_str),
                            "fuzziness": 2,
                            "max_expansions": 50,
                            "prefix_length": 0,
                            "transpositions": "false",
                            "rewrite": "constant_score"
                        }
                    }}
                ],
                "should": [
                    {"wildcard": {
                        "name": {
                            "value": "{}*".format(search_str),
                            "boost": 2,
                            "case_insensitive": "true",
                            "rewrite": "constant_score"
                        }
                    }},
                    {"match_phrase_prefix": {
                        "name": "{}".format(search_str)
                    }}
                ],
                "filter": [],
                "must_not": []
            }
        }
        resp = self.es.search(index=index, query=query, size=limit)
        hits_ = []
        total_hits = resp["hits"]["total"]["value"]
        for i in resp["hits"]["hits"]:
            hit_ = {
                "_id": i["_id"],
                "_score": i["_score"],
                "id": i["_source"]["id"],
                "name": i["_source"]["name"],
                "tags": i["_source"]["tags"],
                "type": i["_source"]["type"],
                "_description": i["_source"]["description"]
            }
            hits_.append(hit_)
        return json({"total_hits": total_hits,
                     "hits": hits_})

    def contract_search_v1(self, search_str, limit=10):
        if search_str is None:
            return None
        index = "smart_contracts"
        query = {
            "bool": {
                "must": [
                    {"fuzzy": {
                        "name": {
                            "value": "{}".format(search_str),
                            "fuzziness": "AUTO",
                            "max_expansions": 50,
                            "prefix_length": 0,
                            "transpositions": "false",
                            "rewrite": "constant_score"
                        }
                    }}
                    # {
                    #     "wildcard": {
                    #         "name": {
                    #             "value": "*{}*".format(search_str),
                    #             "boost": 1.0,
                    #             "case_insensitive": "true",
                    #             "rewrite": "constant_score"
                    #         }
                    #     }
                    # }
                ],
                "should": [
                    {"wildcard": {
                        "name": {
                            "value": "*{}*".format(search_str),
                            "boost": 1.5,
                            "case_insensitive": "true",
                            "rewrite": "constant_score"
                        }
                    }},
                    {"match_phrase_prefix": {
                        "name": "{}".format(search_str)
                    }}
                    # {"fuzzy": {
                    #     "name": {
                    #         "value": "{}".format(search_str),
                    #         "fuzziness": "AUTO",
                    #         "max_expansions": 20,
                    #         "prefix_length": 0,
                    #         "transpositions": "false",
                    #         "rewrite": "constant_score"
                    #     }
                    # }}
                ],
                "filter": [],
                "must_not": []
            }
        }
        resp = self.es.search(index=["smart_contracts", "projects"], query=query, size=limit)
        hits_ = []
        total_hits = resp["hits"]["total"]["value"]
        for i in resp["hits"]["hits"]:
            hit_ = {
                "_id": i["_id"],
                "_score": i["_score"],
                "id": i["_source"]["id"],
                "name": i["_source"]["name"],
                "tags": i["_source"]["tags"],
                "type": i["_source"]["type"]
            }
            hits_.append(hit_)
        return json({"total_hits": total_hits,
                     "hits": hits_})

    def search_v2(self, search_str, limit=10, index=None):
        if search_str is None:
            return None
        if index is None:
            index = ["projects", "smart_contracts"]

        tokens = search_str.split(" ")

        name_field_clause = [{
            "span_multi": {
                "match": {
                    "fuzzy": {
                        "name": {
                            "value": "{}".format(i),
                            "fuzziness": "1"
                        }
                    }
                }
            }
        } for i in tokens]

        des_field_clause = [{
            "span_multi": {
                "match": {
                    "fuzzy": {
                        "description": {
                            "value": "{}".format(i),
                            "fuzziness": "1"
                        }
                    }
                }
            }
        } for i in tokens]

        multimatch = [{
            "multi_match": {
                "query": "{}".format(i),
                "fields": ["description", "name"],
                "fuzziness": 1,
                "boost": 1
            }
        } for i in tokens]

        match_bool_prefix = {
            "match_bool_prefix": {
                "name": {
                    "query": search_str,
                    "boost": 5
                }
            }
        }

        must_param = []
        should_param = [{"span_near": {
            "clauses": des_field_clause,
            "slop": 12,
            "in_order": "false"
        }}, {"span_near": {
            "clauses": name_field_clause,
            "slop": 1,
            "in_order": "false"
        }}, match_bool_prefix]

        for i in multimatch:
            should_param.append(i)

        query = {
            "bool": {
                "should": should_param
            }
        }
        # print(query)

        resp = self.es.search(index=index, query=query, size=limit)
        hits_ = []
        total_hits = resp["hits"]["total"]["value"]
        for i in resp["hits"]["hits"]:
            hit_ = {
                "_id": i["_id"],
                "_score": i["_score"],
                "id": i["_source"]["id"],
                "name": i["_source"]["name"],
                "tags": i["_source"]["tags"],
                "type": i["_source"]["type"]
            }
            hits_.append(hit_)
        return json({"total_hits": total_hits,
                     "hits": hits_})

# kibana query
# GET /projects,smart_contracts/_search
# {
#     "query":{
#     "bool": {
#       "should": [
#         {"span_near": {
#           "clauses": [
#             {
#               "span_multi": {
#                 "match": {
#                   "fuzzy": {
#                     "name": {
#                       "value": "trava",
#                       "fuzziness": "AUTO"
#                     }
#                   }
#                 }
#               }
#             },{
#               "span_multi": {
#                 "match": {
#                   "fuzzy":{
#                     "name":{
#                       "value": "fin",
#                       "fuzziness": "AUTO"
#                     }
#                   }
#                 }
#               }
#             }
#           ],
#           "slop": 0,
#           "in_order": false
#         }},
#         {"span_near": {
#           "clauses": [
#             {
#               "span_multi": {
#                 "match": {
#                   "fuzzy": {
#                     "description": {
#                       "value": "trava",
#                       "fuzziness": "AUTO"
#                     }
#                   }
#                 }
#               }
#             },{
#               "span_multi": {
#                 "match": {
#                   "fuzzy":{
#                     "description":{
#                       "value": "fin",
#                       "fuzziness": "AUTO"
#                     }
#                   }
#                 }
#               }
#             }
#           ],
#           "slop": 10,
#           "in_order": false
#         }},
#         {
#           "multi_match": {
#             "query": "trava",
#             "fields": ["description", "name"],
#             "fuzziness": 0,
#             "boost": 1
#           }
#         },
#                 {
#           "multi_match": {
#             "query": "fin",
#             "fields": ["description", "name"],
#             "fuzziness": 0,
#             "boost": 1
#           }
#         },
#         {
#           "match_bool_prefix":{
#             "name": {
#               "query": "trava fin",
#               "boost": 1
#             }
#           }
#         }
#         ]
# }}}