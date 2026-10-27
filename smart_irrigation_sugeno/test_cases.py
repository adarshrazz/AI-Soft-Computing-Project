"""Run with: python test_cases.py"""
from sugeno import calculate_irrigation

CASES = [
    ("Dry soil, hot", 15, 40),
    ("Moderate conditions", 50, 25),
    ("Moist soil, hot", 85, 40),
    ("Wet soil, cool", 90, 15),
]

def main():
    print(f"{'Scenario':<24} {'Moisture':>9} {'Temp':>7} {'Duration':>12} {'Category':>16}")
    print("-" * 74)
    for name, soil, temp in CASES:
        result = calculate_irrigation(soil, temp)
        print(f"{name:<24} {soil:>8}% {temp:>6}C {result['duration_minutes']:>11.2f} {result['category']:>16}")

    # Basic invariants
    for soil in range(0, 101, 5):
        for temp in range(0, 51, 5):
            result = calculate_irrigation(soil, temp)
            assert 0 <= result["duration_minutes"] <= 10
    assert calculate_irrigation(100, 25)["duration_minutes"] == 0
    print("\nAll range and invariant checks passed.")

if __name__ == "__main__":
    main()
