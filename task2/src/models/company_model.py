class company_model:
    def __init__(self,
                 name: str = "",
                 inn: str = "",
                 account: str = "",
                 corr_account: str = "",
                 bik: str = "",
                 ownership: str = ""):
        self._name = ""
        self._inn = ""
        self._account = ""
        self._corr_account = ""
        self._bik = ""
        self._ownership = ""

        if name is not None and name.strip() != "":
            self.name = name
        if inn is not None and inn != "":
            self.inn = inn
        if account is not None and account != "":
            self.account = account
        if corr_account is not None and corr_account != "":
            self.corr_account = corr_account
        if bik is not None and bik != "":
            self.bik = bik
        if ownership is not None and ownership != "":
            self.ownership = ownership

    @property
    def inn(self) -> str:
        return self._inn

    @inn.setter
    def inn(self, value: str):
        if not isinstance(value, str):
            raise ValueError("ИНН должен быть строкой цифр")
        if not value.isdigit():
            raise ValueError("ИНН должен быть числом")
        if len(value) != 12:
            raise ValueError("ИНН должен содержать 12 символов")
        self._inn = value

    @property
    def account(self) -> str:
        return self._account

    @account.setter
    def account(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Счет должен быть строкой цифр")
        if not value.isdigit():
            raise ValueError("Счет должен быть числом")
        if len(value) != 11:
            raise ValueError("Счет должен содержать 11 символов")
        self._account = value

    @property
    def corr_account(self) -> str:
        return self._corr_account

    @corr_account.setter
    def corr_account(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Корр. счет должен быть строкой цифр")
        if not value.isdigit():
            raise ValueError("Корреспондентский счет должен быть числом")
        if len(value) != 11:
            raise ValueError("Корреспондентский счет должен содержать 11 символов")
        self._corr_account = value

    @property
    def bik(self) -> str:
        return self._bik

    @bik.setter
    def bik(self, value: str):
        if not isinstance(value, str):
            raise ValueError("БИК должен быть строкой цифр")
        if not value.isdigit():
            raise ValueError("БИК должен быть числом")
        if len(value) != 9:
            raise ValueError("БИК должен содержать 9 символов")
        self._bik = value

    @property
    def ownership(self) -> str:
        return self._ownership

    @ownership.setter
    def ownership(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Вид собственности должен быть строкой")
        if len(value) > 5:
            raise ValueError("Вид собственности должен содержать 5 символов")
        self._ownership = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value is None:
            return
        if value.strip() == "":
            return
        self._name = value.strip()

    def __eq__(self, other):
        if not isinstance(other, company_model):
            return False
        return (self.name == other.name and self.inn == other.inn and
                self.account == other.account and self.corr_account == other.corr_account and
                self.bik == other.bik and self.ownership == other.ownership)

    def __repr__(self):
        return f"company_model(name='{self._name}', inn='{self._inn}')"
