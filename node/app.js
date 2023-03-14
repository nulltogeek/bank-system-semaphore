class Semaphore {
    constructor(max = 1) {
        this.max = max;
        this._fns = [];
        this._active = 0;
    }

    remaining() {
        return this._fns.length;
    }

    active() {
        return this._active;
    }

    take(fn) {
        this._fns.push(fn);
        this._try();
    }

    _done() {
        console.log(`active ${this._active}`);
        this._active -= 1;
        this._try();
    }

    _try() {
        if (this._active === this.max || this._fns.length === 0) return;
        let fn = this._fns.shift();
        console.log("++++++++++++++++++++++")
        console.log("+ Released a process +");
        console.log("++++++++++++++++++++++\n")
        this._active += 1;
        if (fn) fn(this._done.bind(this));
    }
}

class Bank {
    constructor(balance, numUser) {
        this.balance = balance;
        this.numUser = numUser;
        this.accounts = [];
    }

    showAccounts() {
        console.log(this.accounts);
    }
    createAccounts() {
        for (let i = 0; i < this.numUser; i++) {
            let account = new Account(i, 100);
            this.accounts.push(account);
        }
        console.log("Accounts created\n", this.accounts)
        console.log("_______________________________________________________________________________________________________________________\n")

    }
    transact(amount, sender, receiver) {
        sender.withdraw(amount);
        receiver.deposite(amount);
    }
}

class Account {
    constructor(id, balance) {
        this.id = id;
        this.balance = balance;
    }
    setBalance(balance) {
        this.balance = balance;
    }
    getBalance() {
        return this.balance;
    }
    showBalance() {
        console.log(`${this.id} --> ${this.balance}`);
    }
    deposite(amount) {
        try {
            const res = this.getBalance() + amount
            this.setBalance(res);
        } catch (error) { }
    }
    withdraw(amount) {
        try {
            const res = this.getBalance() - amount
            this.setBalance(res);
        } catch (error) { }
    }
}

// objects
const bankObject = new Bank(10000, 10);
bankObject.createAccounts();
sem = new Semaphore(1);


// orders
const run1 = (done) => {
    bankObject.transact(amount = 50, sender = bankObject.accounts[0], receiver = bankObject.accounts[1]);
    console.log(`${bankObject.accounts[0].id} ===> ${bankObject.accounts[1].id}\t\t\t\t------transaction completed at ${Date.now()}------\n`)
    console.log("_______________________________________________________________________________________________________________________\n")
    setTimeout(done, 2000);
};
const run2 = (done) => {

    console.log(`user ${bankObject.accounts[0].id} is getting his/her balance: `, bankObject.accounts[0].getBalance(), `\t------transaction completed at ${Date.now()}------\n`)
    console.log("_______________________________________________________________________________________________________________________\n")
    setTimeout(done, 2000);
}

const run3 = (done) => {
    bankObject.transact(amount = 50, sender = bankObject.accounts[2], receiver = bankObject.accounts[3]);
    console.log(`${bankObject.accounts[2].id} ===> ${bankObject.accounts[3].id}\t\t\t\t------transaction completed at ${Date.now()}------\n`)
    console.log("_______________________________________________________________________________________________________________________\n")

    setTimeout(done, 2000);

}

const run4 = (done) => {
    console.log(`user ${bankObject.accounts[3].id} is getting his/her balance: `, bankObject.accounts[3].getBalance(), `\t------transaction completed at ${Date.now()}------\n`)
    console.log("_______________________________________________________________________________________________________________________\n")
    setTimeout(done, 2000);

};
const run5 = (done) => {
    bankObject.transact(50, bankObject.accounts[3], bankObject.accounts[9])
    console.log(`${bankObject.accounts[3].id} ===> ${bankObject.accounts[9].id}\t\t\t\t------transaction completed at ${Date.now()}------\n`)
    console.log("_______________________________________________________________________________________________________________________\n")
    setTimeout(done, 2000);
};
sem.take(run1);
sem.take(run2)
sem.take(run3)
sem.take(run4)
sem.take(run5)

// const input = prompt("asds")

setTimeout(function () {
    console.log(bankObject.showAccounts());
}, 10000);