from plaid import Client 
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

class BankConnector:
    def __init__(self, client_id, secret, environment): #we have our.envKeys here so we can automatically send our verification to Plaid since we have to verify oursleves with every req
        self.client_id = client_id
        self.secret = secret
        self.environment = environment

        self.client = Client( #Creates the Plaid Client, allows authenticaiton every req
            client_id=self.client_id,
            secret=self.secret,
            environment=self.environment
        )


    def create_link_token(self):
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

        
