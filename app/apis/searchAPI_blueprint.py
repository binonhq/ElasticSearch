from sanic import Sanic
from sanic.response import json
from sanic_openapi import openapi2_blueprint
from sanic_openapi import swagger_blueprint
from sanic_openapi.openapi2 import doc

from app.databases.filter import SearchFilter

app = Sanic(name="SearchAPI")
app.blueprint(openapi2_blueprint)
# app.blueprint(swagger_blueprint)

esearch = SearchFilter()


@app.route("/search")
@doc.tag("Elastic Search Test")
@doc.summary("Search data by type and string")
@doc.consumes(doc.String(name="index_type", description="'projects or 'smart_contracts'"), location="query",
              required=True)
@doc.consumes(doc.String(name="search_str"), location="query", required=True)
@doc.consumes(doc.Integer(name="limit"), location="query")
@doc.response(400, {"message": str}, description="Bad Request")
async def search(request):
    args = request.args
    search_str = args.get("search_str")
    index_type = args.get("index_type")
    limit = int(args.get('limit'))
    if limit <= 0 or limit >= 10000:
        limit = 10  # default value
    if index_type == "projects":
        result = esearch.projects_search_v1(search_str=search_str, limit=limit)
    elif index_type == "smart_contracts":
        result = esearch.contract_search_v1(search_str=search_str, limit=limit)
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
