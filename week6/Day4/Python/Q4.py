import random

# Base Class 1: TradingAccount
class TradingAccount:
    def __init__(self, account_id, owner_name, balance):
        self.account_id = account_id
        self.owner_name = owner_name
        self.balance = float(balance)

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False


# Base Class 2: RiskManagement
class RiskManagement:
    def assess_portfolio_risk(self):
        return random.choice(["Low", "Medium", "High"])

    def calculate_position_size(self, symbol, price):
        if price <= 0:
            return 0
        return int(self.balance * 0.1 // price)


# Base Class 3: AnalyticsEngine
class AnalyticsEngine:
    def analyze_market_trend(self, symbol):
        return {
            "trend": random.choice(["Bullish", "Bearish", "Neutral"]),
            "confidence": round(random.uniform(0.5, 1.0), 2)
        }


# Base Class 4: NotificationSystem
class NotificationSystem:
    def __init__(self):
        self.alerts = []

    def set_price_alert(self, symbol, threshold, direction):
        self.alerts.append({"symbol": symbol, "threshold": threshold, "direction": direction})
        return True

    def get_pending_notifications(self):
        return self.alerts


# Derived Class: StockTrader
class StockTrader(TradingAccount, RiskManagement, AnalyticsEngine):
    def __init__(self, account_id, owner_name, balance):
        TradingAccount.__init__(self, account_id, owner_name, balance)


# Derived Class: CryptoTrader
class CryptoTrader(TradingAccount, RiskManagement, NotificationSystem):
    def __init__(self, account_id, owner_name, balance):
        TradingAccount.__init__(self, account_id, owner_name, balance)
        NotificationSystem.__init__(self)


# Derived Class: ProfessionalTrader (Multiple Inheritance)
class ProfessionalTrader(StockTrader, CryptoTrader):
    def __init__(self, account_id, owner_name, balance):
        StockTrader.__init__(self, account_id, owner_name, balance)
        NotificationSystem.__init__(self)

    def execute_diversified_strategy(self, portfolio):
        positions = []
        for category, symbols in portfolio.items():
            if category == "allocation":
                continue
            allocation = portfolio["allocation"].get(category, 0)
            category_balance = self.balance * allocation
            for symbol in symbols:
                price = random.uniform(100, 500)
                qty = int(category_balance * 0.1 // price)
                if qty > 0:
                    positions.append({
                        "symbol": symbol,
                        "price": round(price, 2),
                        "qty": qty
                    })
        return {
            "status": "executed",
            "positions": positions
        }