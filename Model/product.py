class Product:

    def __init__(self, name, amount, price):
        self.name = name
        self.amount = amount
        self.priceForItem = price

    def soldItem(self,soldAmount):
        self.amount = self.amount - soldAmount