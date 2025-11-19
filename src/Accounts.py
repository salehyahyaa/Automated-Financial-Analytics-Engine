class Accounts:

    def __init__(self, dateOpened, bank, accountName, transcations):
        self.dateOpened = dateOpened
        self.bank = bank 
        self.accountname = accountName
        self.transcations = transcations

        
    def getAccount(self):
        return f"{self.bank} + " " + {self.accountName}"
    

    def getMoreDetails(self):
        return f"Account Opened: {self.dateOpened}"


#---------------------------------------------------------------------------------------------------------

        


    



    

    



    

    
    
