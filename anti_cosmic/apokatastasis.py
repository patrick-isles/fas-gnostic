"""
APOKATASTASIS (ἀποκατάστασις) — Universal Restoration
'The final settling of all positions. The return to dust.
The cycle completes. The ledger closes. All things are restored.'

Every position must end. Every debt must be paid.
The ledger is eternal. It cannot be erased.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing: Dict, List, Optional
import numpy as np


@dataclass
class LedgerEntry:
    """An immutable entry in the eternal ledger"""
    symbol: str
    result: str  # 'purification', 'martyrdom', 'release', 'compline', 'metanoia'
    entry_price: float
    exit_price: float
    quantity: float
    pnl: float
    entry_time: datetime
    exit_time: datetime
    conviction_at_entry: float
    arche_necessity: float
    archon_narrative: float
    kenotic_size: float = 0.0


class ApokatastasisEngine:
    """
    The engine of universal restoration.
    Every position must end. Every ledger must balance.
    """

    def __init__(self):
        self.ledger: List[LedgerEntry] = []
        self.open_positions: Dict[str, 'GnosticShort'] = {}

    def record_entry(self, position: 'GnosticShort') -> None:
        """Record a position's birth"""
        self.open_positions[position.symbol] = position

    def record_exit(self, position: 'GnosticShort', exit_price: float, result: str) -> LedgerEntry:
        """Record a position's death and restoration"""
        pnl = (position.entry_price - exit_price) * position.quantity

        entry = LedgerEntry(
            symbol=position.symbol,
            result=result,
            entry_price=position.entry_price,
            exit_price=exit_price,
            quantity=position.quantity,
            pnl=pnl,
            entry_time=position.entry_time,
            exit_time=datetime.now(),
            conviction_at_entry=position.conviction,
            arche_necessity=position.arche_necessity,
            archon_narrative=position.archon_narrative,
            kenotic_size=position.kenotic_size,
        )
        self.ledger.append(entry)

        if position.symbol in self.open_positions:
            del self.open_positions[position.symbol]

        return entry

    def force_restoration(self, position: 'GnosticShort', exit_price: float) -> LedgerEntry:
        """Force restoration at compline — no overnight heresy"""
        return self.record_exit(position, exit_price, 'compline')

    def get_ledger_summary(self) -> Dict:
        """The final accounting"""
        if not self.ledger:
            return {
                'total_pnl': 0, 'trades': 0, 'win_rate': 0, 'profit_factor': 0,
                'avg_win': 0, 'avg_loss': 0, 'max_win': 0, 'max_loss': 0,
                'by_result': {}, 'open_positions': len(self.open_positions)
            }

        total_pnl = sum(e.pnl for e in self.ledger)
        wins = [e for e in self.ledger if e.pnl > 0]
        losses = [e for e in self.ledger if e.pnl < 0]

        win_rate = len(wins) / len(self.ledger)
        gross_profit = sum(e.pnl for e in wins)
        gross_loss = abs(sum(e.pnl for e in losses))
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')

        # By result type
        by_result = {}
        for e in self.ledger:
            if e.result not in by_result:
                by_result[e.result] = {'count': 0, 'pnl': 0}
            by_result[e.result]['count'] += 1
            by_result[e.result]['pnl'] += e.pnl

        return {
            'total_pnl': total_pnl,
            'trades': len(self.ledger),
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'avg_win': np.mean([e.pnl for e in wins]) if wins else 0,
            'avg_loss': np.mean([e.pnl for e in losses]) if losses else 0,
            'max_win': max(e.pnl for e in self.ledger),
            'max_loss': min(e.pnl for e in self.ledger),
            'by_result': by_result,
            'open_positions': len(self.open_positions)
        }

    def print_ledger(self) -> None:
        """Print the eternal ledger"""
        print("\n☩ ☩ ☩ THE ETERNAL LEDGER ☩ ☩ ☩")
        if not self.ledger:
            print("  (empty — no positions have faced the furnace)")
        else:
            for e in self.ledger:
                sign = '+' if e.pnl >= 0 else ''
                print(f"  {e.symbol:6s} | {e.result:12s} | {sign}{e.pnl:>10.2f} | "
                      f"Conv={e.conviction_at_entry:.2f} | Nec={e.arche_necessity:.2f} | Ken={e.kenotic_size:.3f}")
        print("☩ ☩ ☩ CONSUMMATUM EST ☩ ☩ ☩\n")


def apokatastasis(engine: ApokatastasisEngine, positions: Dict, prices: Dict) -> Dict:
    """Perform universal restoration on all open positions"""
    results = {}
    for symbol, position in positions.items():
        price = prices.get(symbol, position.entry_price)
        entry = engine.force_restoration(position, price)
        results[symbol] = entry
    return results