import json
import configparser
from dataclasses import dataclass
from datetime import datetime

import bitcoinaddress
from dateutil.tz import tzutc
import blockcypher as bc
from bitcoinaddress import Wallet
# from bitcoin import *

@dataclass
class Payment:
    amount: int
    created: str = None
    success: bool = False

    config = configparser.ConfigParser()
    config.read("bot.ini")

    def create(self):
        current_time = datetime.now(tz=tzutc())
        self.created = current_time.isoformat()

    # generating new address for accepting bitcoin
    def generate_new_address(self):
        # this is for real bitcoin address
        # address = bc.generate_new_address(api_key=self.config["payments"]["blockcypher_token"])

        # this is for testnet address
        wallet = Wallet(testnet=True)
        wallet = wallet.address.__dict__["testnet"].__dict__
        address = wallet["pubaddrtb1_P2WSH"]
        return address

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
