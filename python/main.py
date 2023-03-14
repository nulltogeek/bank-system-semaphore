from bank import BankSys
from threading import Thread
import time
from collections import deque
from datetime import datetime


class CustomSemaphore:
    def __init__(self, permits=1):
        self.permits = permits
        self.buffer = deque([])
        self.online = 0

    def blocked(self):
        return len(self.buffer)

    def online(self):
        return self.online

    def take(self, process):
        self.buffer.append(process)
        self.start()

    def completed(self):
        self.online -= 1
        self.start()

    def start(self):
        if self.online == self.permits or len(self.buffer) == 0:
            return
        process = self.buffer.popleft()
        self.online += 1
        if process:
            process(self.completed())


def show_res(bank_obj):
    """just show the result after all transactions"""
    time.sleep(5)
    print("\nresult:")
    bank_obj.accounts[0].show_balance()
    bank_obj.accounts[1].show_balance()
    bank_obj.accounts[2].show_balance()
    bank_obj.accounts[3].show_balance()


def main():

    # build a bank obj
    bank_obj = BankSys(400, 4)
    bank_obj.create_accounts()

    sem = CustomSemaphore(3)

    def run1(done):
        time.sleep(2)
        bank_obj.transact(bank_obj.accounts[0], bank_obj.accounts[1], 50)
        start_time = time.time()
        time.sleep(2)
        print(
            f"Transaction has been completed in",
            "---%.2f seconds---" % (time.time() - start_time),
            f"from {bank_obj.accounts[0].name} to {bank_obj.accounts[1].name} AT\t {datetime.utcnow()}",
            sep="\t",
        )

    def run2(done):
        time.sleep(2)
        bank_obj.transact(bank_obj.accounts[1], bank_obj.accounts[2], 50)
        start_time = time.time()
        time.sleep(2)
        print(
            f"Transaction has been completed in",
            "---%.2f seconds---" % (time.time() - start_time),
            f"from {bank_obj.accounts[1].name} to {bank_obj.accounts[2].name} AT\t {datetime.utcnow()}",
            sep="\t",
        )

    def run3(done):
        time.sleep(2)
        bank_obj.transact(bank_obj.accounts[2], bank_obj.accounts[3], 50)
        start_time = time.time()
        time.sleep(2)
        print(
            f"Transaction has been completed in",
            "---%.2f seconds---" % (time.time() - start_time),
            f"from {bank_obj.accounts[2].name} to {bank_obj.accounts[3].name} AT\t {datetime.utcnow()}",
            sep="\t",
        )

    t1 = Thread(target=sem.take, args=(run1,))
    t2 = Thread(target=sem.take, args=(run2,))
    t3 = Thread(target=sem.take, args=(run3,))

    t1.start()
    t2.start()
    t3.start()

    return bank_obj


if "__main__" == __name__:
    show_res(main())
