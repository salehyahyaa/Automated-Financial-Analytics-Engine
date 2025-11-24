from Accounts import Accounts

class CreditCards(Accounts):

    def __init__(self, dateOpened, bank, accountName, transactions, limit, balance, interestRate, dueDate, reportDate, minDue):
        super().__init__(dateOpened, bank, accountName, transactions)
        self.limit = limit 
        self.balance = balance 
        self.interestRate = interestRate
        self.dueDate = dueDate
        self.reportDate = reportDate
        self.minDue = minDue

    
    def getCredCard(self):
            return (
            f"{self.getAccount()}\n"
            f"Credit Balance: {self.balance}\n"
            f"Credit Limit: {self.limit}\n"
            f"Mininmum Payment Due: {self.minDue}\n"
            f"dueDate: {self.dueDate}\n"
            )
    

    def getMoreCreditCardDetails(self):
         return (
            f"Account opened: {self.dateOpened}\n"
            f"Interest Rate: {self.interestRate}\n"
            f"Monthly Report to Credit Bureaus: {self.reportDate}\n"
            )
            
            
            
             
    
