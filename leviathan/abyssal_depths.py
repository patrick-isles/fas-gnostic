"""
THE DEEP — Dark Pool Topology
'Beneath the lit exchange lies the abyss. There, the true price hides.'

The market has depths. The lit order book is the surface.
Dark pools, internalizers, wholesalers — these are the abyssal zones.
Each node is a predator. Each route is a migration path.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from collections import defaultdict
import numpy as np


@dataclass
class AbyssalNode:
    """A node in the dark pool topology"""
    name: str
    type: str  # 'dark_pool', 'internalizer', 'wholesaler', 'exchange', 'bank'
    volume_share: float  # 0-1
    toxicity: float  # 0-1 (adverse selection)
    latency_ms: float
    connections: List[str] = field(default_factory=list)
    predatory: bool = False  # Known to front-run, sell flow, etc.


class TheDeep:
    """
    The Deep — topology of hidden liquidity.
    Maps the subterranean rivers where true price flows.
    """

    # Known abyssal nodes (simplified)
    NODES = {
        'CITADEL': AbyssalNode('CITADEL', 'internalizer', 0.18, 0.7, 0.5,
                               ['VIRTU', 'G1X', 'NYSE', 'NASDAQ'], predatory=True),
        'VIRTU': AbyssalNode('VIRTU', 'internalizer', 0.15, 0.65, 0.4,
                             ['CITADEL', 'G1X', 'NYSE', 'NASDAQ'], predatory=True),
        'G1X': AbyssalNode('G1X', 'wholesaler', 0.08, 0.6, 0.8,
                           ['CITADEL', 'VIRTU', 'NASDAQ'], predatory=True),
        'X_TX': AbyssalNode('X_TX', 'dark_pool', 0.06, 0.4, 2.0,
                            ['NYSE', 'NASDAQ', 'BATS'], predatory=False),
        'LIQUIDNET': AbyssalNode('LIQUIDNET', 'dark_pool', 0.04, 0.3, 3.0,
                                 ['NYSE', 'NASDAQ'], predatory=False),
        'LEVEL': AbyssalNode('LEVEL', 'dark_pool', 0.03, 0.35, 2.5,
                             ['NYSE', 'NASDAQ'], predatory=False),
        'MS_POOL': AbyssalNode('MS_POOL', 'dark_pool', 0.05, 0.5, 1.5,
                               ['NYSE', 'NASDAQ'], predatory=True),
        'GS_SIGMA': AbyssalNode('GS_SIGMA', 'dark_pool', 0.04, 0.55, 1.5,
                                ['NYSE', 'NASDAQ'], predatory=True),
        'JPM_JPMX': AbyssalNode('JPM_JPMX', 'dark_pool', 0.03, 0.45, 1.8,
                                ['NYSE', 'NASDAQ'], predatory=True),
        'UBS_PIN': AbyssalNode('UBS_PIN', 'dark_pool', 0.03, 0.4, 2.0,
                               ['NYSE', 'NASDAQ'], predatory=False),
        'NYSE': AbyssalNode('NYSE', 'exchange', 0.12, 0.1, 0.1,
                            ['NASDAQ', 'BATS', 'IEX'], predatory=False),
        'NASDAQ': AbyssalNode('NASDAQ', 'exchange', 0.14, 0.1, 0.1,
                              ['NYSE', 'BATS', 'IEX'], predatory=False),
        'BATS': AbyssalNode('BATS', 'exchange', 0.08, 0.15, 0.2,
                            ['NYSE', 'NASDAQ', 'IEX'], predatory=False),
        'IEX': AbyssalNode('IEX', 'exchange', 0.02, 0.05, 350.0,  # 350μs speed bump
                           ['NYSE', 'NASDAQ', 'BATS'], predatory=False),
    }

    def __init__(self):
        self.nodes = dict(self.NODES)
        self.flows = defaultdict(float)  # (from, to) -> volume
        self.symbol_routes = {}  # symbol -> dominant path

    def map_symbol(self, symbol: str, market_data: Dict) -> Dict:
        """Map the abyssal topology for a symbol"""
        data = market_data.get(symbol, {})
        dark_pool_ratio = data.get('dark_pool_ratio', 0.35)
        hft_ratio = data.get('hft_ratio', 0.5)
        internalizer_share = data.get('internalizer_share', 0.33)

        # Determine dominant routing
        if internalizer_share > 0.4:
            route = ['CITADEL', 'VIRTU'] + (['NYSE'] if np.random.rand() > 0.5 else ['NASDAQ'])
        elif dark_pool_ratio > 0.4:
            route = ['X_TX', 'LIQUIDNET', 'LEVEL'] + ['NYSE']
        else:
            route = ['NYSE', 'NASDAQ', 'BATS']

        self.symbol_routes[symbol] = route

        # Calculate toxicity of the path
        path_toxicity = np.mean([self.nodes[n].toxicity for n in route if n in self.nodes])

        # Predator presence
        predators = [n for n in route if self.nodes.get(n, AbyssalNode('', '', 0, 0, 0)).predatory]

        return {
            'symbol': symbol,
            'dominant_route': route,
            'dark_pool_ratio': dark_pool_ratio,
            'internalizer_share': internalizer_share,
            'path_toxicity': path_toxicity,
            'predators_on_path': predators,
            'estimated_adverse_selection': path_toxicity * dark_pool_ratio,
            'abyssal_depth': len([n for n in route if self.nodes.get(n, AbyssalNode('', '', 0, 0, 0)).type == 'dark_pool']),
        }

    def get_node(self, name: str) -> Optional[AbyssalNode]:
        return self.nodes.get(name)

    def all_predators(self) -> List[AbyssalNode]:
        return [n for n in self.nodes.values() if n.predatory]

    def total_dark_volume(self) -> float:
        return sum(n.volume_share for n in self.nodes.values() if n.type == 'dark_pool')

    def total_internalizer_volume(self) -> float:
        return sum(n.volume_share for n in self.nodes.values() if n.type == 'internalizer')