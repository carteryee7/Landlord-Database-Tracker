from models.payment import Payment

class Tenant:
    def __init__(self, name, phone: str, unit: str, rent_cost: float, paid: bool, payments: list[Payment] = []):
        self.name = name
        self.phone = phone
        self.unit = unit
        self.rent_cost = rent_cost
        self.paid = paid
        self.payments = payments