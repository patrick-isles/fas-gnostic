"""
VOLUME INCENSE — The Smoke of the Tape
Volume rises like incensor smoke. It reveals the true intent.
Thin smoke = no conviction. Thick smoke = archon presence.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from collections import deque
import numpy as np


@dataclass
class VolumeIncense:
    """A reading of volume incense"""
    symbol: str
    timestamp: datetime
    volume: float
    vwap: float
    price: float
    volume_profile: Dict  # price -> volume
    smoke_density: float  # 0-1
    smoke_color: str      # 'white', 'gray', 'black'
    prayer: str


class Censer:
    """
    The Censer — swings the incense through the tape.
    Reads volume as smoke signals from the abyss.
    """

    def __init__(self, lookback_periods: int = 390):  # 390 = 1-min bars in RTH
        self.lookback = lookback_periods
        self.incense_history: Dict[str, deque] = {}

    def _get_history(self, symbol: str) -> deque:
        if symbol not in self.incense_history:
            self.incense_history[symbol] = deque(maxlen=self.lookback)
        return self.incense_history[symbol]

    def swing(self, symbol: str, bar: Dict) -> VolumeIncense:
        """Swing the censer — process a volume bar"""
        history = self._get_history(symbol)

        volume = bar.get('volume', 0)
        vwap = bar.get('vwap', bar.get('close', 0))
        price = bar.get('close', 0)
        high = bar.get('high', price)
        low = bar.get('low', price)

        # Build volume profile (simplified: 10 price levels)
        profile = {}
        if high > low:
            for i in range(10):
                level = low + (high - low) * i / 10
                # Approximate volume at level (uniform for now)
                profile[round(level, 2)] = volume / 10

        history.append({
            'volume': volume,
            'vwap': vwap,
            'price': price,
            'profile': profile,
            'timestamp': bar.get('timestamp', datetime.now()),
        })

        # Analyze the smoke
        incense = self._read_smoke(symbol, volume, vwap, price, profile)
        return incense

    def _read_smoke(self, symbol: str, volume: float, vwap: float,
                    price: float, profile: Dict) -> VolumeIncense:
        """Read the smoke signals"""
        history = list(self._get_history(symbol))

        if len(history) < 20:
            return VolumeIncense(symbol, datetime.now(), volume, vwap, price,
                                profile, 0, 'white', 'Insufficient smoke')

        # Average volume
        avg_vol = np.mean([h['volume'] for h in history[-20:]])

        # Smoke density = current volume / average
        density = min(volume / avg_vol if avg_vol > 0 else 1, 3.0) / 3.0

        # VWAP vs price = smoke color
        vwap_dev = (price - vwap) / vwap if vwap else 0

        if vwap_dev > 0.005:
            color = 'black'   # Price above VWAP = selling pressure (for shorts, good)
            prayer = 'The smoke is black. The sellers dominate. Deo gratias.'
        elif vwap_dev < -0.005:
            color = 'white'   # Price below VWAP = buying pressure (bad for shorts)
            prayer = 'The smoke is white. The buyers swarm. Miserere.'
        else:
            color = 'gray'    # At VWAP = equilibrium
            prayer = 'The smoke is gray. The battle is joined. Kyrie eleison.'

        # High density + black smoke = strong conviction
        if density > 0.7 and color == 'black':
            prayer = '☩ THICK BLACK SMOKE — The arche manifests. CONVICTION HIGH.'

        # High density + white smoke = trap
        if density > 0.7 and color == 'white':
            prayer = '☩ THICK WHITE SMOKE — The archons feign strength. TRAP LIKELY.'

        # Low density = no conviction
        if density < 0.3:
            prayer = 'Thin smoke. No conviction. We wait.'

        return VolumeIncense(
            symbol=symbol,
            timestamp=datetime.now(),
            volume=volume,
            vwap=vwap,
            price=price,
            volume_profile=profile,
            smoke_density=density,
            smoke_color=color,
            prayer=prayer
        )

    def read_all(self, market_data: Dict) -> Dict[str, VolumeIncense]:
        """Swing the censer over all symbols"""
        results = {}
        for symbol, data in market_data.items():
            bar = {
                'volume': data.get('volume', 0),
                'vwap': data.get('vwap', data.get('price', 0)),
                'close': data.get('price', 0),
                'high': data.get('high', data.get('price', 0) * 1.001),
                'low': data.get('low', data.get('price', 0) * 0.999),
                'timestamp': datetime.now(),
            }
            results[symbol] = self.swing(symbol, bar)
        return results

    def get_smoke_signal(self, symbol: str) -> Dict:
        """Get aggregated smoke signal"""
        incense_list = list(self._get_history(symbol))
        if len(incense_list) < 10:
            return {'signal': 'UNCLEAR', 'strength': 0}

        recent = incense_list[-10:]
        densities = [1.0] * len(recent)  # Simplified
        colors = ['gray'] * len(recent)

        # In production, would store actual incense readings
        # For now, return based on volume trend
        vols = [h['volume'] for h in recent]
        vol_trend = np.polyfit(range(len(vols)), vols, 1)[0]

        if vol_trend > 0:
            return {'signal': 'BUILDING', 'strength': min(vol_trend / np.mean(vols), 1)}
        else:
            return {'signal': 'FADING', 'strength': min(-vol_trend / np.mean(vols), 1)}