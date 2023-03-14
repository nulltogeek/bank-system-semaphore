from threading import Thread


class BankSys:
    """a class that have 2 methods create_accounts ,
    transact
    """

    def __init__(self, balance, number_of_user):
        self.balance = balance
        self.accounts = []
        self.number_of_user = number_of_user

    # 1
    def create_accounts(self):
        for i in range(self.number_of_user):
            self.accounts.append(Account(f"user {i}", i, 100))
        for i in self.accounts:
            print(f"{i.name} =====> {i.balance}")

    # classmethod because we can't pass the self object to the other class method
    @classmethod
    def transact(self, sender, receiver, amount):
        sender.withdraw(amount)
        receiver.diposite(amount)


class Account(Thread):
    def __init__(self, name, account_number, balance):
        Thread.__init__(self)
        self.name = name
        self.account_number = account_number
        self.balance = balance
        self.target = []

    def set_balance(self, balance):
        self.balance = balance

    def set_target(self, target):
        try:
            self.target.append(target)
        except Exception as err:
            raise err("only on target at a time")

    def get_balance(self):
        return self.balance

    def show_balance(self):
        print(f"{self.name} -> {self.balance}")

    def diposite(self, amount):
        try:
            self.set_balance(self.get_balance() + amount)
        except Exception as err:
            raise err("something went wrong in deposite operation")

    def withdraw(self, amount):
        try:
            self.set_balance(self.get_balance() - amount)
        except Exception as err:
            raise err("something went wrong in withdraw operation")
