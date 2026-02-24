import numpy as np
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

def sample_size_two_proportion(p1, p2, alpha=0.05, power=0.8, ratio=1.0):
    """Required sample sizes for two-proportion z-test."""
    effect_size = proportion_effectsize(p1, p2)
    analysis = NormalIndPower()
    n1 = analysis.solve_power(effect_size=effect_size, power=power, alpha=alpha, ratio=ratio, alternative='two-sided')
    n1 = int(np.ceil(n1))
    n2 = int(np.ceil(n1 * ratio))
    return n1, n2, n1 + n2, effect_size

def days_to_run(n1, n2, daily_traffic, traffic_allocation=1.0, allocation_ratio=1.0):
    """Days needed so both control and treatment reach their required sizes."""
    test_traffic_per_day = daily_traffic * traffic_allocation
    daily_n1 = test_traffic_per_day * 1 / (1 + allocation_ratio)
    daily_n2 = test_traffic_per_day * allocation_ratio / (1 + allocation_ratio)
    days_for_control = n1 / daily_n1 if daily_n1 > 0 else np.inf
    days_for_treatment = n2 / daily_n2 if daily_n2 > 0 else np.inf
    return max(days_for_control, days_for_treatment), daily_n1, daily_n2

def run_calculation(baseline_conversion_rate, expected_relative_pct_change,
                    daily_traffic, statistical_power=0.80, significance_level=0.05,
                    traffic_allocation=1.0, allocation_ratio=1.0):
    """Single entry point — this is what FastAPI will call."""
    p1 = baseline_conversion_rate / 100
    p2 = p1 * (1 + expected_relative_pct_change / 100)

    n1, n2, total_n, effect_size = sample_size_two_proportion(
        p1, p2, alpha=significance_level, power=statistical_power, ratio=allocation_ratio
    )
    days_needed, daily_n1, daily_n2 = days_to_run(
        n1, n2, daily_traffic, traffic_allocation, allocation_ratio
    )
    days_rounded = int(np.ceil(days_needed))

    return {
        "p1": p1, "p2": p2,
        "n1": n1, "n2": n2, "total_n": total_n,
        "effect_size": round(effect_size, 4),
        "daily_n1": daily_n1, "daily_n2": daily_n2,
        "days_needed": round(days_needed, 1),
        "days_rounded": days_rounded,
    }