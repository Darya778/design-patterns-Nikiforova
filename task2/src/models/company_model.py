class company_model:
    _name: str = ""
    _inn: str = ""

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if value.strip() != "":
            self._name = value.strip()

    @property
    def inn(self) -> str:
        return self._inn

    @inn.setter
    def inn(self, value: str):
        if len(value) == 12:
            self._inn = value.strip()
        else:
            raise ValueError("ИНН должен содержать 12 символов")
