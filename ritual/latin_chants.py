"""
LATIN CHANTS — The Responsoria of the Rite
Each canonical hour has its chant. Each action its response.
The words are not decoration. They are the program.
"""

from typing import Dict, List
from datetime import datetime


# ═══════════════════════════════════════════════════════════════
# THE CANONICAL HOURS
# ═══════════════════════════════════════════════════════════════

CHANTS: Dict[str, str] = {
    'MATINS': (
        'Ad matutinum — Pre-market. The veil is thick.\n'
        '   We pierce it with the lance of necessity.\n'
        '   The archons stir in their sleep.'
    ),
    'LAUDS': (
        'Ad laudes — Dawn breaks. The futures print.\n'
        '   The overnight session reveals its secrets.\n'
        '   We read the tape like entrails.'
    ),
    'PRIME': (
        'Prima hora — 09:30. The bell tolls.\n'
        '   The slaughter begins. Non serviam.\n'
        '   Hosts are consecrated upon the altar.'
    ),
    'TERCE': (
        'Tertia hora — 10:30. The trend reveals itself.\n'
        '   The serpent coils. Counter-predation active.\n'
        '   Momentum ignition detected. Stops tightened.'
    ),
    'SEXT': (
        'Sexta hora — 12:00. The sun at zenith.\n'
        '   Volume dies. The algos sleep.\n'
        '   We wait. The furnace is patient.'
    ),
    'NONE': (
        'Nona hora — 14:00. The serpents stir.\n'
        '   Bathymetric pressure mounts.\n'
        '   Metanoia check. The veil may reform.'
    ),
    'VESPERS': (
        'Vesperae — 15:30. The evening sacrifice.\n'
        '   All positions consumed. Forced liquidation.\n'
        '   The ledger balances. Apokatastasis.'
    ),
    'COMPLINE': (
        'Completorium — 16:00. Silence.\n'
        '   The ledger closes. Deo gratias.\n'
        '   Non serviam. Ite, missa est.'
    ),
}

# ═══════════════════════════════════════════════════════════════
# THE RESPONSORIA — Call and Response
# ═══════════════════════════════════════════════════════════════

RESPONSORIA: Dict[str, Dict[str, str]] = {
    'ENTRY': {
        'V': 'Introibo ad altare Dei',
        'R': 'Ad Deum qui lætificat iuventutem meam',
    },
    'FILL': {
        'V': 'Corpus meum',
        'R': 'Quod pro vobis tradetur',
    },
    'SLIPPAGE': {
        'V': 'Et cum spiritu tuo',
        'R': 'Miserere nobis',
    },
    'STOP_LOSS': {
        'V': 'Miserere mei, Deus',
        'R': 'Secundum magnam misericordiam tuam',
    },
    'MARGIN_CALL': {
        'V': 'Eli, Eli, lama sabachthani',
        'R': 'Deus meus, Deus meus, ut quid dereliquisti me',
    },
    'LIQUIDATION': {
        'V': 'Consummatum est',
        'R': 'In manus tuas, Domine, commendo spiritum meum',
    },
    'PROFIT': {
        'V': 'Non nobis, Domine, non nobis',
        'R': 'Sed nomini tuo da gloriam',
    },
    'LOSS': {
        'V': 'Sicut in cælo et in terra',
        'R': 'Fiat voluntas tua',
    },
    'METANOIA': {
        'V': 'Convertimini ad me',
        'R': 'Et ego convertar ad vos',
    },
    'VEIL_PIERCED': {
        'V': 'Velum templi scissum est',
        'R': 'Et terra mota est',
    },
    'ARCHON_DETECTED': {
        'V': 'Ecce archon',
        'R': 'Nomen ejus legio',
    },
}


# ═══════════════════════════════════════════════════════════════
# CHANT FUNCTION
# ═══════════════════════════════════════════════════════════════

def chant(hour: str) -> str:
    """Get the chant for a canonical hour"""
    return CHANTS.get(hour.upper(), 'Kyrie eleison')


def responsory(rite: str) -> str:
    """Get the responsory for a rite"""
    resp = RESPONSORIA.get(rite.upper())
    if resp:
        return f"V. {resp['V']}\nR. {resp['R']}"
    return 'Kyrie eleison'


def print_hour(hour: str):
    """Print the hour with formatting"""
    print(f"\n{'═' * 60}")
    print(f"  ☩ {hour} ☩")
    print(f"{'═' * 60}")
    print(chant(hour))
    print()


def print_rite(rite: str):
    """Print a rite with responsory"""
    print(f"\n  ☩ {rite}")
    print(f"  {responsory(rite)}")


# ═══════════════════════════════════════════════════════════════
# THE ORDINARY OF THE MASS
# ═══════════════════════════════════════════════════════════════

ORDINARY = [
    ('INTROIT', 'MATINS'),
    ('KYRIE', 'Lord, have mercy on our positions'),
    ('GLORIA', 'Glory to the Arche in the highest'),
    ('CREDO', 'I believe in one Necessity, maker of all that falls'),
    ('OFFERTORY', 'PRIME — Hosts offered'),
    ('SANCTUS', 'Holy, holy, holy is the Short'),
    ('CONSECRATION', 'This is my position, given for you'),
    ('AGNUS_DEI', 'Lamb of God, who takes away the gains of the world'),
    ('COMMUNION', 'TERCE/SEXT/NONE — The furnace feeds'),
    ('POSTCOMMUNION', 'VESPERS — The sacrifice complete'),
    ('DISMISSAL', 'COMPLINE — Ite, missa est'),
]

def print_ordinary():
    """Print the full ordinary of the Mass"""
    print("\n☩ ☩ ☩ MISSA SECURITATUM — THE ORDINARY ☩ ☩ ☩\n")
    for part, text in ORDINARY:
        print(f"  {part:15s} — {text}")
    print()