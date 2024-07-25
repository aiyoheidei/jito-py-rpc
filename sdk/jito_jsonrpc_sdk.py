import requests
import os

# Jito JSON RPC SDK
# Bindings for https://github.com/jito-labs/mev-protos/blob/master/json_rpc/http.md
class JitoJsonRpcSDK:
  # Initialize a block engine URL
  def __init__(self, url, uuid_var=None):
    self.url = url
    if uuid_var == None:
      self.uuid_var = None
    else:
      self.uuid_var = self.__get_uuid(uuid_var)

  def __get_uuid(self, uuid_var):
    return os.getenv(uuid_var)

  # Send a request to the Block engine url using the JSON RPC methods 
  def __send_request(self, endpoint, method, params=None):
    if endpoint == None:
      return "Error: Please enter a valid endpoint."
    
    if self.uuid_var == None:
      headers = {
          'Content-Type': 'application/json', 
          "accept": "application/json"
      }
    else:
      headers = {
          'Content-Type': 'application/json', 
          "accept": "application/json",
          "x-jito-atuh": self.uuid_var
      }
    data = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": method,
        "params": [params]
    }

    try:
      resp = requests.post(self.url + endpoint, headers=headers, json=data)
      resp.raise_for_status()
      return {"success": True, "data": resp.json()}
    except requests.exceptions.HTTPError as errh:
      return {"success": False, "error": f"HTTP Error: {errh}"}
    except requests.exceptions.ConnectionError as errc:
      return {"success": False, "error": f"Error Connecting: {errc}"}
    except requests.exceptions.Timeout as errt:
      return {"success": False, "error": f"Timeout Error: {errt}"}
    except requests.exceptions.InvalidHeader as err:
      return {"success": False, "error": f"Invalid Header error: {err}"}
    except requests.exceptions.InvalidURL as err:
      return {"success": False, "error": f"InvalidURL error: {err}"}
    except requests.exceptions.RequestException as err:
      return {"success": False, "error": f"An error occurred: {err}"}
  
  #Bundle Endpoint
  def get_tip_accounts(self, params=None):
    if self.uuid_var == None:
      return self.__send_request(endpoint="/bundles", method="getTipAccounts")
    else:
      return self.__send_request(endpoint="/bundles?uuid=" + self.uuid_var, method="getTipAccounts")

  def get_bundle_statuses(self, params=None):
    if self.uuid_var == None:
      return self.__send_request(endpoint="/bundles", method="getBundleStatuses",params=params)
    else:
      return self.__send_request(endpoint="/bundles?uuid=" + self.uuid_var, method="getBundleStatuses",params=params)

  def send_bundle(self, params=None):
    if self.uuid_var == None:
      return self.__send_request(endpoint="/bundles",method="sendBundle", params=params)
    else:
      return  self.__send_request(endpoint="/bundles?uuid=" + self.uuid_var, method="sendBundle", params=params)

  # Transaction Endpoint
  def send_txn(self, params=None):
    if self.uuid_var == None:
      return self.__send_request(endpoint="/transactions",method="sendTransaction", params=params)
    else:
      return self.__send_request(endpoint="/transactions?uuid=" + self.uuid_var, method="sendTransaction", params=params)
