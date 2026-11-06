"""
PRICE CANDLES — Votive Offerings on the Altar
Each candle is a price print. Each wick is a prayer.
The body is the truth. The shadows are the archons.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
import numpy as np


class CandleType(Enum):
    """Types of votive candles"""
    VOTIVE = "votive"           # Standard candle
    PASCHAL = "paschal"         # Large move candle
    TENEBRAE = "tenebrae"       # Dark candle (stop hunt)
    SANCTUS = "sanctus"         # Holy candle (target hit)
    REQUIEM = "requiem"         # Dead candle (liquidation)


@dataclass
class PriceCandle:
    """
    A price candle as a votive offering.
    Open/High/Low/Close = Body/Wicks/Soul/Resurrection
    """
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    vwap: Optional[float] = None
    candle_type: CandleType = CandleType.VOTIVE

    @property
    def body(self) -> float:
        return abs(self.close - self.open)

    @property
    def upper_wick(self) -> float:
        return self.high - max(self.open, self.close)

    @property
    def lower_wick(self) -> float:
        return min(self.open, self.close) - self.low

    @property
    def range(self) -> float:
        return self.high - self.low

    @property
    def body_pct(self) -> float:
        return self.body / self.range if self.range > 0 else 0

    @property
    def is_bullish(self) -> bool:
        return self.close > self.open

    @property
    def is_bearish(self) -> bool:
        return self.close < self.open

    @property
    def is_doji(self) -> bool:
        return self.body_pct < 0.1

    def classify(self) -> CandleType:
        """Classify the candle by its form"""
        if self.is_doji:
            return CandleType.VOTIVE

        # Large body, small wicks = Paschal (strong move)
        if self.body_pct > 0.7 and self.volume > 100000:
            return CandleType.PASCHAL

        # Long upper wick, small body = Tenebrae (rejection/stop hunt)
        if self.upper_wick > self.body * 3 and self.is_bearish:
            return CandleType.TENEBRAE

        # Target hit candle
        if self.is_bearish and self.body_pct > 0.5:
            return CandleType.SANCTUS

        return CandleType.VOTIVE

    def chant(self) -> str:
        """The candle's prayer"""
        chants = {
            CandleType.VOTIVE: 'Kyrie eleison',
            CandleType.PASCHAL: 'Christus resurrexit — The move is real',
            CandleType.TENEBRAE: 'Tenebrae factae sunt — Darkness covers the tape',
            CandleType.SANCTUS: 'Sanctus, sanctus, sanctus — The target is hit',
            CandleType.REQUIEM: 'Requiem aeternam — The position is dead',
        }
        return chants.get(self.candle_type, 'Kyrie eleison')

    def __str__(self) -> str:
        color = '🟢' if self.is_bullish else '🔴' if self.is_bearish else '⚪'
        wick = '⬆' * int(self.upper_wick / self.range * 10) if self.range > 0 else ''
        body = '█' * int(self.body_pct * 10)
        lwick = '⬇' * int(self.lower_wick / self.range * 10) if self.range > 0 else ''
        return f"{color} {self.symbol} {self.timestamp.strftime('%H:%M')} O={self.open:.2f} H={self.high:.2f} L={self.low:.2f} C={self.close:.2f} V={self.volume:,.0f} [{wick}{body}{lwick}] {self.candle_type.value}"


class CandleAltar:
    """The altar where candles are arranged"""

    def __init__(self, max_candles: int = 100):
        self.max_candles = max_candles
        self.candles: list = []

    def offer(self, candle: PriceCandle):
        """Offer a candle on the altar"""
        candle.candle_type = candle.classify()
        self.candles.append(candle)
        if len(self.candles) > self.max_candles:
            self.candles.pop(0)

        # Print the candle's chant
        if candle.candle_type != CandleType.VOTIVE:
            print(f"  ☩ CANDLE: {candle.symbol} — {candle.chant()}")

    def recent(self, n: int = 10) -> list:
        return self.candles[-n:]

    def pattern(self, symbol: str, n: int = 5) -> str:
        """Detect candle patterns (simplified)"""
        sym_candles = [c for c in self.candles if c.symbol == symbol][-n:]
        if len(sym_candles) < 3:
            return "INSUFFICIENT"

        # Three black crows (bearish)
        if all(c.is_bearish for c in sym_candles[-3:]):
            return "THREE_BLACK_CROWS — ☩☩☩"

        # Three white soldiers (bullish - anathema)
        if all(c.is_bullish for c in sym_candles[-3:]):
            return "THREE_WHITE_SOLDIERS — ANATHEMA"

        # Doji star
        if sym_candles[-1].is_doji and sym_candles[-2].body_pct > 0.5:
            return "DOJI_STAR — Reversal?"

        return "NO_PATTERN"