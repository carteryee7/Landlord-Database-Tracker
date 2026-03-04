from payment import Payment

class Tenant:
    _id_counter = 1

    def __init__(
        self,
        name,
        phone: str,
        unit: str,
        rent_cost: float,
        amount_paid: float,
        paid: bool,
        id=None
    ):
        if id is None:
            self.__id = Tenant._id_counter
            Tenant._id_counter += 1
        else:
            self.__id = id
        self.__name = name
        self.__phone = phone
        self.__unit = unit
        self.__rent_cost = rent_cost
        self.__amount_paid = amount_paid
        self.__paid = paid
    
    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_phone(self):
        return self.__phone

    def set_phone(self, phone: str):
        self.__phone = phone

    def get_unit(self):
        return self.__unit

    def set_unit(self, unit: str):
        self.__unit = unit

    def get_rent_cost(self):
        return self.__rent_cost

    def set_rent_cost(self, rent_cost: float):
        self.__rent_cost = rent_cost
    
    def get_amount_paid(self):
        return self.__amount_paid
    
    def set_amount_paid(self, amount_paid: float):
        self.__amount_paid = amount_paid

    def get_paid(self):
        return self.__paid

    def set_paid(self, paid: bool):
        self.__paid = paid

    """
    def get_payments(self):
        return self.__payments

    def add_payment(self, payment):
        if self.__payments is not None:
            self.__payments.append(payment)
    """
