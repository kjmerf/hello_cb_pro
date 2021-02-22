class Transaction:

    def __init__(self, profile_id, side, usd, btc, fee):
        self.profile_id = profile_id
        self.side = side
        self.usd = usd
        self.btc = btc
        self.fee = fee

    def to_pg_row(self):
        return [self.profile_id] + [self.side] + [self.btc] + [self.usd]+ [self.fee]

    def __str__(self):
        if self.side == "buy":
            message = f"You paid ${self.usd:.2f}, which bought {self.btc} BTC and paid ${self.fee:.2f} in fees"
            return message
        else:
            message = f"You sold {self.btc} BTC for ${self.usd:.2f} and paid ${self.fee:.2f} in fees"
            return message
