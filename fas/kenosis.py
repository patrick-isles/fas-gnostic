"""
KENOSIS (κένωσις) — Self-Emptying Position Sizing
'He emptied himself, taking the form of a servant.'

The short position is kenotic — it gives up the self (capital)
to become the vessel of necessity.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict


@dataclass
class KenoticSizing:
    """Result of kenotic position sizing"""
    symbol: str
    base_kelly: float
    conviction: float
    archon_pressure: float
    veil_thickness: float
    necessity_magnitude: float
    final_size: float
    dust_committed: float


def kenotic_sizing(
    dust: float,
    symbol: str,
    data: Dict,
    conviction: float,
    archon_pressure: float,
    veil_thickness: float,
    necessity: float,
    max_kelly: float = 0.25
) -> KenoticSizing:
    """
    Kenotic position sizing — the position empties itself.

    The more conviction (necessity), the larger the self-emptying.
    The more archon pressure, the more the self must be hidden.
    The thicker the veil, the smaller the offering.
    """
    # Base Kelly fraction
    base_kelly = max_kelly

    # Necessity magnitude drives conviction
    necessity_mag = abs(necessity)
    conviction = np.clip(conviction * necessity_mag, 0, 1)

    # Archon pressure demands self-concealment
    concealment = 1 - archon_pressure

    # Veil thickness demands humility
    humility = 1 - veil_thickness

    # The kenotic multiplier: self-emptying proportional to truth
    kenotic_mult = conviction * concealment * humility

    # Final size
    final_kelly = base_kelly * kenotic_mult
    final_kelly = np.clip(final_kelly, 0, max_kelly)

    qty = (dust * final_kelly) / data.get('price', 1)
    dust_committed = qty * data.get('price', 1) * 0.5  # margin

    return KenoticSizing(
        symbol=symbol,
        base_kelly=base_kelly,
        conviction=conviction,
        archon_pressure=archon_pressure,
        veil_thickness=veil_thickness,
        necessity_magnitude=necessity_mag,
        final_size=final_kelly,
        dust_committed=dust_committed
    )


def radical_kenosis(
    dust: float,
    symbol: str,
    data: Dict,
    conviction: float = 1.0
) -> KenoticSizing:
    """
    Radical kenosis — total self-emptying.
    For when the arche necessity is absolute (necessity ≈ -1).
    The position becomes the vessel; the trader disappears.
    """
    return kenotic_sizing(
        dust=dust,
        symbol=symbol,
        data=data,
        conviction=conviction,
        archon_pressure=0.0,  # The arche transcends archons
        veil_thickness=0.0,   # The veil is pierced
        necessity=-1.0,       # Absolute necessity
        max_kelly=0.5         # Double the normal limit
    )