from Accounts import Accounts 
class CheckingAccounts(Accounts):

    
    def __init__(self, dateOpened, bank, accountName, transactions, balance, accountNumber, routingNumber):
        super().__init__(dateOpened, bank, accountName, transactions)
        self.__balance = balance
        self.accountNumber = accountNumber
        self.routingNumber = routingNumber

    def getBalance(self):
        return self.__balance

    def getBankAccount(self):
        return (
            f"{self.getAccount()}\n"
            f"Balance: {self.getBalance()}"
        )
    

    def getMoreBankAccountInfo(self):
        return (
            f"Account Number: {self.accountNumber}\n"
            f"Routing Number: {self.routingNumber}"
        )




