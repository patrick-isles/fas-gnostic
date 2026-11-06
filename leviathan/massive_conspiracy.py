"""
MASSIVE CONSPIRACY AGAINST ALL LIFE
'The market is a conspiracy. Every tick is a lie agreed upon.'

The daily office of the conspiracy:
- MATINS: Reconnaissance — scan for archons
- PRIME: The bell tolls — enter positions
- TERCE: The serpent coils — counter-predation
- SEXT: The sun at zenith — silence
- NONE: The afternoon watch — monitor
- VESPERS: The evening sacrifice — forced liquidation
- COMPLINE: Night prayer — the ledger closes
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from collections import deque
import numpy as np


@dataclass
class ConspiracyState:
    """The state of the massive conspiracy"""
    hour: str = 'MATINS'
    archons_detected: Dict = field(default_factory=dict)
    veil_piercings: Dict = field(default_factory=dict)
    serpent_detections: List = field(default_factory=list)
    bathymetric_pressures: Dict = field(default_factory=dict)
    ledger: List = field(default_factory=list)


class GnosticShort:
    """Local definition to avoid circular imports"""
    def __init__(self, symbol, entry, qty, conviction, necessity, arche):
        self.symbol = symbol
        self.entry_price = entry
        self.quantity = qty
        self.conviction = conviction
        self.arche_necessity = necessity
        self.archon_narrative = arche
        self.entry_time = datetime.now()
        self.stop_price = entry * 1.015
        self.target_price = entry * 0.75


class MassiveConspiracy:
    """
    The daily office of the massive conspiracy against all life.
    Every market hour is a canonical hour. Every trade is a rite.
    """

    def __init__(self):
        self.state = ConspiracyState()
        self.liturgy = None
        self.veil_piercer = None
        self.archon_detector = None
        self.serpent = None
        self.apokatastasis = None

    # ═══════════════════════════════════════════════════════════
    # THE DAILY OFFICE
    # ═══════════════════════════════════════════════════════════

    def matins(self, market_data: Dict):
        """MATINS — Pre-dawn reconnaissance. Scan for archons."""
        self.state.hour = 'MATINS'
        print("☩ MATINS — The abyss gazes back. Scanning for archons...")
        self.state.archons_detected = self.archon_detector.scan(market_data)

    def prime(self, market_data: Dict):
        """PRIME — 09:30. The bell tolls. Enter the short."""
        self.state.hour = 'PRIME'
        print("☩ PRIME — The bell tolls. Non serviam.")
        if self.liturgy:
            hosts = self.liturgy.celebrate(market_data, self.veil_piercer)
            for h in hosts:
                self.apokatastasis.record_entry(h)

    def terce(self, market_data: Dict):
        """TERCE — 10:30. The serpent coils. Counter-predation."""
        self.state.hour = 'TERCE'
        print("☩ TERCE — The serpent coils.")
        if self.liturgy:
            self._terce_coil(market_data)

    def sext(self, market_data: Dict):
        """SEXT — 12:00. The sun at zenith. Volume dies. We wait."""
        self.state.hour = 'SEXT'
        print("☩ SEXT — The sun at zenith. Volume dies. We wait.")

    def none(self, market_data: Dict):
        """NONE — 14:00. The afternoon watch. Serpents stir."""
        self.state.hour = 'NONE'
        print("☩ NONE — The serpents stir.")
        if self.liturgy:
            self._none_watch(market_data)

    def vespers(self, market_data: Dict):
        """VESPERS — 15:30. The evening sacrifice. Forced liquidation."""
        self.state.hour = 'VESPERS'
        print("☩ VESPERS — The evening sacrifice.")
        if self.liturgy:
            for h in list(self.liturgy.thesaurus.consecrated_hosts):
                price = market_data.get(h.symbol, {}).get('price', h.entry_price)
                self.liturgy.thesaurus.consume(h, price)
                self.apokatastasis.force_restoration(h, price)

    def compline(self):
        """COMPLINE — 16:00. Night prayer. The ledger closes."""
        self.state.hour = 'COMPLINE'
        print("☩ COMPLINE — Silence. The ledger closes. Deo gratias.")
        if self.apokatastasis:
            self.apokatastasis.print_ledger()

    # ═══════════════════════════════════════════════════════════
    # THE SERPENT COIL (TERCE)
    # ═══════════════════════════════════════════════════════════

    def _terce_coil(self, market_data: Dict):
        """Counter-predation — detect algo manipulation"""
        for h in self.liturgy.thesaurus.consecrated_hosts:
            tape = market_data.get(h.symbol, {}).get('recent_tape', [])
            if not tape:
                continue
            det = self.serpent.analyze(h.symbol, tape)
            if det.get('toxicity', 0) > 0.3:
                self.state.serpent_detections.append(det)
                if det.get('momentum_ignition', {}).get('detected'):
                    if det['momentum_ignition']['direction'] == 'up':
                        h.stop_price = min(h.stop_price, market_data[h.symbol]['price'] * 1.005)
                        print(f"☩ SERPENS: {h.symbol} momentum ignition UP — stop tightened")

    # ═══════════════════════════════════════════════════════════
    # THE AFTERNOON WATCH (NONE)
    # ═══════════════════════════════════════════════════════════

    def _none_watch(self, market_data: Dict):
        """Monitor bathymetric pressure and archon activity"""
        for h in self.liturgy.thesaurus.consecrated_hosts:
            data = market_data.get(h.symbol, {})
            if not data:
                continue

            pressure = data.get('bathymetric_pressure', 0)
            self.state.bathymetric_pressures[h.symbol] = pressure

            if pressure > 0.8:
                h.stop_price = h.stop_price * 1.002
                print(f"☩ BATHYMETRIC: {h.symbol} pressure={pressure:.2f} — stop widened")

            from ..fas.metanoia import metanoia_check
            met = metanoia_check(h.symbol, h, market_data, self.veil_piercer, self.archon_detector)
            if met.required:
                print(f"☩ METANOIA: {h.symbol} — {met.reason}")
                if met.new_direction == 'flat':
                    price = data.get('price', h.entry_price)
                    self.liturgy.thesaurus.consume(h, price)
                    self.apokatastasis.force_restoration(h, price)


CANONICAL_CHANTS = {
    'MATINS': 'Ad matutinum — The veil is thick. We pierce it.',
    'PRIME': 'Prima hora — The bell tolls. The slaughter begins.',
    'TERCE': 'Tertia hora — The trend reveals. The serpent watches.',
    'SEXT': 'Sexta hora — The sun at zenith. Volume dies. We wait.',
    'NONE': 'Nona hora — The serpents stir. Pressure mounts.',
    'VESPERS': 'Vesperae — The evening sacrifice. All positions consumed.',
    'COMPLINE': 'Completorium — Silence. The ledger closes. Deo gratias.',
}