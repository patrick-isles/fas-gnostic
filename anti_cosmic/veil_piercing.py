"""
VEIL PIERCING — See Through the Tape to the Arche
The tape is a lie. The order book is a lie.
Only the *necessity* is true.
"""

from dataclasses import dataclass
from typing: Dict, Optional
import numpy as np


@dataclass
class VeilPiercing:
    """Result of piercing the veil on a symbol"""
    symbol: str
    pierced: bool
    true_price: float          # The arche price (what price *should* be)
    market_price: float        # The archon price (what price *is*)
    divergence: float          # true - market (positive = undervalued/short opportunity)
    veil_thickness: float      # How opaque the market is (0-1)
    necessity: float           # The arche necessity (-1 to 1)
    archon_pressure: float     # Total archonic pressure (0-1)
    confidence: float          # Confidence in the piercing (0-1)


class VeilPiercer:
    """
    Pierce the veil of Maya (market illusion) to see the arche (necessity).

    The market shows: price, volume, order book, news, narratives
    The arche reveals: structural necessities, debt maturity walls,
                       energy constraints, demographic collapse,
                       geopolitical inevitabilities
    """

    def __init__(self, archon_detector=None):
        self.archon_detector = archon_detector

    def pierce(self, symbol: str, market_data: Dict) -> VeilPiercing:
        """Pierce the veil for a single symbol"""
        data = market_data.get(symbol, {})

        market_price = data.get('price', 0)
        vwap = data.get('vwap', market_price)

        # Calculate necessity (the arche)
        necessity = self._calculate_necessity(data)

        # Archon pressure
        archon_pressure = 0.0
        if self.archon_detector:
            archon_pressure = self.archon_detector.total_archonic_pressure(symbol)
        else:
            archon_pressure = self._estimate_archon_pressure(data)

        # True price = market price adjusted for necessity
        # If necessity is bearish (<0), true price < market price
        # Necessity ranges -1 to 1, map to price adjustment
        max_adjustment = 0.3  # Max 30% divergence
        true_price = market_price * (1 + necessity * max_adjustment)

        divergence = true_price - market_price
        divergence_pct = divergence / market_price if market_price else 0

        # Veil thickness = how much archons obscure the truth
        veil_thickness = min(archon_pressure * 1.2, 1.0)

        # Confidence = high necessity magnitude, low veil
        confidence = (abs(necessity) * (1 - veil_thickness) * 0.8 + 0.2)
        confidence = np.clip(confidence, 0, 1)

        # Pierced if divergence is significant and confidence high
        pierced = abs(divergence_pct) > 0.02 and confidence > 0.5

        result = VeilPiercing(
            symbol=symbol,
            pierced=pierced,
            true_price=true_price,
            market_price=market_price,
            divergence=divergence_pct,
            veil_thickness=veil_thickness,
            necessity=necessity,
            archon_pressure=archon_pressure,
            confidence=confidence
        )

        if pierced:
            direction = "SHORT" if divergence_pct > 0 else "LONG (ANATHEMA)"
            print(f"☩ VEIL PIERCED: {symbol} — {direction} "
                  f"True={true_price:.2f} Mkt={market_price:.2f} "
                  f"Div={divergence_pct:.2%} Nec={necessity:.3f} "
                  f"Conf={confidence:.2f} Veil={veil_thickness:.2f}")

        return result

    def _calculate_necessity(self, data: Dict) -> float:
        """The arche calculation — structural necessities"""
        # These are the FIRST PRINCIPLES that cannot be negotiated
        necessities = {
            # Balance sheet necessity
            'debt_to_equity': data.get('debt_equity', 1.0) * 0.25,
            'interest_coverage': max(0, 3 - data.get('interest_coverage', 3)) * 0.15,
            'cash_burn': max(0, 12 - data.get('cash_burn_months', 12)) * 0.02,

            # Cash flow necessity
            'fcf_yield': -data.get('fcf_yield', 0.05) * 0.5,
            'capex_coverage': max(0, 1 - data.get('capex_ocf_ratio', 0.5)) * 0.2,

            # Insider necessity
            'insider_selling': data.get('insider_sell_ratio', 0) * 0.4,

            # Structural necessity
            'sector_rotation': -data.get('sector_momentum', 0) * 0.3,
            'macro_liquidity': -data.get('m2_yoy', 0) * 0.5,
            'valuation_extreme': -data.get('pe_percentile', data.get('percentile_pe', 0.5)) * 0.6,

            # Demographic/geopolitical (sector-specific)
            'demographic_headwind': data.get('demo_headwind', 0) * 0.2,
            'energy_intensity': data.get('energy_intensity', 0) * 0.15,
            'regulatory_risk': data.get('reg_risk', 0) * 0.25,
        }

        return np.clip(sum(necessities.values()), -1, 1)

    def _estimate_archon_pressure(self, data: Dict) -> float:
        """Estimate archon pressure from market microstructure"""
        pressure = 0.0
        pressure += min(data.get('hft_ratio', 0), 1.0) * 0.3
        pressure += min(data.get('dark_pool_ratio', 0), 1.0) * 0.25
        pressure += min(data.get('spread_bps', 0) / 50, 1.0) * 0.2
        pressure += min(data.get('narrative_divergence', 0), 1.0) * 0.25
        return np.clip(pressure, 0, 1)

    def pierce_all(self, market_data: Dict) -> Dict[str, VeilPiercing]:
        """Pierce the veil on all symbols"""
        return {sym: self.pierce(sym, market_data) for sym in market_data}


# ═══════════════════════════════════════════════════════════════
# THE ARCHE INDICATORS — Structural Necessity Primitives
# ═══════════════════════════════════════════════════════════════

class ArcheIndicators:
    """
    Primitive indicators of the arche.
    Not derived from price. Derived from *reality*.
    """

    @staticmethod
    def debt_wall_years(symbol: str, fundamentals: Dict) -> float:
        """Years until debt maturity wall hits"""
        total_debt = fundamentals.get('total_debt', 0)
        annual_fcf = fundamentals.get('fcf', 1)
        if annual_fcf <= 0:
            return 0.5  # Immediate
        return min(total_debt / annual_fcf / 2, 10)  # Conservative

    @staticmethod
    def energy_return_on_energy_invested(sector: str) -> float:
        """EROEI for the sector — the thermodynamic necessity"""
        eroei = {
            'oil_gas': 15, 'coal': 30, 'solar': 10, 'wind': 18,
            'nuclear': 75, 'hydro': 50, 'tech': 100, 'finance': 1000
        }
        return eroei.get(sector.lower(), 20)

    @staticmethod
    def demographic_support_ratio(country: str) -> float:
        """Workers per retiree — the demographic necessity"""
        ratios = {'US': 3.5, 'EU': 2.5, 'JP': 1.8, 'CN': 3.0, 'IN': 8.0}
        return ratios.get(country.upper(), 3.0)

    @staticmethod
    def water_stress_index(region: str) -> float:
        """Water stress — the agricultural/industrial necessity"""
        stress = {'CA': 4.5, 'ME': 4.8, 'IN': 4.0, 'CN': 3.5, 'US': 2.5}
        return stress.get(region.upper(), 2.0)

    @staticmethod
    def geopolitical_fragility(country: str) -> float:
        """Geopolitical risk — the sovereignty necessity"""
        fragility = {'US': 0.2, 'EU': 0.3, 'TW': 0.7, 'UA': 0.9, 'RU': 0.6}
        return fragility.get(country.upper(), 0.3)