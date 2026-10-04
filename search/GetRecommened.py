import pickle 
import json
class Store:
    def __init__(self):
        pass  # No need to store the function as an instance attribute

    def store(self, obj, name):

        
        with open(f"/workspaces/nightfall/variables/{name}.pkl", "wb") as f:
            pickle.dump(obj, f)

    def load(self, varname):
        with open(f"/workspaces/nightfall/variables/{varname}.pkl", "rb") as f:
            return pickle.load(f)

store = Store()
# import http.client

# conn = http.client.HTTPSConnection("api.audius.co")

# headers = { 'Authorization': "Bearer YOUR_SECRET_TOKEN" }

# conn.request("GET", "/v1/tracks/recommended", headers=headers)

# res = conn.getresponse()
# data = res.read()
data = json.loads(store.load( "data"))
print(((list(data.values())[0])[0]).keys())