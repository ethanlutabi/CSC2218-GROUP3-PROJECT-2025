import json
import os
from domain.interest.interest_strategy import InterestStrategy
from domain.interest.savings_interest import SavingsInterestStrategy
from domain.interest.checking_interest import CheckingInterestStrategy

from application.interest.interest_strategy_interface import InterestStrategyRepositoryInterface


class ConfigInterestStrategyRepository(InterestStrategyRepositoryInterface):
    """
    Retrieves InterestStrategy instances based on a strategy ID,
    loading rates from an external JSON configuration file.
    """
    def __init__(self, config_path: str = None):
        path_env = os.getenv("INTEREST_CONFIG_PATH")
        self.config_path = config_path or path_env or "config/interest_rates.json"
        self._rates = self._load_rates()
        
    def _load_rates(self) -> dict:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Interest rates file not found at {self.config_path}")
        with open(self.config_path, 'r') as f:
            data = json.load(f)
        return data

    def get_strategy(self, strategy_id: str) -> InterestStrategy:
        rate = self._rates.get(strategy_id)
        if rate is None:
            raise ValueError(f"Unknown interest strategy: {strategy_id}")
        if strategy_id == "savings":
            return SavingsInterestStrategy(rate)
        if strategy_id == "checking":
            return CheckingInterestStrategy(rate)
        raise ValueError(f"Strategy not implemented for: {strategy_id}")