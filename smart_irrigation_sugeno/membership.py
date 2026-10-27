"""Membership functions for the Smart Irrigation Sugeno FIS."""
from typing import Dict, Tuple

def triangular_membership(x: float, a: float, b: float, c: float) -> float:
    """Triangular membership with shoulder support when a == b or b == c."""
    x = float(x)
    if x < a or x > c:
        return 0.0
    if a == b and x <= b:
        return 1.0
    if b == c and x >= b:
        return 1.0
    if x == b:
        return 1.0
    if x < b:
        denominator = b - a
        return 1.0 if denominator == 0 else max(0.0, min(1.0, (x - a) / denominator))
    denominator = c - b
    return 1.0 if denominator == 0 else max(0.0, min(1.0, (c - x) / denominator))

SOIL_MOISTURE_SETS: Dict[str, Tuple[float, float, float]] = {
    "Low": (0, 0, 40),
    "Medium": (20, 50, 80),
    "High": (60, 100, 100),
}
TEMPERATURE_SETS: Dict[str, Tuple[float, float, float]] = {
    "Low": (0, 0, 20),
    "Medium": (10, 25, 40),
    "High": (30, 50, 50),
}

def fuzzify(value: float, sets: Dict[str, Tuple[float, float, float]]) -> Dict[str, float]:
    """Return the membership degree for each named fuzzy set."""
    return {name: triangular_membership(value, *params) for name, params in sets.items()}
