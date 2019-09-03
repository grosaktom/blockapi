from .services import BlockchainAPI,set_default_args_values,APIError,AddressNotExist,BadGateway,GatewayTimeOut

class BlockcypherAPI(BlockchainAPI):
    """
    Multi coins: bitcoin, litecoin, dogecoin
    API docs: https://github.com/Blockchair/Blockchair.Support/blob/master/API_DOCUMENTATION_EN.md
    Explorer: https://live.blockcypher.com
    """

    currency_id = None
    coin_symbol = None
    base_url = 'https://api.blockcypher.com/v1/'
    rate_limit = 0
    coef = None
    start_offset = 0
    max_items_per_page = None
    page_offset_step = max_items_per_page

    supported_requests = {
        # for limit and offset the second parameter 0 is for utxo
        'get_balance': '/{coin}/main/addrs/{address}',
    }

    def process_error_response(self, response):
        err = response.json().get('error')
        if 'is invalid' in err or err == 'Error: wallet not found':
            raise AddressNotExist()
        # else
        super().process_error_response(response)

    def get_balance(self):
        response = self.request(
            'get_balance',
            coin=self.coin_symbol,
            address=self.address
        )
        if not response:
            return 0

        return response['balance'] * self.coef

class BlockcypherLitecoinAPI(BlockcypherAPI):
    currency_id = 'litecoin'
    coin_symbol = 'ltc'
    coef = 1e-8


