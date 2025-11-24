from BankConnector import BankConnector
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
import os

router = APIRouter()

load_dotenv()
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV")

bank = BankConnector(PLAID_CLIENT_ID, PLAID_SECRET, PLAID_ENV)


@router.get("/create_link_token") #putting data in the html btn to get to plaid
def createLinkToken():
    return {"link_token": bank.create_link_token()}


@router.post("/exchange_public_token") #giving plaid our verificaiton("acess_token") to get access to accounts
def getAccessToken(body: dict): #accepting Access_tokens as dicts
    public_token = body["public_token"] #we give public token
    access_token = bank.exchange_public_token(public_token) #Here we recieve our acess token
    return {"access_token": access_token} #gets our access token