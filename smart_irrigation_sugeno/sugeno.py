"""Zero-order Sugeno inference engine for irrigation duration."""
from dataclasses import dataclass
from typing import Dict, List
from membership import SOIL_MOISTURE_SETS, TEMPERATURE_SETS, fuzzify

# Output constants in minutes. Rows are soil moisture; columns are temperature.
# These are illustrative project-design values, not agronomic recommendations.
OUTPUT_CONSTANTS = {
    ("Low", "Low"): 7.0,
    ("Low", "Medium"): 8.0,
    ("Low", "High"): 10.0,
    ("Medium", "Low"): 3.0,
    ("Medium", "Medium"): 4.0,
    ("Medium", "High"): 6.0,
    ("High", "Low"): 0.0,
    ("High", "Medium"): 0.0,
    ("High", "High"): 0.0,
}

@dataclass
class RuleResult:
    soil_set: str
    temperature_set: str
    soil_membership: float
    temperature_membership: float
    firing_strength: float
    output_minutes: float

def calculate_irrigation(soil_moisture: float, temperature: float) -> Dict:
    """Calculate the Sugeno weighted-average output and rule trace."""
    if not 0 <= soil_moisture <= 100:
        raise ValueError("Soil moisture must be between 0 and 100%.")
    if not 0 <= temperature <= 50:
        raise ValueError("Temperature must be between 0 and 50°C.")

    soil_degrees = fuzzify(soil_moisture, SOIL_MOISTURE_SETS)
    temp_degrees = fuzzify(temperature, TEMPERATURE_SETS)
    rule_results: List[RuleResult] = []

    for soil_set in SOIL_MOISTURE_SETS:
        for temp_set in TEMPERATURE_SETS:
            # AND operator: minimum membership degree.
            strength = min(soil_degrees[soil_set], temp_degrees[temp_set])
            rule_results.append(RuleResult(
                soil_set=soil_set,
                temperature_set=temp_set,
                soil_membership=soil_degrees[soil_set],
                temperature_membership=temp_degrees[temp_set],
                firing_strength=strength,
                output_minutes=OUTPUT_CONSTANTS[(soil_set, temp_set)],
            ))

    denominator = sum(rule.firing_strength for rule in rule_results)
    if denominator <= 0:
        raise ValueError("No fuzzy rule fired. Check the membership function definitions.")

    numerator = sum(rule.firing_strength * rule.output_minutes for rule in rule_results)
    duration = numerator / denominator
    duration = max(0.0, min(10.0, duration))

    active_rules = [
        {
            "Rule": f"IF soil moisture is {r.soil_set} AND temperature is {r.temperature_set}",
            "Soil membership": round(r.soil_membership, 3),
            "Temperature membership": round(r.temperature_membership, 3),
            "Firing strength": round(r.firing_strength, 3),
            "Sugeno output (min)": r.output_minutes,
            "Weighted contribution": round(r.firing_strength * r.output_minutes, 3),
        }
        for r in rule_results if r.firing_strength > 0
    ]
    active_rules.sort(key=lambda item: item["Firing strength"], reverse=True)

    if duration < 0.5:
        category = "No irrigation"
        explanation = "Soil moisture is high enough in this model; irrigation is not recommended."
    elif duration < 3.5:
        category = "Low"
        explanation = "Only a short irrigation duration is suggested by the model."
    elif duration < 7.0:
        category = "Moderate"
        explanation = "A moderate irrigation duration is suggested by the model."
    else:
        category = "High"
        explanation = "A longer irrigation duration is suggested by the model."

    return {
        "duration_minutes": duration,
        "category": category,
        "explanation": explanation,
        "soil_memberships": soil_degrees,
        "temperature_memberships": temp_degrees,
        "active_rules": active_rules,
        "weighted_sum": numerator,
        "strength_sum": denominator,
    }
