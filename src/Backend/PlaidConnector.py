import plaid 
import os
from plaid.model.country_code import CountryCode  
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid import ApiClient, Configuration
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.products import Products
from plaid import Environment
#Purpose of this file is to hold our credientals and automate our verification to plaid everytime we send a req

class PlaidConnector:
    
    def __init__(self, client_id, secret, environment):             #we have our.envKeys here so we can automatically send our verification to Plaid since we have to verify oursleves with every req
        self.client_id = os.getenv("PLAID_CLIENT_ID")
        self.secret = os.getenv("PLAID_SECRET")

        self.config = Configuration(
            host=Environment.Production,
            api_key={
                "clientId": self.client_id,
                "secret": self.secret,
            }
        )
        api_client = ApiClient(self.config)                         #Creates the Plaid Client, allows authentication every req
        self.client = plaid_api.PlaidApi(api_client)


    def create_link_token(self):                                                             #PlaidDoc's made the method called create_link_token, we just call it here to use it
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id="USER"), 
            client_name="Automated Financial Analytics Engine",

            products=[Products("transactions")],   #Products("auth"), <-add LATER              #need to establish whitch PlaidProducts you want to use otherwise you cannot use its endpoints                                                                                   
            country_codes=[CountryCode("US")], 
            language="en"
        )
        response = self.client.link_token_create(request)
        return response.link_token


    def exchange_public_token(self, public_token):#access_token //plaidDoc's made the method called that 
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = self.client.item_public_token_exchange(request)
        # #region agent log
        try:#debug log
            import json, time
            with open("/Users/salehyahya/Desktop/TechProjects/FinancialProject/.cursor/debug.log", "a") as f:
                f.write(json.dumps({"location":"PlaidConnector.py:exchange_public_token","message":"response attrs","data":{"has_item_id":hasattr(response,"item_id"),"has_plaid_item_id":hasattr(response,"plaid_item_id")},"timestamp":round(time.time()*1000),"hypothesisId":"A"}) + "\n")
        except Exception:
            pass
        #end of debug log
        return response.access_token, response.item_id


    def getAccounts(self, access_token): # Pull real time balance information for each account associated
        request = AccountsBalanceGetRequest(access_token=access_token)
        response = self.client.accounts_balance_get(request)
        accounts = response.accounts
        return accounts 
 
 
    def getTransactions(self):
        ...