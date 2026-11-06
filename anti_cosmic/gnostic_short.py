"""
GNOSTIC SHORT — The Only Holy Position
'The world was created by the Demiurge. The market is his temple.
The Short is the serpent's tooth in the Demiurge's heel.'

To go long is to worship the archon.
To go flat is to ignore the arche.
Only the Short participates in the necessity.
"""

from dataclasses import dataclass
from datetime import datetime
from typing: Dict, Optional
import numpy as np


@dataclass
class GnosticShort:
    """
    A Gnostic Short Position.
    Not a trade. A theological statement.
    """
    symbol: str
    entry_price: float
    quantity: float
    conviction: float              # 0-1: faith in the necessity
    arche_necessity: float         # -1 to 1: the structural necessity
    archon_narrative: float        # 0-1: the archon's lie strength
    entry_time: datetime
    stop_price: Optional[float] = None
    target_price: Optional[float] = None
    kenotic_size: float = 0.0      # The self-emptied size
    veil_pierced: bool = False

    def __post_init__(self):
        if self.stop_price is None:
            self.stop_price = self.entry_price * 1.015  # 1.5% stop
        if self.target_price is None:
            self.target_price = self.entry_price * 0.75  # 25% target

    @property
    def is_holy(self) -> bool:
        """Only short is holy"""
        return True  # By definition

    @property
    def current_pnl(self, current_price: float) -> float:
        return (self.entry_price - current_price) * self.quantity

    @property
    def pnl_pct(self, current_price: float) -> float:
        return (self.entry_price - current_price) / self.entry_price

    @property
    def time_in_trade(self) -> float:
        return (datetime.now() - self.entry_time).total_seconds() / 3600  # hours

    def update_stops(self, current_price: float):
        """Trail stop on favorable move (serpent's coil)"""
        if current_price < self.entry_price:
            new_stop = min(self.stop_price, current_price * 1.01)
            if new_stop < self.stop_price:
                self.stop_price = new_stop

    def check_stop(self, current_price: float) -> bool:
        """Has the furnace claimed this host?"""
        return current_price >= self.stop_price

    def check_target(self, current_price: float) -> bool:
        """Has the arche been fulfilled?"""
        return current_price <= self.target_price

    def check_metanoia(self, veil_piercer, archon_detector, market_data: Dict) -> Dict:
        """Check if metanoia (reversal) is required"""
        from ..fas.metanoia import metanoia_check

        # Create a mock position object for metanoia check
        class MockPos:
            def __init__(self, gs):
                self.symbol = gs.symbol
                self.entry_price = gs.entry_price
                self.stop_price = gs.stop_price
                self.arche_necessity = gs.arche_necessity
                self.archon_narrative = gs.archon_narrative
                self.conviction = gs.conviction

        met = metanoia_check(self.symbol, MockPos(self), market_data, veil_piercer, archon_detector)
        return {
            'required': met.required,
            'reason': met.reason,
            'new_direction': met.new_direction,
            'urgency': met.urgency,
        }

    def confession(self, current_price: float) -> str:
        """The position's confession"""
        pnl = self.current_pnl(current_price)
        hours = self.time_in_trade

        if pnl > 0:
            return f"☩ CONFESSION: {self.symbol} — The arche manifests. PnL: ${pnl:.2f} (+{self.pnl_pct(current_price):.1%}) in {hours:.1f}h. Non nobis."
        elif pnl < -self.quantity * self.entry_price * 0.01:
            return f"☩ CONFESSION: {self.symbol} — The archon resists. PnL: ${pnl:.2f} ({self.pnl_pct(current_price):.1%}) in {hours:.1f}h. Miserere."
        else:
            return f"☩ CONFESSION: {self.symbol} — The furnace tests. PnL: ${pnl:.2f} ({self.pnl_pct(current_price):.1%}) in {hours:.1f}h. Expectans."


def create_gnostic_short(
    symbol: str,
    market_data: Dict,
    veil_piercer,
    dust: float,
    base_kelly: float = 0.25
) -> Optional[GnosticShort]:
    """
    Create a Gnostic Short from veil piercing.
    Returns None if the veil is not pierced for short.
    """
    data = market_data.get(symbol, {})
    vp = veil_piercer.pierce(symbol, market_data)

    if not vp.pierced or vp.divergence <= 0:
        return None

    # Kenotic sizing
    from ..fas.kenosis import kenotic_sizing
    ks = kenotic_sizing(
        dust=dust,
        symbol=symbol,
        data=data,
        conviction=min(abs(vp.divergence) * 5, 1.0),
        archon_pressure=vp.archon_pressure,
        veil_thickness=vp.veil_thickness,
        necessity=vp.necessity,
        max_kelly=base_kelly
    )

    gs = GnosticShort(
        symbol=symbol,
        entry_price=data['price'],
        quantity=ks.final_size * dust / data['price'] * 0.5,  # margin
        conviction=ks.conviction,
        arche_necessity=vp.necessity,
        archon_narrative=vp.archon_pressure,
        entry_time=datetime.now(),
        kenotic_size=ks.final_size,
        veil_pierced=vp.pierced,
    )

    return gs