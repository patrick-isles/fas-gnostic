"""
SERPENT COIL — Algo Detection & Counter-Predation
'The serpent coils in the tape. It strikes at momentum. It feasts on stops.'

Detect the algorithmic predators:
- Momentum Ignition: Light volume, rapid price move, no fundamental catalyst
- Stop Hunt: Price spikes to obvious levels, immediate reversal
- Layering/Spoofing: Large orders appear/disappear, no execution
- Wash Trading: Self-trades to paint tape
- Quote Stuffing: Burst of orders to slow competitors
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from collections import deque
from datetime import datetime, timedelta
import numpy as np


@dataclass
class SerpentDetection:
    """A detected serpent in the tape"""
    type: str  # 'momentum_ignition', 'stop_hunt', 'layering', 'wash_trade', 'quote_stuffing'
    symbol: str
    detected: bool
    direction: str  # 'up', 'down', 'both'
    magnitude: float
    confidence: float
    toxicity: float  # 0-1, how dangerous to our position
    details: Dict = field(default_factory=dict)


class SerpentCoil:
    """
    The Serpent Coil — detects and counters algorithmic predation.
    Watches the tape. Names the serpent. Breaks its fangs.
    """

    def __init__(self, lookback_ticks: int = 1000):
        self.lookback_ticks = lookback_ticks
        self.tapes: Dict[str, deque] = {}
        self.detections_history: Dict[str, List[SerpentDetection]] = {}

    def _get_tape(self, symbol: str) -> deque:
        if symbol not in self.tapes:
            self.tapes[symbol] = deque(maxlen=self.lookback_ticks)
        return self.tapes[symbol]

    def add_tick(self, symbol: str, tick: Dict):
        """Add a tick to the tape"""
        tape = self._get_tape(symbol)
        tick['received_at'] = datetime.now()
        tape.append(tick)

    def analyze(self, symbol: str, tape: Optional[List[Dict]] = None) -> Dict:
        """
        Analyze tape for serpent signatures.
        Returns dict of detections.
        """
        if tape is None:
            tape = list(self._get_tape(symbol))

        if len(tape) < 30:
            return {'toxicity': 0, 'detections': []}

        detections = []

        # 1. MOMENTUM IGNITION
        det = self._detect_momentum_ignition(symbol, tape)
        if det.detected:
            detections.append(det)

        # 2. STOP HUNT
        det = self._detect_stop_hunt(symbol, tape)
        if det.detected:
            detections.append(det)

        # 3. LAYERING / SPOOFING
        det = self._detect_layering(symbol, tape)
        if det.detected:
            detections.append(det)

        # 4. WASH TRADING
        det = self._detect_wash_trading(symbol, tape)
        if det.detected:
            detections.append(det)

        # 5. QUOTE STUFFING
        det = self._detect_quote_stuffing(symbol, tape)
        if det.detected:
            detections.append(det)

        # Overall toxicity
        toxicity = max((d.toxicity for d in detections), default=0)

        result = {
            'symbol': symbol,
            'toxicity': toxicity,
            'detections': [self._det_to_dict(d) for d in detections],
            'timestamp': datetime.now().isoformat(),
        }

        if symbol not in self.detections_history:
            self.detections_history[symbol] = []
        self.detections_history[symbol].extend(detections)

        return result

    def _det_to_dict(self, det: SerpentDetection) -> Dict:
        return {
            'type': det.type,
            'detected': det.detected,
            'direction': det.direction,
            'magnitude': det.magnitude,
            'confidence': det.confidence,
            'toxicity': det.toxicity,
            'details': det.details,
        }

    # ═══════════════════════════════════════════════════════════
    # DETECTION ALGORITHMS
    # ═══════════════════════════════════════════════════════════

    def _detect_momentum_ignition(self, symbol: str, tape: List[Dict]) -> SerpentDetection:
        """
        Momentum Ignition: Small size, rapid move, no news.
        Characteristic: price moves >0.5% in <60s on <10k shares.
        """
        recent = tape[-30:]
        prices = [t['price'] for t in recent]
        volumes = [t.get('size', 0) for t in recent]
        times = [t.get('time', datetime.now()) for t in recent]

        if len(prices) < 10:
            return SerpentDetection('momentum_ignition', symbol, False, 'none', 0, 0, 0)

        pct_change = (prices[-1] - prices[0]) / prices[0]
        total_volume = sum(volumes)
        time_span = (times[-1] - times[0]).total_seconds()

        # Criteria: significant move, low volume, short time
        move_significant = abs(pct_change) > 0.005
        volume_low = total_volume < 10000
        time_short = time_span < 60
        no_news = True  # Would check news feed in production

        detected = move_significant and volume_low and time_short and no_news
        direction = 'up' if pct_change > 0 else 'down'
        magnitude = abs(pct_change)
        confidence = 0.7 if detected else 0.0
        toxicity = magnitude * 10 if detected else 0  # Scales with move size

        return SerpentDetection(
            type='momentum_ignition',
            symbol=symbol,
            detected=detected,
            direction=direction,
            magnitude=magnitude,
            confidence=confidence,
            toxicity=min(toxicity, 1.0),
            details={
                'pct_change': pct_change,
                'total_volume': total_volume,
                'time_span_sec': time_span,
                'ticks': len(recent),
            }
        )

    def _detect_stop_hunt(self, symbol: str, tape: List[Dict]) -> SerpentDetection:
        """
        Stop Hunt: Spike to round number/previous high/low, immediate reversal.
        """
        recent = tape[-50:]
        prices = [t['price'] for t in recent]
        highs = [t.get('high', t['price']) for t in recent]
        lows = [t.get('low', t['price']) for t in recent]

        if len(prices) < 20:
            return SerpentDetection('stop_hunt', symbol, False, 'none', 0, 0, 0)

        # Look for spike and reversal within 5-10 ticks
        for i in range(5, len(prices) - 5):
            spike_up = prices[i] > max(prices[i-5:i]) * 1.003
            spike_down = prices[i] < min(prices[i-5:i]) * 0.997

            if spike_up:
                # Check reversal
                if prices[-1] < prices[i] * 0.998:
                    magnitude = (prices[i] - prices[i-1]) / prices[i-1]
                    return SerpentDetection(
                        type='stop_hunt',
                        symbol=symbol,
                        detected=True,
                        direction='up',
                        magnitude=magnitude,
                        confidence=0.75,
                        toxicity=0.8,
                        details={'spike_idx': i, 'spike_price': prices[i],
                                'reversal_pct': (prices[i] - prices[-1]) / prices[i]}
                    )

            if spike_down:
                if prices[-1] > prices[i] * 1.002:
                    magnitude = (prices[i-1] - prices[i]) / prices[i-1]
                    return SerpentDetection(
                        type='stop_hunt',
                        symbol=symbol,
                        detected=True,
                        direction='down',
                        magnitude=magnitude,
                        confidence=0.75,
                        toxicity=0.8,
                        details={'spike_idx': i, 'spike_price': prices[i],
                                'reversal_pct': (prices[-1] - prices[i]) / prices[i]}
                    )

        return SerpentDetection('stop_hunt', symbol, False, 'none', 0, 0, 0)

    def _detect_layering(self, symbol: str, tape: List[Dict]) -> SerpentDetection:
        """
        Layering: Large orders on one side, canceled before execution.
        Detect via order book snapshot analysis (simplified here).
        """
        recent = tape[-20:]
        # In production, would analyze L2 data
        # Here: look for price stability with high quote/update ratio
        prices = [t['price'] for t in recent]
        price_std = np.std(prices) / np.mean(prices) if prices else 0

        # Simulated: high message rate with low volatility = layering
        msg_rate = len(recent)
        layering_suspected = price_std < 0.001 and msg_rate > 15

        return SerpentDetection(
            type='layering',
            symbol=symbol,
            detected=layering_suspected,
            direction='both',
            magnitude=0,
            confidence=0.5 if layering_suspected else 0,
            toxicity=0.6 if layering_suspected else 0,
            details={'price_cv': price_std, 'msg_rate': msg_rate}
        )

    def _detect_wash_trading(self, symbol: str, tape: List[Dict]) -> SerpentDetection:
        """
        Wash Trading: Same size, same price, rapid back-and-forth.
        """
        recent = tape[-30:]
        # Look for repeated identical prints
        price_size_pairs = [(t['price'], t.get('size', 0)) for t in recent]
        from collections import Counter
        counts = Counter(price_size_pairs)
        max_repeat = max(counts.values()) if counts else 0

        detected = max_repeat >= 3
        return SerpentDetection(
            type='wash_trade',
            symbol=symbol,
            detected=detected,
            direction='none',
            magnitude=0,
            confidence=0.6 if detected else 0,
            toxicity=0.5 if detected else 0,
            details={'max_repeat': max_repeat, 'unique_prints': len(counts)}
        )

    def _detect_quote_stuffing(self, symbol: str, tape: List[Dict]) -> SerpentDetection:
        """
        Quote Stuffing: Burst of orders to create latency.
        """
        recent = tape[-100:]
        if len(recent) < 50:
            return SerpentDetection('quote_stuffing', symbol, False, 'none', 0, 0, 0)

        # Check for burst in message rate
        times = [t.get('time', datetime.now()) for t in recent]
        intervals = [(times[i] - times[i-1]).total_seconds() * 1e6 for i in range(1, len(times))]
        if not intervals:
            return SerpentDetection('quote_stuffing', symbol, False, 'none', 0, 0, 0)

        median_interval = np.median(intervals)
        min_interval = min(intervals)
        burst = min_interval < median_interval * 0.01 and median_interval > 100  # microseconds

        return SerpentDetection(
            type='quote_stuffing',
            symbol=symbol,
            detected=burst,
            direction='none',
            magnitude=0,
            confidence=0.6 if burst else 0,
            toxicity=0.7 if burst else 0,
            details={'median_interval_us': median_interval, 'min_interval_us': min_interval}
        )

    def get_toxicity_score(self, symbol: str) -> float:
        """Overall toxicity score for a symbol"""
        recent_dets = self.detections_history.get(symbol, [])[-10:]
        if not recent_dets:
            return 0.0
        return max(d.toxicity for d in recent_dets)