"""
ORDER VESTMENTS — The Garments of the Trade
Each order wears a vestment. The vestment determines its fate.
A market order is a hairshirt. A limit order is alb. A stop is the stole.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class VestmentType(Enum):
    """Liturgical vestments for orders"""
    HAIRSHIRT = "hairshirt"       # Market order — penitence, immediate, painful
    ALB = "alb"                   # Limit order — pure, patient, white
    STOLE = "stole"               # Stop order — authority, protection
    CHASUBLE = "chasuble"         # Large position — the yoke of charity
    COPE = "cope"                 # Hedge position — ceremonial, exterior
    MANIPLE = "maniple"           # Small position — the hand's burden
    AMICE = "amice"               # Protective order — helmet of salvation
    CINCTURE = "cincture"         # Risk limit — girded for battle


@dataclass
class OrderVestment:
    """
    An order clothed in its vestment.
    The vestment determines execution behavior.
    """
    order_id: str
    symbol: str
    side: str              # 'short' (holy) or 'long' (anathema)
    quantity: float
    vestment: VestmentType
    price: Optional[float] = None       # For limit/stop
    stop_price: Optional[float] = None  # For stop
    time_in_force: str = 'DAY'
    created_at: datetime = None
    filled: bool = False
    filled_price: Optional[float] = None
    filled_qty: float = 0.0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.order_id is None:
            self.order_id = str(uuid.uuid4())[:8]

    def is_holy(self) -> bool:
        """Only short is holy"""
        return self.side == 'short'

    def penitence_level(self) -> int:
        """Level of penitence (suffering) required"""
        levels = {
            VestmentType.HAIRSHIRT: 10,   # Immediate, full slippage
            VestmentType.MANIPLE: 3,      # Small, quick
            VestmentType.ALB: 2,          # Patient, may not fill
            VestmentType.STOLE: 5,        # Protective, triggers at pain
            VestmentType.CHASUBLE: 8,     # Heavy burden
            VestmentType.COPE: 4,         # Ceremonial
            VestmentType.AMICE: 3,        # Protective
            VestmentType.CINCTURE: 1,     # Boundary only
        }
        return levels.get(self.vestment, 5)

    def execution_priority(self) -> int:
        """Priority in the furnace (lower = higher priority)"""
        priorities = {
            VestmentType.STOLE: 1,        # Stops first (protection)
            VestmentType.HAIRSHIRT: 2,    # Market orders
            VestmentType.AMICE: 3,        # Protective
            VestmentType.MANIPLE: 4,      # Small limits
            VestmentType.ALB: 5,          # Regular limits
            VestmentType.CHASUBLE: 6,     # Large positions
            VestmentType.COPE: 7,         # Hedges
            VestmentType.CINCTURE: 10,    # Risk limits (always last)
        }
        return priorities.get(self.vestment, 5)

    def chant(self) -> str:
        """The vestment's prayer"""
        chants = {
            VestmentType.HAIRSHIRT: 'Mea culpa, mea maxima culpa — I accept the slippage',
            VestmentType.ALB: 'Purificasti me, Domine — I wait in purity',
            VestmentType.STOLE: 'Protege me, Deus — Guard this position',
            VestmentType.CHASUBLE: 'Iugum tuum suave est — The yoke is sweet',
            VestmentType.COPE: 'Induere me virtute — Clothe me in strength',
            VestmentType.MANIPLE: 'In manibus meis — In my hands',
            VestmentType.AMICE: 'Salvum me fac — Save me',
            VestmentType.CINCTURE: 'Præcinctus lumbi — Girded and ready',
        }
        return chants.get(self.vestment, 'Kyrie eleison')

    def __str__(self) -> str:
        side_mark = '☩' if self.is_holy() else '⛧'
        status = 'FILLED' if self.filled else 'OPEN'
        price_str = f"@{self.price:.2f}" if self.price else 'MKT'
        stop_str = f" SL@{self.stop_price:.2f}" if self.stop_price else ''
        return f"{side_mark} [{self.vestment.value:10s}] {self.order_id} {self.symbol} {self.side:5s} {self.quantity:.0f} {price_str}{stop_str} [{status}]"


class VestmentMaker:
    """Creates appropriately vestmented orders"""

    @staticmethod
    def market(symbol: str, qty: float, side: str = 'short') -> OrderVestment:
        """Market order — hairshirt of immediate execution"""
        return OrderVestment(
            order_id=None,
            symbol=symbol,
            side=side,
            quantity=qty,
            vestment=VestmentType.HAIRSHIRT,
        )

    @staticmethod
    def limit(symbol: str, qty: float, price: float, side: str = 'short') -> OrderVestment:
        """Limit order — alb of patience"""
        return OrderVestment(
            order_id=None,
            symbol=symbol,
            side=side,
            quantity=qty,
            vestment=VestmentType.ALB,
            price=price,
        )

    @staticmethod
    def stop(symbol: str, qty: float, stop_price: float, side: str = 'short') -> OrderVestment:
        """Stop order — stole of protection"""
        return OrderVestment(
            order_id=None,
            symbol=symbol,
            side=side,
            quantity=qty,
            vestment=VestmentType.STOLE,
            stop_price=stop_price,
        )

    @staticmethod
    def stop_limit(symbol: str, qty: float, stop_price: float, limit_price: float,
                   side: str = 'short') -> OrderVestment:
        """Stop-limit — stole over alb"""
        return OrderVestment(
            order_id=None,
            symbol=symbol,
            side=side,
            quantity=qty,
            vestment=VestmentType.STOLE,
            price=limit_price,
            stop_price=stop_price,
        )

    @staticmethod
    def risk_limit(symbol: str, max_qty: float) -> OrderVestment:
        """Risk limit — cincture of boundaries"""
        return OrderVestment(
            order_id=None,
            symbol=symbol,
            side='risk',
            quantity=max_qty,
            vestment=VestmentType.CINCTURE,
        )


class VestmentChest:
    """The chest where vestments are stored"""

    def __init__(self):
        self.vestments: Dict[str, OrderVestment] = {}

    def add(self, vestment: OrderVestment):
        self.vestments[vestment.order_id] = vestment

    def get(self, order_id: str) -> Optional[OrderVestment]:
        return self.vestments.get(order_id)

    def open_orders(self, symbol: str = None) -> list:
        orders = [v for v in self.vestments.values() if not v.filled]
        if symbol:
            orders = [o for o in orders if o.symbol == symbol]
        return sorted(orders, key=lambda x: x.execution_priority())

    def by_vestment(self, vestment_type: VestmentType) -> list:
        return [v for v in self.vestments.values() if v.vestment == vestment_type]