from Accounts import Accounts 
class CheckingAccounts(Accounts):

    
    def __init__(self, dateOpened, bank, accountName, transcations, balance, accountNumber, routingNumber):
        super().__init__(dateOpened, bank, accountName, transcations)
        self.balance = balance
        self.accountNumber = accountNumber
        self.routingNumber = routingNumber


    def getBankAccount(self):
        return (
            f"{self.getAccount}"
            f"Balance: {self.balance}"
        )
    

    def getMoreBankAccountInfo(self):
        return (
            f"Account Number: {self.accountNumber}"
            f"Routing Number: {self.routingNumber}"
        )




