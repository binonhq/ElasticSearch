from sanic import Sanic
from sanic.response import json
from sanic_openapi import openapi2_blueprint
from sanic_openapi import swagger_blueprint
from sanic_openapi.openapi2 import doc

from app.databases.arangodb import Arango
from app.databases.elastic import Elastic

app = Sanic(name="SearchAPI")
app.blueprint(openapi2_blueprint)
app.blueprint(swagger_blueprint)

_arango = Arango()
_elastic = Elastic()


@app.route("/import_data_to_elasticsearch")
@doc.tag("Import data")
@doc.summary("Import data from ArangoDB to Elasticsearch")
@doc.consumes(doc.String(name="Type", description="'projects' or 'smart_contracts'"), location="query", required=True)
@doc.response(400, {"message": str}, description="Bad Request")
async def import_data_to_es(request):
    import_type = request.args.get('Type')
    if import_type == 'projects':
        data_list = _arango.get_project()
    elif import_type == 'smart_contracts':
        data_list = _arango.get_smart_contract()
    else:
        return json({"Error": "Wrong type"})

    load_data = _elastic.load_data(data_list, index=import_type)
    if load_data:
        return json({"status": "Success"})
    else:
        return json({"status": "False"})


@app.route("/autocomplete")
@doc.tag("Autocomplete")
@doc.consumes(doc.String(name="Query string", description="query string"), location="query", required=True)
@doc.consumes(doc.String(name="Type search", description="'project' or 'smart_contract' DEFAULT is 'all'"),
              location="query")
async def autocomplete(request):
    query = request.args.get('Query string')
    index = request.args.get('Type search')
    if not index:
        index = '_all'
    result = _elastic.autocomplete(query=query, index=index)
    return json(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
