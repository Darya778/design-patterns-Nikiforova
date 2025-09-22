class Settings:
    def __init__(self, name: str, inn: str, account: str, corr_account: str,
                 bik: str, ownership: str):
        self.name = name
        self.inn = inn
        self.account = account
        self.corr_account = corr_account
        self.bik = bik
        self.ownership = ownership

    @property
    def inn(self) -> str:
        return self._inn

    @inn.setter
    def inn(self, value: str):
        if len(value) != 12:
            raise ValueError("ИНН должен содержать 12 символов")
        self._inn = value

    @property
    def account(self) -> str:
        return self._account

    @account.setter
    def account(self, value: str):
        if len(value) != 11:
            raise ValueError("Счет должен содержать 11 символов")
        self._account = value

    @property
    def corr_account(self) -> str:
        return self._corr_account

    @corr_account.setter
    def corr_account(self, value: str):
        if len(value) != 11:
            raise ValueError("Корреспондентский счет должен содержать 11 символов")
        self._corr_account = value

    @property
    def bik(self) -> str:
        return self._bik

    @bik.setter
    def bik(self, value: str):
        if len(value) != 9:
            raise ValueError("БИК должен содержать 9 символов")
        self._bik = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value.strip() == "":
            raise ValueError("Наименование не может быть пустым")
        self._name = value.strip()

    @property
    def ownership(self) -> str:
        return self._ownership

    @ownership.setter
    def ownership(self, value: str):
        if len(value) != 5:
            raise ValueError("Вид собственности должен содержать 5 символов")
        self._ownership = value
