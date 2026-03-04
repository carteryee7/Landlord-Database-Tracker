
class Payment:
    _id_counter = 1

    def __init__(self, amount: float, type: str, date: str, id=None):
        if id is None:
            self.__id = Payment._id_counter
            Payment._id_counter += 1
        else:
            self.__id = id
        self.__amount = amount
        self.__type = type
        self.__date = date

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_amount(self):
        return self.__amount

    def get_type(self):
        return self.__type

    def get_date(self):
        return self.__date