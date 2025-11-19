from Accounts import Accounts 

class Transcations(Accounts):
    
    def __init__(self,dateOpened, bank, accountName, transcations, amount, transactionType, merchant, category, datePosted, isPending):
        super().__init__(dateOpened, bank, accountName, transcations)
        self.amount = amount 
        self.transactionType = transactionType
        self.merchant = merchant
        self.category = category
        self.datePosted = datePosted
        self.isPending = isPending

        

    