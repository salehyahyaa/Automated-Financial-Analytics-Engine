from PlaidConnector import PlaidConnector
from fastapi import APIRouter, HTTPException
from fastapi import status 
from dotenv import load_dotenv
import os
import json
import time
from database.Connection import Connection 
from DataAutomation import DataAutomation 
import psycopg2
DEBUG_LOG = "/Users/salehyahya/Desktop/TechProjects/FinancialProject/.cursor/debug.log"

router = APIRouter()
db = Connection() 
load_dotenv()
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV")

bank = PlaidConnector(PLAID_CLIENT_ID, PLAID_SECRET, PLAID_ENV)
dataAutomation = DataAutomation(db)


@router.get("/create_link_token", status_code = 200)                            #putting data in the html btn to get to plaid
def createLinkToken():
    try:
        link_token = bank.create_link_token()                                   #assign the LinkToken to var to return it
        if link_token == None: 
            raise HTTPException(500, detail = "Link Token Failed to create")    #only if we have no token returned #tackling potionel error's before actully telling endpoint what to do
        return {"link_token": link_token}                                       #return link_token 
    except Exception as e:
        raise HTTPException(500, detail = f"ServerSide Error: {str(e)}")

 
@router.post("/exchange_public_token", status_code = 200)                       #giving plaid our verificaiton("acess_token") -> get access to accounts
def getAccessToken(body: dict):                                                 #accepting Access_tokens as dicts
    try:
        public_token = body.get("public_token")
        if not public_token:                                                    #publicKey is what we send to Plaid to recive accessToken to login
            raise HTTPException(400, detail = "frontend needs PUBLIC TOKEN to request accessToken")

        access_token, plaid_item_id = bank.exchange_public_token(public_token)       #Assigmation is atomic either both get values or NONE
        
        if access_token == None:
            raise HTTPException(500, detail="Server error")
        
        plaid_items_id_column = dataAutomation.store_plaid_item_id(plaid_item_id)   #tracks inserated row of plaid_item_id so when  ID column auto increments we can store that ID and return it to plaid_items_id_column
        dataAutomation.store_access_token(access_token, plaid_items_id_column)   
        return {"access_token": access_token}
    except HTTPException:
        raise
    except Exception as e:
        try:#debug log logic
            with open(DEBUG_LOG, "a") as f:                          
                f.write(json.dumps({"location":"Endpoints.py:getAccessToken","message":"exception","data":{"type":type(e).__name__,"msg":str(e)},"timestamp":round(time.time()*1000),"hypothesisId":"D"}) + "\n")
        except Exception:
            pass #end of debug log logic
        raise HTTPException(500, detail=f"Server error: {str(e)}")


@router.post("/sync_checking_accounts", status_code=200)
def getCheckingAccounts():
    try:
        result = dataAutomation.get_latest_plaid_item()
        if not result:
            raise HTTPException(404, detail="No linked item_id found. Link a bank first.")
        plaid_items_id_column, access_token = result
        accounts = bank.getAccounts(access_token)
        checking_accounts = [account for account in accounts if account.type and str(account.type).lower() == "depository"] #plaid uses depository to identify checking accounts
        dataAutomation.store_checking_accounts(checking_accounts, plaid_items_id_column)
        return {"stored": len(checking_accounts)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=f"Server error: {str(e)}")


@router.post("/sync_credit_accounts", status_code=200)
def getCreditAccounts():
    try:
        result = dataAutomation.get_latest_plaid_item()
        if not result:
            raise HTTPException(404, detail="No linked item found. Link a bank first.")
        plaid_items_id_column, access_token = result
        accounts = bank.getAccounts(access_token)
        credit_accounts = [account for account in accounts if account.type and str(account.type).lower() == "credit"] #plaid uses credit to identify credit accounts
        dataAutomation.store_credit_accounts(credit_accounts, plaid_items_id_column)
        return {"stored": len(credit_accounts)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=f"Server error: {str(e)}")




"""
-so everytime we create a link token //by starting program and clicking the connect bank account button
-we are prompted to enter user login credentials(public token) whitch plaid exchanges into access_token to securly log in
-plaid then creates an item_id(unique identifier) to represent every successful connection to a finaincal institution
-from that item_id our syncCredit/Checking endpoints processes every new linked connection    //endpoints are statless so every endpoint sends the data recived to the db thanks to our DataAutomation class
    for every iteration the sync_credit will filter for credit accounts and the sync_checking will filter for checking accounts
    then it will add those accounts to the proper columns in the accounts table
"""