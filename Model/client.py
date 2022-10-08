class Client:

    def __init__(self, name, password, accountValue):
        self.name = name
        self.password = password
        self.accountValue = accountValue
    
    def passwordValdiation(self, inputPassword):
        if(self.password != inputPassword):
            return False
        else:
            return True

    def isAfforadable(self, itemValue, amountCount):
        if(itemValue * amountCount > self.accountValue):
            return False
        else:
            return True
    
    def doPaymentProcess(self, paymentValue):
        self.accountValue = self.accountValue - paymentValue
        print("you're all set your purchase was successful")