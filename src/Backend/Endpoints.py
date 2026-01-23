from PlaidConnector import PlaidConnector
from fastapi import APIRouter, HTTPException
from fastapi import status 
from dotenv import load_dotenv
import os
from database.Connection import Connection #from folder.file import class
import psycopg2

router = APIRouter()
db = Connection() 
load_dotenv()
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV")

bank = PlaidConnector(PLAID_CLIENT_ID, PLAID_SECRET, PLAID_ENV)


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

        access_token = bank.exchange_public_token(public_token)         
        if access_token == None:
            raise 
        return {"access_token": access_token}
    except Exception as e:                                                      #The second catches unexpected errors and converts them to 500, Both is needed
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")  #always good practice to include this Ecpection at the end of every try exepct endpoint ALWAYS         
        