from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from app.core.db import engine, Base
from app.routes import router as routes
from app.graphql.schema import schema

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes)

@app.post("/graphql")
async def graphql_endpoint(request: Request):
    data = await request.json()
    query = data.get("query")
    variables = data.get("variables")
    result = schema.execute(query, variables=variables)
    response = {}
    if result.errors:
        response["errors"] = [str(error) for error in result.errors]
    if result.data:
        response["data"] = result.data
    return response

# GraphQL Playground
@app.get("/graphql", response_class=HTMLResponse)
async def graphql_playground():
    playground_html = """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset=utf-8/>
        <title>GraphQL Playground</title>
        <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/css/index.css"/>
        <link rel="shortcut icon" href="//cdn.jsdelivr.net/npm/graphql-playground-react/build/favicon.png"/>
        <script src="//cdn.jsdelivr.net/npm/graphql-playground-react/build/static/js/middleware.js"></script>
      </head>
      <body>
        <div id="root" style="height: 100vh;"></div>
        <script>
          window.addEventListener('load', function (event) {
            GraphQLPlayground.init(document.getElementById('root'), { endpoint: '/graphql' })
          })
        </script>
      </body>
    </html>
    """
    return playground_html
