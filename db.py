import sqlite3
import hashlib
import arabic_reshaper

con = sqlite3.connect('factory.db')

mycursor = con.cursor()

#encrypt the password
def hashing(pwd):
    hash_object = hashlib.md5(bytes(str(pwd), encoding='utf-8'))
    hex_dig= hash_object.hexdigest()
    return hex_dig

#check if the entered password is correct
def passwdValdiate(name,password):
    try:
        mycursor.execute("select passwd from clients where name=?",(name,))
        data=mycursor.fetchone()
        if hashing(password) != data[0]: 
            return False
        else :
            return True
    except Exception as e:
         return {'Error',str(e)}

#show the Factory clients
def namesFetch():
    for name in mycursor.execute('''SELECT name FROM clients'''):
        reshaped_text = arabic_reshaper.reshape(*name)    # correct its shape
        rev_text = reshaped_text[::-1]  # slice backwards 
        # bidi_text = get_display(reshaped_text)           # correct its direction
        print(rev_text)

#check if the input name is among the current clients
def isClientExsist(name):
    try:
        mycursor.execute("select 1 from clients where name=?",(name,))
        data=mycursor.fetchone()
        if data != None: 
            return True
        else :
            return False
    except Exception as e:
         return {'Error',str(e)}

#check if the client whether broke or has money to shop
def isBroke(name):
    try:
        mycursor.execute("select accountValue from clients where name=?",(name,))
        data=mycursor.fetchone()
        if data[0] == 0: 
            return True
        else :
            return False # data[0]
    except Exception as e:
         return {'Error',str(e)}

#show the products and its details
def productsFetch():
    print("Code     name      amount      price")
    for product in mycursor.execute('''SELECT * FROM products'''):
        print(product[0],product[1],product[2],product[3])


#return the value of the client's account
def clientAccount(client):
    try:
        mycursor.execute("select accountValue from clients where name=?",(client,))
        data=mycursor.fetchone()
        return data[0]
    except Exception as e:
         return {'Error',str(e)}

#return the available amount for a specific product using its id
def checkAmount(id):
    try:
        mycursor.execute("select amount from products where id=?",(id,))
        data=mycursor.fetchone()
        return data[0]
    except Exception as e:
         return {'Error',str(e)}

#return the value of the purchases that the client want to do
def calculate(productId,amount):
    try:
        mycursor.execute("select price from products where id=?",(productId,))
        data=mycursor.fetchone()
        totalPrice = data[0] * amount
        return totalPrice
    except Exception as e:
         return {'Error',str(e)}

#do the purchases process and update the account value of the client and the left amount of the product 
def doPurchases(purchasesValue,clientName,itemCode,itemAmount):

    mycursor.execute("select accountValue from clients where name=?",(clientName,))
    data = mycursor.fetchone()
    acountValue = data[0]

    mycursor.execute("select amount from products where id=?",(itemCode,))
    data = mycursor.fetchone()
    amount = data[0]

    newAccountValue = acountValue - purchasesValue
    newAmount = amount - itemAmount

    mycursor.execute("update clients set accountValue = ? where name = ?",(newAccountValue,clientName))
    mycursor.execute("update products set amount = ? where id = ?",(newAmount,itemCode))

    mycursor.execute("select id from clients where name=?",(clientName,))
    id = mycursor.fetchone()
    clientId = id[0]
    mycursor.execute("Insert or ignore into  purchases values (?,?,?)",(clientId,itemCode,purchasesValue))

    con.commit()

    print("your purchase was all set\nBuy More!\n")


def runQueries():

    # Creating Tables of the database
    mycursor.execute('''CREATE TABLE IF NOT EXISTS clients (id integer PRIMARY KEY, name text, passwd text, accountValue real)''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS products (id integer PRIMARY KEY, name text, amount integer, price real)''')

    mycursor.execute('''CREATE TABLE IF NOT EXISTS purchases (clientId integer, productId integer, price real)''')

    #inserting the data of the clients

    mycursor.execute("Insert or ignore into  clients values (?,?,?,?)",(1, 'خالد مسعود',hashing('khaled123'),100))

    mycursor.execute("Insert or ignore into  clients values (?,?,?,?)",(2, 'أحمد الحجي', hashing('Ahmet123'), 120))

    mycursor.execute("Insert or ignore into  clients values (?,?,?,?)",(3, 'سامر المعلب', hashing('Samer123'), 80))

    mycursor.execute("Insert or ignore into  clients values (?,?,?,?)",(4, 'مطيع الخالد', hashing('Moteaa123'), 60))

    #inserting the data of products

    mycursor.execute('''INSERT OR IGNORE INTO products VALUES (1, 'Soup', 15, 3)''')

    mycursor.execute('''INSERT OR IGNORE INTO products VALUES (2, 'Washing liquid', 10, 4)''')

    mycursor.execute('''INSERT OR IGNORE INTO products VALUES (3, 'Cleaning detergent', 7, 6)''')

    mycursor.execute('''INSERT OR IGNORE INTO products VALUES (4, 'Shampoo', 20, 2)''')

    con.commit()

