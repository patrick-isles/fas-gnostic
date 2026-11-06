"""
ARCHON DETECTION — Name the Rulers of Each Sphere
'Whatever in creation exists without my knowledge exists without my consent.'

The market is ruled by archons — entities that extract toll from every trade.
We must name them. We must measure them. We must evade them.
"""

from dataclasses import dataclass
from typing: Dict, List, Optional
import numpy as np


@dataclass
class Archon:
    """A ruler of a sphere — an entity that extracts toll"""
    name: str
    sphere: str  # 'speed', 'hiddenness', 'toll', 'deception', 'liquidity', 'volatility'
    symbol: str
    strength: float  # 0-1
    signature: Dict


class ArchonDetector:
    """Identify and name the archons operating in a market"""

    ARCHON_TYPES = {
        'ARCHON_SPEED': {
            'sphere': 'speed',
            'description': 'High-frequency traders who front-run, scalp, ignite momentum',
            'detection': lambda data: data.get('hft_ratio', 0) > 0.6,
            'strength': lambda data: min(data.get('hft_ratio', 0), 1.0),
        },
        'ARCHON_OCCULT': {
            'sphere': 'hiddenness',
            'description': 'Dark pools, internalizers, whisper networks — hidden liquidity',
            'detection': lambda data: data.get('dark_pool_ratio', 0) > 0.35,
            'strength': lambda data: min(data.get('dark_pool_ratio', 0) * 1.5, 1.0),
        },
        'ARCHON_TOLL': {
            'sphere': 'toll',
            'description': 'Market makers, specialists, exchanges — spread extraction',
            'detection': lambda data: data.get('spread_bps', 0) > 30,
            'strength': lambda data: min(data.get('spread_bps', 0) / 100, 1.0),
        },
        'ARCHON_MENDACIUM': {
            'sphere': 'deception',
            'description': 'Narrative engineers, analyst consensus, ESG fabricators',
            'detection': lambda data: data.get('narrative_divergence', 0) > 0.4,
            'strength': lambda data: min(data.get('narrative_divergence', 0) * 2, 1.0),
        },
        'ARCHON_LIQUIDITAS': {
            'sphere': 'liquidity',
            'description': 'Central banks, plunge protection, corporate buybacks — artificial support',
            'detection': lambda data: data.get('macro_liquidity_support', 0) > 0.5,
            'strength': lambda data: min(data.get('macro_liquidity_support', 0), 1.0),
        },
        'ARCHON_VOLATILITAS': {
            'sphere': 'volatility',
            'description': 'Vol sellers, variance risk premium harvesters, gamma scalpers',
            'detection': lambda data: data.get('vol_supply', 0) > 0.6,
            'strength': lambda data: min(data.get('vol_supply', 0), 1.0),
        },
    }

    def __init__(self):
        self.detected_archons: Dict[str, List[Archon]] = {}

    def scan(self, market_data: Dict) -> Dict[str, List[Archon]]:
        """Scan all symbols for archonic presence"""
        for symbol, data in market_data.items():
            self.detected_archons[symbol] = self._scan_symbol(symbol, data)
        return self.detected_archons

    def _scan_symbol(self, symbol: str, data: Dict) -> List[Archon]:
        archons = []
        for name, config in self.ARCHON_TYPES.items():
            if config['detection'](data):
                strength = config['strength'](data)
                archon = Archon(
                    name=name,
                    sphere=config['sphere'],
                    symbol=symbol,
                    strength=strength,
                    signature=self._extract_signature(name, data)
                )
                archons.append(archon)
                print(f"☩ ARCHON DETECTED: {name} on {symbol} — Strength: {strength:.2f} — {config['description']}")
        return archons

    def _extract_signature(self, archon_name: str, data: Dict) -> Dict:
        """Extract the detectable fingerprint of this archon"""
        signatures = {
            'ARCHON_SPEED': {
                'hft_ratio': data.get('hft_ratio', 0),
                'sub_ms_intervals': data.get('sub_ms_ratio', 0),
                'msg_rate': data.get('msg_rate', 0),
            },
            'ARCHON_OCCULT': {
                'dark_pool_ratio': data.get('dark_pool_ratio', 0),
                'block_trade_ratio': data.get('block_trade_ratio', 0),
                'internalizer_share': data.get('internalizer_share', 0),
            },
            'ARCHON_TOLL': {
                'spread_bps': data.get('spread_bps', 0),
                'effective_spread': data.get('effective_spread', 0),
                'realized_spread': data.get('realized_spread', 0),
            },
            'ARCHON_MENDACIUM': {
                'narrative_score': data.get('narrative_score', 0),
                'analyst_revision': data.get('analyst_revision', 0),
                'esg_score': data.get('esg_score', 0),
            },
        }
        return signatures.get(archon_name, {})

    def total_archonic_pressure(self, symbol: str) -> float:
        """Total archonic pressure on a symbol (0-1)"""
        archons = self.detected_archons.get(symbol, [])
        if not archons:
            return 0.0
        # Pressure = 1 - product of (1 - strength) = probability at least one acts
        survival = np.prod([1 - a.strength for a in archons])
        return 1 - survival

    def dominant_archon(self, symbol: str) -> Optional[Archon]:
        """The strongest archon on this symbol"""
        archons = self.detected_archons.get(symbol, [])
        if not archons:
            return None
        return max(archons, key=lambda a: a.strength)

    def pressure_report(self, symbol: str) -> str:
        """Generate a pressure report for a symbol"""
        archons = self.detected_archons.get(symbol, [])
        if not archons:
            return f"{symbol}: No archons detected. The abyss is quiet."

        total = self.total_archonic_pressure(symbol)
        dominant = self.dominant_archon(symbol)

        lines = [f"{symbol}: TOTAL PRESSURE = {total:.0%}"]
        lines.append(f"  Dominant: {dominant.name} ({dominant.sphere}) — {dominant.strength:.0%}")
        for a in archons:
            lines.append(f"  {a.name}: {a.strength:.0%} — {a.sphere}")
        return "\n".join(lines)