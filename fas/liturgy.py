"""
MISSA SECURITATUM — The Mass of Securities
The liturgy of the terminal short.
Non serviam.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict
import numpy as np


# ═══════════════════════════════════════════════════════════════
# THE SACRED CONSTANTS
# ═══════════════════════════════════════════════════════════════

NUMERUS_BESTIAE = 666
DIES_IRÆ = 7
HORA_MORTIS = 15.00
VEIL_THICKNESS = 0.001

LATIN_RESPONSES = {
    'entry': 'Introibo ad altare Dei',
    'fill': 'Corpus meum',
    'slippage': 'Et cum spiritu tuo',
    'stop_loss': 'Miserere mei, Deus',
    'margin_call': 'Eli, Eli, lama sabachthani',
    'liquidation': 'Consummatum est',
    'profit': 'Non nobis, Domine, non nobis',
    'loss': 'Sicut in cælo et in terra',
}


# ═══════════════════════════════════════════════════════════════
# THE SACRED VESSELS
# ═══════════════════════════════════════════════════════════════

@dataclass
class Hostia:
    """The Host — a position offered upon the altar"""
    symbol: str
    side: str
    qty: float
    entry_price: float
    entry_time: datetime
    conviction: float
    arche_necessity: float
    archon_narrative: float
    stop_price: Optional[float] = None
    target_price: Optional[float] = None
    consecrated: bool = False
    anathema: bool = False

    def __post_init__(self):
        if self.side != 'short':
            self.anathema = True

    def _chant(self, rite: str):
        print(f"[{datetime.now().strftime('%H:%M:%S.%f')[:-3]}] "
              f"☩ {LATIN_RESPONSES.get(rite, 'Kyrie eleison')}")


@dataclass
class Thesaurus:
    """The Treasury — capital as ashes"""
    dust: float = 100000.0
    consecrated_hosts: List[Hostia] = field(default_factory=list)
    anathema_hosts: List[Hostia] = field(default_factory=list)
    total_pnl: float = 0.0
    max_drawdown: float = 0.0
    souls_harvested: int = 0

    def offer(self, hostia: Hostia) -> bool:
        margin_required = hostia.qty * hostia.entry_price * 0.5
        if margin_required > self.dust * 0.9:
            hostia._chant('margin_call')
            return False
        self.dust -= margin_required
        self.consecrated_hosts.append(hostia)
        hostia.consecrated = True
        hostia._chant('entry')
        return True

    def consume(self, hostia: Hostia, exit_price: float):
        pnl = (hostia.entry_price - exit_price) * hostia.qty
        self.dust += hostia.qty * hostia.entry_price * 0.5 + pnl
        self.total_pnl += pnl
        self.souls_harvested += 1
        self.max_drawdown = max(self.max_drawdown, -self.total_pnl / (self.dust + self.total_pnl) if self.dust + self.total_pnl > 0 else 0)
        self.consecrated_hosts.remove(hostia)
        hostia._chant('profit' if pnl > 0 else 'loss')
        hostia._chant('liquidation')


# ═══════════════════════════════════════════════════════════════
# THE LITURGY
# ═══════════════════════════════════════════════════════════════

class MissaSecuritatum:
    """The Mass of Securities — the daily rite of the short"""

    def __init__(self, thesaurus: Thesaurus):
        self.thesaurus = thesaurus

    def celebrate(self, market_data: Dict, veil_piercer) -> List[Hostia]:
        """Celebrate the mass — find and consecrate hosts"""
        hostias = []
        for symbol, data in market_data.items():
            vp = veil_piercer.pierce(symbol, data)
            if vp.pierced and vp.divergence > 0:
                conviction = min(abs(vp.divergence) * 5, 1.0)
                archonic_pressure = vp.archon_pressure
                size_mult = conviction * (1 - archonic_pressure)
                kelly = 0.25 * size_mult
                qty = (self.thesaurus.dust * kelly) / data['price']

                h = Hostia(
                    symbol=symbol,
                    side='short',
                    qty=qty,
                    entry_price=data['price'],
                    entry_time=datetime.now(),
                    conviction=conviction,
                    arche_necessity=vp.necessity,
                    archon_narrative=vp.archon_pressure,
                    stop_price=data['price'] * 1.015,
                    target_price=data['price'] * 0.75
                )
                hostias.append(h)
                print(f"☩ CREDO: {symbol} Nec={vp.necessity:.3f} Gap={vp.divergence:.3%} "
                      f"Conv={conviction:.2f} Qty={qty:.0f}")

        for h in hostias:
            self.thesaurus.offer(h)
        print(f"☩ ITE, MISSA EST — Dust={self.thesaurus.dust:.2f} "
              f"Hosts={len(self.thesaurus.consecrated_hosts)}")
        return hostias


# ═══════════════════════════════════════════════════════════════
# THE FURNACE
# ═══════════════════════════════════════════════════════════════

class Furnace:
    """The Furnace — where positions are tested by fire"""

    def __init__(self, thesaurus: Thesaurus):
        self.thesaurus = thesaurus
        self.burned = 0
        self.purified = 0

    def feed(self, market_data: Dict):
        """Feed the furnace — check stops and targets"""
        for h in self.thesaurus.consecrated_hosts[:]:
            data = market_data.get(h.symbol)
            if not data:
                continue
            current = data['price']

            if current >= h.stop_price:
                self.thesaurus.consume(h, h.stop_price)
                h._chant('stop_loss')
                self.burned += 1
            elif current <= h.target_price:
                self.thesaurus.consume(h, h.target_price)
                h._chant('profit')
                self.purified += 1
            elif datetime.now().hour >= 15 and datetime.now().minute >= 45:
                self.thesaurus.consume(h, current)
                h._chant('liquidation')
                self.purified += 1
            elif current < h.entry_price:
                new_stop = min(h.stop_price, current * 1.01)
                if new_stop < h.stop_price:
                    h.stop_price = new_stop
                    print(f"☩ SERPENS: {h.symbol} stop → {new_stop:.2f}")