class Account:

    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath, 'r') as file:
            self.balance = int(file.read())

    def withdraw(self, amount):
        self.balance -= amount

    def deposit(self, amount):
        self.balance += amount

    def commit(self):
        with open(self.filepath, 'w') as file:
            file.seek(0)
            file.write(str(self.balance))

class Checking(Account):

    def __init__(self, filepath, fee):
        Account.__init__(self, filepath)
        self.fee = fee

    def transfer(self, amount):
        self.balance -= amount + self.fee

acc = Checking("account/balance.txt", 100)
#acc.deposit(9000)
#acc.commit()
print("Checking account balance", acc.balance)
acc.transfer(1000)
print("Transferring ", 1000, ", operation fee is", acc.fee)
print("Balance after transfer", acc.balance)
acc.commit()
