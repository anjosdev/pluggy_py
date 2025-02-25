from .config import BASE_URL
from pluggy_py.utils.http_client import HttpClient
from pluggy_py.resources.auth import AuthResource
from pluggy_py.models.auth import AuthRequest
from pluggy_py.resources.items import ItemsResource
from pluggy_py.resources.consents import ConsentsResource
from pluggy_py.resources.accounts import AccountsResource
from pluggy_py.resources.transactions import TransactionsResource
from pluggy_py.resources.investments import InvestmentsResource
from pluggy_py.resources.identity import IdentityResource
from pluggy_py.resources.categories import CategoriesResource
from pluggy_py.resources.loans import LoansResource
from pluggy_py.resources.benefits import BenefitsResource
from pluggy_py.resources.bills import BillsResource
from pluggy_py.resources.webhooks import WebhooksResource

class PluggyClient:
    def __init__(self, client_id: str, client_secret: str, base_url: str = BASE_URL):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = base_url
        self.api_key = None

        # Create a shared HttpClient
        self._http = HttpClient(self.base_url)

    def authenticate(self):
        auth_resource = AuthResource(self._http)
        auth_response = auth_resource.create_api_key(AuthRequest(
            clientId=self.client_id,
            clientSecret=self.client_secret
        ))
        self.api_key = auth_response.apiKey

        # Once we have the api_key, instantiate the resources
        self.items = ItemsResource(self._http, self.api_key)
        self.consents = ConsentsResource(self._http, self.api_key)
        self.accounts = AccountsResource(self._http, self.api_key)
        self.transactions = TransactionsResource(self._http, self.api_key)
        self.investments = InvestmentsResource(self._http, self.api_key)
        self.identity = IdentityResource(self._http, self.api_key)
        self.categories = CategoriesResource(self._http, self.api_key)
        self.loans = LoansResource(self._http, self.api_key)
        self.benefits = BenefitsResource(self._http, self.api_key)
        self.bills = BillsResource(self._http, self.api_key)
        self.webhooks = WebhooksResource(self._http, self.api_key)
