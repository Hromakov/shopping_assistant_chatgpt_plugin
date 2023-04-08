import json
import os
import quart
import quart_cors
from quart import jsonify, Response
from quart import request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Note: Setting CORS to allow chat.openapi.com is required for ChatGPT to access your plugin
app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

_SERVICE_AUTH_KEY = os.environ.get("_SERVICE_AUTH_KEY")




# Fetch the service account key JSON file contents (using secrets one by one as this is a public Replit)
type_value = os.environ.get("type")
project_id_value = os.environ.get("project_id")
private_key_id_value = os.environ.get("private_key_id")
private_key_value = os.environ.get("private_key")
client_email_value = os.environ.get("client_email")
client_id_value = os.environ.get("client_id")
auth_uri_value = os.environ.get("auth_uri")
token_uri_value = os.environ.get("token_uri")
auth_provider_x509_cert_url_value = os.environ.get("auth_provider_x509_cert_url")
client_x509_cert_url_value = os.environ.get("client_x509_cert_url")

cred = credentials.Certificate({
    "type": type_value,
    "project_id": project_id_value,
    "private_key_id": private_key_id_value,
    "private_key": private_key_value,
    "client_email": client_email_value,
    "client_id": client_id_value,
    "auth_uri": auth_uri_value,
    "token_uri": token_uri_value,
    "auth_provider_x509_cert_url": auth_provider_x509_cert_url_value,
    "client_x509_cert_url": client_x509_cert_url_value
})

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://groceryplanner-bfcda-default-rtdb.europe-west1.firebasedatabase.app'
})

# Reference the database
ref = db.reference('shoppingList')



def assert_auth_header(req):
    assert req.headers.get(
        "Authorization", None) == f"Bearer {_SERVICE_AUTH_KEY}"


store_layout_description = """
Продукты в магазине расположены в группах. Они пронумерованы в последовательности по дальности, от самой ближней (группа 1) до самой дальней группы (группа 9). Все продукты внутри одной группы находятся в одном и том же месте.
Самая ближняя группа 1: пельмени, пицца, замороженная вишня;
Группа 2: овощи, фрукты, бананы, картофель;
Группа 3: зелень, перец, квашеная капуста;
Группа 4: селедка, хамон, колбаса, куриные ножки, яйца;
Группа 5: каши, каша "пять зерен", макароны, рис;
Группа 6: хлебные изделия;
Группа 7: рыбные продукты;
Группа 8: молочные продукты;
Самая дальняя группа 9: предметы гигиены.
"""





@app.get("/getShoppingListAndStoreLayout")
async def get_shop_list_and_layout():
    assert_auth_header(quart.request)
    
    # Retrieve the data
    shopping_list_data = ref.get()

    # Create a new list with only the required properties
    filtered_shopping_list = []
    for item in shopping_list_data.values():
        filtered_shopping_list.append({
            "isPurchased": item["isPurchased"],
            "name": item["name"]
        })

    # Combine the filtered shopping list data and store layout description into a dictionary
    combined_data = {
        "shopping_list": json.dumps(filtered_shopping_list),
        "store_layout": store_layout_description
    }

    return quart.Response(response=json.dumps(combined_data), status=200)

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