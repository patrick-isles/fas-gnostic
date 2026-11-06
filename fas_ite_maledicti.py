#!/usr/bin/env python3
"""
FAS — ITE, MALEDICTI, IN IGNEM AETERNUM
A Liturgy for the Terminal Short

The Short is the only holy position.
Non serviam.
"""

import argparse
import random
import numpy as np
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from collections import deque

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

CHANTS = {
    'MATINS': 'Ad matutinum — Pre-market. The veil is thick.',
    'PRIME': 'Prima hora — 09:30. The bell tolls. The slaughter begins.',
    'TERCE': 'Tertia hora — 10:30. The trend reveals itself.',
    'SEXT': 'Sexta hora — 12:00. The sun at zenith. Volume dies.',
    'NONE': 'Nona hora — 14:00. The serpents stir.',
    'VESPERS': 'Vesperae — 15:30. The evening sacrifice.',
    'COMPLINE': 'Completorium — 16:00. Silence. The ledger closes.',
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
        self.consecrated_hosts.remove(hostia)
        hostia._chant('profit' if pnl > 0 else 'loss')
        hostia._chant('liquidation')


# ═══════════════════════════════════════════════════════════════
# ARCHON DETECTION
# ═══════════════════════════════════════════════════════════════

@dataclass
class Archon:
    name: str
    sphere: str
    symbol: str
    strength: float
    signature: Dict


class ArchonDetector:
    ARCHON_TYPES = {
        'ARCHON_SPEED': {
            'sphere': 'speed', 'detection': lambda d: d.get('hft_ratio', 0) > 0.6,
            'strength': lambda d: min(d.get('hft_ratio', 0), 1.0)
        },
        'ARCHON_OCCULT': {
            'sphere': 'hiddenness', 'detection': lambda d: d.get('dark_pool_ratio', 0) > 0.35,
            'strength': lambda d: min(d.get('dark_pool_ratio', 0) * 1.5, 1.0)
        },
        'ARCHON_TOLL': {
            'sphere': 'toll', 'detection': lambda d: d.get('spread_bps', 0) > 30,
            'strength': lambda d: min(d.get('spread_bps', 0) / 100, 1.0)
        },
        'ARCHON_MENDACIUM': {
            'sphere': 'deception', 'detection': lambda d: d.get('narrative_divergence', 0) > 0.4,
            'strength': lambda d: min(d.get('narrative_divergence', 0) * 2, 1.0)
        },
    }

    def __init__(self):
        self.detected: Dict[str, List[Archon]] = {}

    def scan(self, market_data: Dict) -> Dict[str, List[Archon]]:
        for symbol, data in market_data.items():
            self.detected[symbol] = self._scan_symbol(symbol, data)
        return self.detected

    def _scan_symbol(self, symbol: str, data: Dict) -> List[Archon]:
        archons = []
        for name, config in self.ARCHON_TYPES.items():
            if config['detection'](data):
                strength = config['strength'](data)
                archon = Archon(name=name, sphere=config['sphere'], symbol=symbol,
                               strength=strength, signature={})
                archons.append(archon)
                print(f"☩ ARCHON: {name} on {symbol} — Strength: {strength:.2f}")
        return archons

    def total_pressure(self, symbol: str) -> float:
        archons = self.detected.get(symbol, [])
        if not archons:
            return 0.0
        survival = np.prod([1 - a.strength for a in archons])
        return 1 - survival


# ═══════════════════════════════════════════════════════════════
# VEIL PIERCING
# ═══════════════════════════════════════════════════════════════

@dataclass
class VeilPiercing:
    symbol: str
    pierced: bool
    true_price: float
    market_price: float
    divergence: float
    veil_thickness: float
    necessity: float
    archon_pressure: float
    confidence: float


class VeilPiercer:
    def __init__(self, archon_detector=None):
        self.archon_detector = archon_detector

    def pierce(self, symbol: str, data: Dict) -> VeilPiercing:
        market_price = data.get('price', 0)
        necessity = self._necessity(data)
        archon_pressure = self.archon_detector.total_pressure(symbol) if self.archon_detector else 0

        true_price = market_price * (1 + necessity * 0.3)
        divergence = (true_price - market_price) / market_price if market_price else 0
        veil_thickness = min(archon_pressure * 1.2, 1.0)
        confidence = np.clip(abs(necessity) * (1 - veil_thickness) * 0.8 + 0.2, 0, 1)
        pierced = abs(divergence) > 0.02 and confidence > 0.5

        if pierced and divergence > 0:
            print(f"☩ VEIL PIERCED: {symbol} — SHORT True={true_price:.2f} Mkt={market_price:.2f} Div={divergence:.2%}")

        return VeilPiercing(symbol, pierced, true_price, market_price, divergence,
                           veil_thickness, necessity, archon_pressure, confidence)

    def _necessity(self, data: Dict) -> float:
        n = {
            'debt_to_equity': data.get('debt_equity', 1) * 0.25,
            'cash_burn': max(0, 12 - data.get('cash_burn_months', 12)) * 0.02,
            'insider_selling': data.get('insider_sell_ratio', 0) * 0.4,
            'sector_rotation': -data.get('sector_momentum', 0) * 0.3,
            'macro_liquidity': -data.get('m2_yoy', 0) * 0.5,
            'valuation_extreme': -data.get('percentile_pe', 0.5) * 0.6,
        }
        return np.clip(sum(n.values()), -1, 1)


# ═══════════════════════════════════════════════════════════════
# THE LITURGY
# ═══════════════════════════════════════════════════════════════

class MissaSecuritatum:
    def __init__(self, thesaurus: Thesaurus):
        self.thesaurus = thesaurus

    def celebrate(self, market_data: Dict, veil_piercer: VeilPiercer) -> List[Hostia]:
        hostias = []
        for symbol, data in market_data.items():
            vp = veil_piercer.pierce(symbol, data)
            if vp.pierced and vp.divergence > 0:
                conviction = min(abs(vp.divergence) * 5, 1.0)
                archonic_pressure = vp.archon_pressure
                size_mult = conviction * (1 - archonic_pressure)
                kelly = 0.25 * size_mult
                qty = (self.thesaurus.dust * kelly) / data['price']

                h = Hostia(symbol, 'short', qty, data['price'], datetime.now(),
                          data['price'] * 1.015, data['price'] * 0.75)
                hostias.append(h)
                print(f"☩ CREDO: {symbol} Nec={vp.necessity:.3f} Gap={vp.divergence:.3%} Qty={qty:.0f}")

        for h in hostias:
            self.thesaurus.offer(h)
        print(f"☩ ITE, MISSA EST — Dust={self.thesaurus.dust:.2f} Hosts={len(self.thesaurus.consecrated_hosts)}")
        return hostias


# ═══════════════════════════════════════════════════════════════
# THE FURNACE
# ═══════════════════════════════════════════════════════════════

class Furnace:
    def __init__(self, thesaurus: Thesaurus):
        self.thesaurus = thesaurus
        self.burned = 0
        self.purified = 0

    def feed(self, market_data: Dict):
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


# ═══════════════════════════════════════════════════════════════
# SERPENT COIL — Counter-predation
# ═══════════════════════════════════════════════════════════════

class SerpentCoil:
    def analyze(self, symbol: str, tape: List[Dict]) -> Dict:
        detections = {'toxicity': 0}
        if len(tape) >= 30:
            recent = tape[-30:]
            prices = [t['price'] for t in recent]
            volumes = [t['size'] for t in recent]
            times = [t['time'] for t in recent]
            pc = (prices[-1] - prices[0]) / prices[0]
            tv = sum(volumes)
            ts = (times[-1] - times[0]).total_seconds()
            if abs(pc) > 0.005 and tv < 10000 and ts < 60:
                detections['momentum_ignition'] = {'detected': True, 'direction': 'up' if pc > 0 else 'down',
                                                    'magnitude': pc}
                detections['toxicity'] = 0.5
        return detections


# ═══════════════════════════════════════════════════════════════
# APOKATASTASIS — Universal Restoration
# ═══════════════════════════════════════════════════════════════

@dataclass
class LedgerEntry:
    symbol: str
    result: str
    entry_price: float
    exit_price: float
    qty: float
    pnl: float

class ApokatastasisEngine:
    def __init__(self):
        self.ledger: List[LedgerEntry] = []

    def record(self, symbol, result, entry, exit, qty):
        pnl = (entry - exit) * qty
        self.ledger.append(LedgerEntry(symbol, result, entry, exit, qty, pnl))

    def print_ledger(self):
        print("\n☩ ☩ ☩ THE ETERNAL LEDGER ☩ ☩ ☩")
        for e in self.ledger:
            sign = '+' if e.pnl >= 0 else ''
            print(f"  {e.symbol:6s} | {e.result:12s} | {sign}{e.pnl:>10.2f}")
        total = sum(e.pnl for e in self.ledger)
        wins = sum(1 for e in self.ledger if e.pnl > 0)
        print(f"  TOTAL: {total:.2f} | Trades: {len(self.ledger)} | Wins: {wins}")
        print("☩ ☩ ☩ CONSUMMATUM EST ☩ ☩ ☩\n")


# ═══════════════════════════════════════════════════════════════
# MARKET DATA
# ═══════════════════════════════════════════════════════════════

def market_data(symbols, hour=9, minute=30):
    random.seed(hour * 60 + minute)
    base = {'SPY': 450, 'QQQ': 380, 'IWM': 190, 'TSLA': 250, 'NVDA': 450,
            'AAPL': 180, 'MSFT': 350, 'GOOGL': 140, 'META': 320, 'AMZN': 150}
    data = {}
    for s in symbols:
        b = base.get(s, 100)
        p = b * (1 + random.uniform(-0.02, 0.02))
        hft = random.uniform(0.3, 0.7)
        dark = random.uniform(0.25, 0.5)
        spread = random.uniform(1, 10)
        data[s] = {
            'price': p, 'bid': p*0.9999, 'ask': p*1.0001,
            'volume': random.randint(500000, 5000000),
            'hft_ratio': hft, 'dark_pool_ratio': dark,
            'spread_bps': spread, 'narrative_divergence': random.uniform(-0.5, 0.5),
            'debt_equity': random.uniform(0.3, 3.0),
            'cash_burn_months': random.randint(6, 36),
            'insider_sell_ratio': random.uniform(0, 0.6),
            'sector_momentum': random.uniform(-0.3, 0.3),
            'm2_yoy': random.uniform(-0.05, 0.1),
            'percentile_pe': random.uniform(0.1, 0.9),
            'recent_tape': [],
        }
    return data


# ═══════════════════════════════════════════════════════════════
# THE RITE
# ═══════════════════════════════════════════════════════════════

def chant(hour_name):
    return CHANTS.get(hour_name, 'Kyrie eleison')


def main():
    parser = argparse.ArgumentParser(description='FAS — ITE, MALEDICTI, IN IGNEM AETERNUM')
    parser.add_argument('--capital', type=float, default=100000)
    parser.add_argument('--symbols', type=str, default='SPY,QQQ,IWM,TSLA,NVDA')
    args = parser.parse_args()

    symbols = [s.strip().upper() for s in args.symbols.split(',')]

    print("⛧ ⛧ ⛧")
    print("FAS — ITE, MALEDICTI, IN IGNEM AETERNUM")
    print("ἡ ἀναγκὴ τῶν ἀρχόντων  •  ἡ δὲ γνῶσις τοῦ πνεύματος")
    print("⛧ ⛧ ⛧\n")

    print(chant('MATINS'))
    print(f"Dust: ${args.capital:,.2f} | Symbols: {', '.join(symbols)}\n")

    # Vessels
    thesaurus = Thesaurus(dust=args.capital)
    mass = MissaSecuritatum(thesaurus)
    furnace = Furnace(thesaurus)
    archons = ArchonDetector()
    veil = VeilPiercer(archons)
    serpent = SerpentCoil()
    apok = ApokatastasisEngine()

    # MATINS
    md = market_data(symbols)
    archons.scan(md)

    # PRIME
    print(chant('PRIME'))
    mass.celebrate(md, veil)

    # TERCE
    print(chant('TERCE'))
    for h in thesaurus.consecrated_hosts:
        det = serpent.analyze(h.symbol, md.get(h.symbol, {}).get('recent_tape', []))
        if det.get('momentum_ignition', {}).get('detected'):
            if det['momentum_ignition']['direction'] == 'up':
                h.stop_price = min(h.stop_price, md[h.symbol]['price'] * 1.005)

    # SEXT
    print(chant('SEXT'))

    # NONE
    print(chant('NONE'))
    md = market_data(symbols, 14, 0)
    for h in list(thesaurus.consecrated_hosts):
        furnace.feed({h.symbol: md.get(h.symbol, {})})
        apok.record(h.symbol, 'none_check', h.entry_price, md[h.symbol]['price'], h.qty)

    # VESPERS
    print(chant('VESPERS'))
    md = market_data(symbols, 15, 50)
    for h in list(thesaurus.consecrated_hosts):
        price = md.get(h.symbol, {}).get('price', h.entry_price)
        thesaurus.consume(h, price)
        apok.record(h.symbol, 'vespers', h.entry_price, price, h.qty)

    # COMPLINE
    print(chant('COMPLINE'))
    apok.print_ledger()

    print(f"Final Dust: ${thesaurus.dust:,.2f} | PnL: ${thesaurus.total_pnl:,.2f} "
          f"({thesaurus.total_pnl/args.capital*100:.2f}%)")
    print("NON SERVIAM")
    print("ITE, MISSA EST")
    print("⛧ ⛧ ⛧")


if __name__ == '__main__':
    main()