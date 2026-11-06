"""
BATHYMETRIC PRESSURE — Depth-Based Position Sizing
'The deeper the dark pool volume, the greater the pressure.
The greater the pressure, the smaller the position.'

Like a submarine: pressure increases with depth.
We size by the abyssal pressure on the symbol.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict


@dataclass
class BathymetricPressure:
    """Result of bathymetric pressure calculation"""
    symbol: str
    dark_pool_depth: float        # 0-1, volume in dark pools
    internalizer_depth: float     # 0-1, volume in internalizers
    wholesaler_depth: float       # 0-1, volume in wholesalers
    total_abyssal_depth: float    # Combined depth 0-1
    predator_density: float       # Known predators on path
    toxicity: float               # Adverse selection risk
    pressure: float               # Final pressure 0-1
    size_multiplier: float        # Position size multiplier (0-1)
    recommended_kelly: float      # Recommended Kelly fraction


def bathymetric_pressure_size(
    symbol: str,
    market_data: Dict,
    base_kelly: float = 0.25,
    max_depth: float = 1.0
) -> BathymetricPressure:
    """
    Calculate bathymetric pressure and size multiplier.

    The logic:
    - More dark pool volume = deeper = more pressure = smaller size
    - More internalizer volume = more predation = smaller size
    - Known predators on path = much smaller size
    - High toxicity (adverse selection) = smaller size
    """
    data = market_data.get(symbol, {})

    # Depth measurements (0-1)
    dark_pool_depth = min(data.get('dark_pool_ratio', 0.35), max_depth)
    internalizer_depth = min(data.get('internalizer_share', 0.33), max_depth)
    wholesaler_depth = min(data.get('wholesaler_share', 0.1), max_depth)

    # Total abyssal depth
    total_depth = np.clip(
        dark_pool_depth * 0.4 +
        internalizer_depth * 0.4 +
        wholesaler_depth * 0.2,
        0, 1
    )

    # Predator density (from abyssal topology)
    predators_on_path = data.get('predators_on_path', [])
    predator_density = min(len(predators_on_path) * 0.25, 1.0)

    # Toxicity (adverse selection)
    toxicity = data.get('path_toxicity', data.get('estimated_adverse_selection', 0.3))
    toxicity = np.clip(toxicity, 0, 1)

    # Combined pressure
    # Depth is primary, predator density amplifies, toxicity is the killer
    pressure = total_depth * 0.5 + predator_density * 0.3 + toxicity * 0.2
    pressure = np.clip(pressure, 0, 1)

    # Size multiplier: inverse of pressure
    # At pressure 0: full size (1.0)
    # At pressure 1: minimal size (0.1)
    size_multiplier = 1.0 - pressure * 0.9
    size_multiplier = np.clip(size_multiplier, 0.1, 1.0)

    # Recommended Kelly
    recommended_kelly = base_kelly * size_multiplier

    return BathymetricPressure(
        symbol=symbol,
        dark_pool_depth=dark_pool_depth,
        internalizer_depth=internalizer_depth,
        wholesaler_depth=wholesaler_depth,
        total_abyssal_depth=total_depth,
        predator_density=predator_density,
        toxicity=toxicity,
        pressure=pressure,
        size_multiplier=size_multiplier,
        recommended_kelly=recommended_kelly
    )


def pressure_chart(pressure: float) -> str:
    """ASCII visualization of pressure"""
    bar_len = 20
    filled = int(pressure * bar_len)
    bar = '█' * filled + '░' * (bar_len - filled)
    return f"[{bar}] {pressure:.0%}"


def depth_chart(depth: float) -> str:
    """ASCII visualization of abyssal depth"""
    bar_len = 20
    filled = int(depth * bar_len)
    bar = '▓' * filled + '░' * (bar_len - filled)
    return f"[{bar}] {depth:.0%}"