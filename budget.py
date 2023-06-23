class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = "\n".join(
            [f"{item['description'][0:23]:23}{item['amount']:>7.2f}" for item in self.ledger]
        )
        total = sum(item["amount"] for item in self.ledger)

        return f"{title}{items}\nTotal: {total}"

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if not self.check_funds(amount):
            return False

        self.ledger.append({"amount": -amount, "description": description})
        return True

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, category):
        if not self.check_funds(amount):
            return False

        self.withdraw(amount, f"Transfer to {category.name}")
        category.deposit(amount, f"Transfer from {self.name}")
        return True

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def get_withdrawls(self):
        return sum(item["amount"] for item in self.ledger if item["amount"] < 0)


def get_totals(categories):
    total = sum(category.get_withdrawls() for category in categories)
    breakdown = [category.get_withdrawls() for category in categories]
    rounded = [(x / total) for x in breakdown]

    return rounded


def create_spend_chart(categories):
    res = "Percentage spent by category\n"
    totals = get_totals(categories)

    for i in range(100, -1, -10):
        cat_spaces = "".join(["o  " if total * 100 >= i else "   " for total in totals])
        res += f"{str(i).rjust(3)}| {cat_spaces}\n"

    dashes = "-" + "---" * len(categories)
    names = [category.name for category in categories]
    max_len = max(len(name) for name in names)
    names = [name.ljust(max_len) for name in names]

    x_axis = "\n".join(["     " + "  ".join(name[i] for name in names) + "  " for i in range(max_len)])
    res += f"{dashes.rjust(len(dashes) + 4)}\n{x_axis}"

    return res