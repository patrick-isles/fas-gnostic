"""
METANOIA (μετάνοια) — Repentance, Reversal, Change of Mind
The position must be capable of metanoia — turning from error.

When the arche reveals itself was false, the position must reverse.
This is not stop-loss. This is confession.
"""

from dataclasses import dataclass
from typing import Dict, Optional
import numpy as np


@dataclass
class MetanoiaResult:
    """Result of metanoia check"""
    symbol: str
    required: bool
    reason: str
    new_direction: Optional[str]  # 'short', 'flat', 'long' (anathema)
    urgency: float  # 0-1


def metanoia_check(
    symbol: str,
    position,
    market_data: Dict,
    veil_piercer,
    archon_detector
) -> MetanoiaResult:
    """
    Check if the position requires metanoia (reversal).

    Metanoia is required when:
    1. The veil re-forms (archon pressure spikes)
    2. The necessity reverses (arche was misread)
    3. The narrative consumes the truth (mendacium triumphs)
    4. The stop is hit (the furnace demands it)
    """
    data = market_data.get(symbol, {})
    current_price = data.get('price', 0)
    entry_price = position.entry_price

    # 1. Veil re-formation check
    vp = veil_piercer.pierce(symbol, market_data)
    veil_reformed = vp.veil_thickness > 0.7 and vp.confidence < 0.3

    # 2. Necessity reversal check
    necessity_reversed = (
        position.arche_necessity < -0.3 and vp.necessity > 0.1  # Was bearish, now bullish
    )

    # 3. Archon mendacium triumph
    archons = archon_detector.detected_archons.get(symbol, [])
    mendacium = any(a.name == 'ARCHON_MENDACIUM' and a.strength > 0.7 for a in archons)

    # 4. Stop hit
    stop_hit = current_price >= position.stop_price

    # 5. Time-based (compline approaches)
    from datetime import datetime
    hour = datetime.now().hour
    minute = datetime.now().minute
    compline_near = hour >= 15 and minute >= 45

    reasons = []
    if veil_reformed:
        reasons.append("VEIL REFORMED")
    if necessity_reversed:
        reasons.append("NECESSITY REVERSED")
    if mendacium:
        reasons.append("MENDACIUM TRIUMPHS")
    if stop_hit:
        reasons.append("STOP HIT")
    if compline_near:
        reasons.append("COMPLINE APPROACHES")

    required = len(reasons) > 0

    if required:
        if stop_hit or compline_near:
            new_dir = 'flat'
            urgency = 1.0
        elif necessity_reversed:
            new_dir = 'flat'  # Never go long — anathema
            urgency = 0.8
        else:
            new_dir = 'flat'
            urgency = 0.6

        return MetanoiaResult(
            symbol=symbol,
            required=True,
            reason='; '.join(reasons),
            new_direction=new_dir,
            urgency=urgency
        )

    return MetanoiaResult(
        symbol=symbol,
        required=False,
        reason="HOLD THE LINE",
        new_direction='short',
        urgency=0.0
    )


def calculate_necessity(data: Dict) -> float:
    """
    Calculate the arche necessity for a symbol.
    This is the primitive — not derived from price.
    """
    necessities = {
        'debt_to_equity': data.get('debt_equity', 1.0) * 0.25,
        'interest_coverage': max(0, 3 - data.get('interest_coverage', 3)) * 0.15,
        'cash_burn': max(0, 12 - data.get('cash_burn_months', 12)) * 0.02,
        'fcf_yield': -data.get('fcf_yield', 0.05) * 0.5,
        'capex_coverage': max(0, 1 - data.get('capex_ocf_ratio', 0.5)) * 0.2,
        'insider_selling': data.get('insider_sell_ratio', 0) * 0.4,
        'sector_rotation': -data.get('sector_momentum', 0) * 0.3,
        'macro_liquidity': -data.get('m2_yoy', 0) * 0.5,
        'valuation_extreme': -data.get('pe_percentile', data.get('percentile_pe', 0.5)) * 0.6,
        'demographic_headwind': data.get('demo_headwind', 0) * 0.2,
        'energy_intensity': data.get('energy_intensity', 0) * 0.15,
        'regulatory_risk': data.get('reg_risk', 0) * 0.25,
    }

    return np.clip(sum(necessities.values()), -1, 1)