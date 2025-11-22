from plaid import Client 
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
import datetime
class BankConnector:
    def __init__(self, client_id, secret, environment): #we have our.envKeys here so we can automatically send our verification to Plaid since we have to verify oursleves with every req
        self.client_id = client_id
        self.secret = secret
        self.environment = environment

        self.client = Client( #Creates the Plaid Client, allows authenticaiton every req
            client_id = self.client_id,
            secret = self.secret,
            environment = self.environment
        )


    def create_link_token(self): #html goes to this method to fetch PlaidAPI LogInInfo
        request = LinkTokenCreateRequest(
            user=LinkTokenCreateRequestUser(client_user_id="USER"), #nickname for user using software
            client_name="Automated Financial Analytics Engine",
            products=["auth", "transactions", "balances", "investments", "assets", "identity"], #need to establish whitch PlaidProducts you want to use otherwise you cannot use its endpoints
            country_codes=["US"],
            language="en"
        )
        response = self.client.link_token_create(request)
        return response["link_token"]

    def exchange_public_token(self, public_token):
        request = ItemPublicTokenExchangeRequest(public_token=public_token)
        response = self.client.item_public_token_exchange(request)
        return response["access_token"]


    def getAccounts(self, access_token): # Pull real time balance information for each account associated
        request = AccountsBalanceGetRequest(access_token=access_token)
        response = self.client.accounts_balance_get(request)
        accounts = response['accounts']
 
    
    def getTransactions(self):
# Provide a cursor from your database if you've previously
# received one for the Item. Leave null if this is your
# first sync call for this Item. The first request will
# return a cursor.
        cursor = database.get_latest_cursor_or_none(item_id)

        # New transaction updates since "cursor"
        added = []
        modified = []
        removed = [] # Removed transaction ids
        has_more = True

        # Iterate through each page of new transaction updates for item
        while has_more:
        request = TransactionsSyncRequest(
            access_token=access_token,
            cursor=cursor,
        )
        response = plaid_client.transactions_sync(request)

        # Add this page of results
        added.extend(response['added'])
        modified.extend(response['modified'])
        removed.extend(response['removed'])

        has_more = response['has_more']

        # Update cursor to the next cursor
        cursor = response['next_cursor']

        # Persist cursor and updated data
        database.apply_updates(item_id, added, modified, removed, cursor)
