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
from plaid.model.transactions_get_request import TransactionsGetRequest #Plaid SDK to build the transcations API req
from datetime import date, timedelta
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
 
 
    def getTransactions(self, access_token, start_date=None, end_date=None):
        """Fetch transactions via access_token, returning transactions for * accounts under that Item. Paginates * transcations to accountID to link the transactions-accounts"""
        end_date = end_date or date.today()                 #default to today if no end_date is provided
        start_date = start_date or (end_date - timedelta(days=30) if hasattr(end_date, "__sub__") else date.today())   #Fetches last 30 days if no start_date is provided
        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)
        all_tx = []
        offset = 0
        count = 500
        while True:
            request = TransactionsGetRequest(access_token=access_token, start_date=start_date, end_date=end_date, count=count, offset=offset)
            response = self.client.transactions_get(request)
            tx = response.transactions
            all_tx.extend(tx)
            if len(tx) < count:
                break
            offset += count
        return all_tx

"""
HOW TRANSACTIONS WORK:
-we use access_token over item_id because item_id just keeps track of connections, 
whereas access_token is what allows us to access the sensative data from the connected institution,
access_token returns * transcations for that item(item is a plaid object representing a bank connection returning * transcations associated with a bank)
-//paginate: returns a big list of transcations in chunkcs(pages) since plaid only returns 500 transcations at a time
we than req the transcations in batches(500/e) untill reciving all transcations,
    whitch we than catoegorize via their accountID to link the transcations to correct account in the db
"""