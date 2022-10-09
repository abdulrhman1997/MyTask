from Model.client import *
from Model.product import *
from db import *



def main():

    print('***Hello Our Clients!***')
    namesFetch()

    name = input('Enter your name: ')
    while True:
        if(isClientExsist(name)):
            break
        else:
            print("{} isn't one of our clients, please try again!".format(name))
            name = input('Enter your name: ')

    while True:
        passwd = input('Enter your Password: ')
        if(passwdValdiate(name=name,password=passwd)):
            return name
        else:
            print('Inocrrect password, try again!')


def toBuy(clientName):
    productsFetch()
    while True:
        if(isBroke(name=clientName)):
            print("Sorry you are Broke!")
            break

        fixedName = arabic_reshaper.reshape(clientName)    # correct its shape
        fixedName = fixedName[::-1]  # slice backwards 

        print("Hello {} , your have in your account: {}".format(fixedName,clientAccount(client=clientName)))
        
        while True:
            itemCode = input('Enter the code of the item you that you would like to buy: ')
            itemCode = int(itemCode)
            theAvailableAmount = None

            if(itemCode not in range(1,5)):
                print("the Entered code is incorrect, please try again")
                continue
            else:
                theAvailableAmount = checkAmount(itemCode)
            if(theAvailableAmount==0):
                print("Sorry to tell you that! but the choosen Item has run out!, would you like to buy another thing!?")
            else:
                break

        while True:
            itemAmount = input('Enter the amount of the item that you have choosen: ')
            itemAmount = int(itemAmount)

            
            if(itemAmount>theAvailableAmount):
                answer = print("the wanted amount isn't Availabe right now!, there's only {} pieces are left, would you like to order it all? answer with yes if that so".format(checkAmount(itemCode)))
                if(answer == 'yes'):
                    totalPrice = calculate(productId=itemCode,amount=theAvailableAmount)
                    if(clientAccount(client=clientName)<totalPrice):
                        print("Sorry! you can't Afford that!")
                        break
                    else:
                        doPurchases(purchasesValue=totalPrice,clientName=clientName,itemCode=itemCode,itemAmount=theAvailableAmount)
                        break
                else:
                    break
            else:
                totalPrice = calculate(productId=itemCode,amount=itemAmount)
                if(clientAccount(client=clientName)<totalPrice):
                    print("Sorry! you can't Afford that!")
                    break
                else:
                    doPurchases(purchasesValue=totalPrice,clientName=clientName,itemCode=itemCode,itemAmount=itemAmount)
                    break

    

if __name__ == "__main__":
    runQueries()
    while True:
        name = main()
        if (name != None):
            toBuy(name)

