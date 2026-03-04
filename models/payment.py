
class Payment:
    def __init__(self, amount: float, type: str, date: str, tenant_id: int | None = None, id: int | None = None):
        self.__id = id
        self.__tenant_id = tenant_id
        self.__amount = amount
        self.__type = type
        self.__date = date

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_tenant_id(self):
        return self.__tenant_id

    def set_tenant_id(self, tenant_id: int):
        self.__tenant_id = tenant_id

    def get_amount(self):
        return self.__amount

    def get_type(self):
        return self.__type

    def get_date(self):
        return self.__date