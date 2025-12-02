from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid import ApiClient, Configuration
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.products import Products
import os
#Purpose of this file is to hold our credientals and automate our verification to plaid everytime we send a req

class BankConnector:
    def __init__(self, client_id, secret, environment): 
        configuration = Configuration(
            host = environment,
            api_key = { #we have our.envKeys here so we can automatically send our verification to Plaid since we have to verify oursleves with every req
                "clientId": client_id,
                "secret": secret,
            }
        )
        self.client = plaid_api.PlaidApi(ApiClient(configuration)) #Creates the Plaid Client, allows authenticaiton every req


    def create_link_token(self): #html goes to this method to fetch PlaidAPI LogInInfo
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id="USER"), 
            client_name="Automated Financial Analytics Engine",
            products= [ #need to establish whitch PlaidProducts you want to use otherwise you cannot use its endpoints
            Products.AUTH,
            Products.TRANSACTIONS,
            Products.BALANCES,
            Products.INVESTMENTS,
            Products.ASSETS
            ], 
            country_codes=["US"], 
            language="en"
        )
        response = self.client.link_token_create(request)
        return response["link_token"]


    def exchange_public_token(self, public_token):#access_token //plaidDoc's made the method called that 
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = self.client.item_public_token_exchange(request)
        return response["access_token"]


    def getAccounts(self, access_token): # Pull real time balance information for each account associated
        request = AccountsBalanceGetRequest(access_token=access_token)
        response = self.client.accounts_balance_get(request)
        accounts = response['accounts']
        return accounts 
 
    
    def getTransactions(self):
        ...

