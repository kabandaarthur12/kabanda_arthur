class BankAccount:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        """Simple deposit of one amount"""
        self.balance += amount
        return f"Deposited ${amount}"

    def deposit(self, *amounts):
        """Method overloading: can handle single or multiple deposits"""
        total = sum(amounts)
        self.balance += total
        return f"Deposited ${total}"

    def withdraw(self, amount):
        """Simple withdrawal"""
        self.balance -= amount
        return f"Withdrew ${amount}"

    def withdraw(self, amount, fee=0):
        """Method overloading: withdrawal with optional fee"""
        total = amount + fee
        self.balance -= total
        if fee:
            return f"Withdrew ${amount} with ${fee} fee"
        return f"Withdrew ${amount}"


if __name__ == "__main__":
    account = BankAccount("John")
    
    
    print(account.deposit(50, 30, 20))    
    
    print(account.withdraw(50))           
    print(account.withdraw(50, fee=5))    