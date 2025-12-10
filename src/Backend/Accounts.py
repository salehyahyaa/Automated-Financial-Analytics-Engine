class Accounts:

    def __init__(self, dateOpened, bank, accountName, transactions):
        self.dateOpened = dateOpened
        self.bank = bank 
        self.accountName = accountName
        self.transactions = transactions

        
    def getAccount(self):
        return f"{self.bank} + {self.accountName}"
    

    def getMoreDetails(self):
        return f"Account Opened: {self.dateOpened}"
#---------------------------------------------------------------------------------------------------------

        


    



    

    



    

    
    
