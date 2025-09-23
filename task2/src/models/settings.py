from src.models.company_model import company_model

class Settings:
    def __init__(self, company: company_model, log_level: str = "INFO"):
        if not isinstance(company, company_model):
            raise ValueError("company должен быть экземпляром company_model")
        self.company = company
        self.log_level = log_level

    def __repr__(self):
        return f"Settings(company={repr(self.company)}, log_level='{self.log_level}')"
