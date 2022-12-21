from app.databases.arangodb import Arango
from app.databases.elastic import Elastic

_arango = Arango()
_elastic = Elastic()

if __name__ == "__main__":
    a = _elastic.es.indices.exists(index = 'project')
    print(a)

    # for r in rs:
    #     r = dict(r)
    #     print(r)
    # db.load_data_to_es(rs)
    # ls= []
    # tutorials_csv_file_path = "12312.csv".format(Path(__file__).parents[1])
    # Add documents if there are no records in the index.
    # with open(tutorials_csv_file_path) as csv_file:
    #     csv_reader = csv.reader(csv_file)
    #     fields = next(csv_reader)
    #     for row in csv_reader:
    #         payload = {
    #             'topic': row[1],
    #             'title': {
    #                 'input': row[2],
    #             },
    #             'url': row[3],
    #             'labels': row[4],
    #             'upvotes': int(row[5])
    #         }
    #         payload = dict(payload)
    #         # payload = json.dumps(payload)
    #         ls.append(payload)
    # for i in ls:
    #     print(i)
    #     es.index(
    #         index = "cs.stanford",
    #         body = i
    #     )

# GET /project/_search
# {
#   "size": 20,
#   "query": {
#     "bool": {
#       "must": [
#         {
#           "span_near": {
#             "clauses": [
#               {
#                 "span_multi": {
#                   "match": {
#                     "fuzzy": {
#                       "name": {
#                         "value": "Trava",
#                         "fuzziness": "AUTO"
#                       }
#                     }
#                   }
#                 }
#               },{
#                 "span_multi": {
#                   "match": {
#                     "fuzzy": {
#                       "name": {
#                         "value": "lending",
#                         "fuzziness": "AUTO"
#                       }
#                     }
#                   }
#                 }
#               }
#             ],
#             "slop": 0,
#             "in_order": false
#           }
#         }
#       ]
#     }
#   }
# }

# GET /project/_search
# {
#   "query": {
#     "fuzzy": {
#       "name": {
#         "value": "Trava",
#         "fuzziness": "AUTO",
#         "max_expansions": 50,
#         "prefix_length": 0,
#         "transpositions": true,
#         "rewrite": "constant_score"
#       }
#     }
