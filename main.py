import json
import os
import quart
import quart_cors
from quart import request

# Note: Setting CORS to allow chat.openapi.com is required for ChatGPT to access your plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

_SERVICE_AUTH_KEY = os.environ.get("_SERVICE_AUTH_KEY")



def assert_auth_header(req):
    assert req.headers.get(
        "Authorization", None) == f"Bearer {_SERVICE_AUTH_KEY}"




@app.get("/getShoppingListAndStoreLayoutResponse/<string:username>")
async def get_shop_list_and_layout(username):
    assert_auth_header(quart.request)
    #return quart.Response(response=json.dumps(_TODOS.get(username, [])), status=200)
    return quart.Response(response="hello", status=200)


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")


@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")


def main():
    app.run(debug=True, host="0.0.0.0", port=5002)


if __name__ == "__main__":
    main()