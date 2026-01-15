#!/usr/bin/env python3
"""
Calculate Comprehensive Statistics for Paper
Mean, SD, confidence intervals, t-tests for logic gate ratios
"""

import json
import math
from glob import glob

print("📊 CALCULATING COMPREHENSIVE STATISTICS FOR PAPER")
print("=" * 80)
print()

# Load metadata
with open('gcs-processes/metadata.json', 'r') as f:
    metadata = json.load(f)

processes = metadata['processes']
n = len(processes)

print(f"Analyzing {n} processes...")
print()

# Extract data
conditionals = [p.get('conditionals', 0) for p in processes]
or_gates = [p.get('logicGates', {}).get('or', 0) for p in processes]
and_gates = [p.get('logicGates', {}).get('and', 0) for p in processes]
not_gates = [p.get('notGates', 0) for p in processes]

# Calculate basic statistics
def calc_stats(data, name):
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / (n - 1)
    sd = math.sqrt(variance)
    se = sd / math.sqrt(n)
    
    # 95% confidence interval (t-distribution)
    # For n=100, t-critical ≈ 1.984
    t_critical = 1.984  # Two-tailed, 95% CI, df=99
    ci_lower = mean - t_critical * se
    ci_upper = mean + t_critical * se
    
    return {
        'n': n,
        'mean': mean,
        'sd': sd,
        'se': se,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'min': min(data),
        'max': max(data)
    }

# Calculate stats for each gate type
cond_stats = calc_stats(conditionals, 'Conditionals')
or_stats = calc_stats(or_gates, 'OR Gates')
and_stats = calc_stats(and_gates, 'AND Gates')
not_stats = calc_stats(not_gates, 'NOT Gates')

print("=" * 80)
print("BASIC STATISTICS (per process)")
print("=" * 80)
print()

stats_list = [
    ('Conditionals (IF-THEN)', cond_stats),
    ('OR Gates', or_stats),
    ('AND Gates', and_stats),
    ('NOT Gates', not_stats)
]

for name, stats in stats_list:
    print(f"{name}:")
    print(f"  Mean: {stats['mean']:.2f}")
    print(f"  SD: {stats['sd']:.2f}")
    print(f"  SE: {stats['se']:.2f}")
    print(f"  95% CI: [{stats['ci_lower']:.2f}, {stats['ci_upper']:.2f}]")
    print(f"  Range: [{stats['min']}, {stats['max']}]")
    print()

print("=" * 80)
print("RATIO STATISTICS (per process)")
print("=" * 80)
print()

# Calculate ratios for each process
or_and_ratios = []
or_not_ratios = []
and_not_ratios = []

for i in range(n):
    if and_gates[i] > 0:
        or_and_ratios.append(or_gates[i] / and_gates[i])
    if not_gates[i] > 0:
        or_not_ratios.append(or_gates[i] / not_gates[i])
        and_not_ratios.append(and_gates[i] / not_gates[i])

or_and_stats = calc_stats(or_and_ratios, 'OR:AND ratio')
or_not_stats = calc_stats(or_not_ratios, 'OR:NOT ratio') if len(or_not_ratios) > 0 else None
and_not_stats = calc_stats(and_not_ratios, 'AND:NOT ratio') if len(and_not_ratios) > 0 else None

print(f"OR:AND Ratio (n={len(or_and_ratios)} processes with AND gates):")
print(f"  Mean: {or_and_stats['mean']:.3f}")
print(f"  SD: {or_and_stats['sd']:.3f}")
print(f"  95% CI: [{or_and_stats['ci_lower']:.3f}, {or_and_stats['ci_upper']:.3f}]")
print()

if or_not_stats:
    print(f"OR:NOT Ratio (n={len(or_not_ratios)} processes with NOT gates):")
    print(f"  Mean: {or_not_stats['mean']:.3f}")
    print(f"  SD: {or_not_stats['sd']:.3f}")
    print(f"  95% CI: [{or_not_stats['ci_lower']:.3f}, {or_not_stats['ci_upper']:.3f}]")
    print()

if and_not_stats:
    print(f"AND:NOT Ratio (n={len(and_not_ratios)} processes with NOT gates):")
    print(f"  Mean: {and_not_stats['mean']:.3f}")
    print(f"  SD: {and_not_stats['sd']:.3f}")
    print(f"  95% CI: [{and_not_stats['ci_lower']:.3f}, {and_not_stats['ci_upper']:.3f}]")
    print()

print("=" * 80)
print("NORMALIZED ARCHITECTURE PATTERN")
print("=" * 80)
print()

# Calculate normalized ratios (per 100 conditionals)
total_cond = sum(conditionals)
total_or = sum(or_gates)
total_and = sum(and_gates)
total_not = sum(not_gates)

norm_or = (total_or / total_cond) * 100
norm_and = (total_and / total_cond) * 100
norm_not = (total_not / total_cond) * 100

print(f"Aggregate Architecture Pattern (all processes combined):")
print(f"  Total Conditionals: {total_cond}")
print(f"  Total OR Gates: {total_or}")
print(f"  Total AND Gates: {total_and}")
print(f"  Total NOT Gates: {total_not}")
print()
print(f"  Normalized to 100 conditionals:")
print(f"    100 : {norm_or:.1f} : {norm_and:.1f} : {norm_not:.1f}")
print(f"    100 : {round(norm_or)} : {round(norm_and)} : {round(norm_not)}")
print()

# Average per process approach
avg_cond = cond_stats['mean']
avg_or = or_stats['mean']
avg_and = and_stats['mean']
avg_not = not_stats['mean']

norm_or_avg = (avg_or / avg_cond) * 100
norm_and_avg = (avg_and / avg_cond) * 100
norm_not_avg = (avg_not / avg_cond) * 100

print(f"Average Architecture Pattern (mean per process):")
print(f"  Avg Conditionals: {avg_cond:.1f}")
print(f"  Avg OR Gates: {avg_or:.1f}")
print(f"  Avg AND Gates: {avg_and:.1f}")
print(f"  Avg NOT Gates: {avg_not:.1f}")
print()
print(f"  Normalized to 100 conditionals:")
print(f"    100 : {norm_or_avg:.1f} : {norm_and_avg:.1f} : {norm_not_avg:.1f}")
print(f"    100 : {round(norm_or_avg)} : {round(norm_and_avg)} : {round(norm_not_avg)}")
print()

print("=" * 80)
print("THEORETICAL VS OBSERVED")
print("=" * 80)
print()

theoretical = [100, 12, 6, 2]
observed = [100, round(norm_or), round(norm_and), round(norm_not)]

print(f"  Theoretical (100:12:6:2 Principle):")
print(f"    Conditionals : OR : AND : NOT")
print(f"    {theoretical[0]} : {theoretical[1]} : {theoretical[2]} : {theoretical[3]}")
print()
print(f"  Observed (Aggregate Data):")
print(f"    Conditionals : OR : AND : NOT")
print(f"    {observed[0]} : {observed[1]} : {observed[2]} : {observed[3]}")
print()

# Calculate percent difference
or_diff = ((observed[1] - theoretical[1]) / theoretical[1]) * 100
and_diff = ((observed[2] - theoretical[2]) / theoretical[2]) * 100
not_diff = ((observed[3] - theoretical[3]) / theoretical[3]) * 100

print(f"  Percent Difference from Theoretical:")
print(f"    OR Gates: {or_diff:+.1f}%")
print(f"    AND Gates: {and_diff:+.1f}%")
print(f"    NOT Gates: {not_diff:+.1f}%")
print()

print("=" * 80)
print("SUMMARY FOR PAPER")
print("=" * 80)
print()

print("KEY FINDINGS:")
print()
print(f"1. Conditionals: {cond_stats['mean']:.1f} ± {cond_stats['sd']:.1f} per process")
print(f"   (95% CI: {cond_stats['ci_lower']:.1f} to {cond_stats['ci_upper']:.1f})")
print()
print(f"2. OR Gates: {or_stats['mean']:.1f} ± {or_stats['sd']:.1f} per process")
print(f"   (95% CI: {or_stats['ci_lower']:.1f} to {or_stats['ci_upper']:.1f})")
print()
print(f"3. AND Gates: {and_stats['mean']:.1f} ± {and_stats['sd']:.1f} per process")
print(f"   (95% CI: {and_stats['ci_lower']:.1f} to {and_stats['ci_upper']:.1f})")
print()
print(f"4. NOT Gates: {not_stats['mean']:.1f} ± {not_stats['sd']:.1f} per process")
print(f"   (95% CI: {not_stats['ci_lower']:.1f} to {not_stats['ci_upper']:.1f})")
print()
print(f"5. Architecture Pattern: 100:{round(norm_or)}:{round(norm_and)}:{round(norm_not)}")
print(f"   (Theoretical: 100:12:6:2)")
print()
print(f"6. OR:AND Ratio: {or_and_stats['mean']:.2f} ± {or_and_stats['sd']:.2f}")
print()

print("=" * 80)

# Save to JSON for paper
results = {
    'n_processes': n,
    'conditionals': {
        'mean': round(cond_stats['mean'], 2),
        'sd': round(cond_stats['sd'], 2),
        'ci_95': [round(cond_stats['ci_lower'], 2), round(cond_stats['ci_upper'], 2)],
        'range': [cond_stats['min'], cond_stats['max']]
    },
    'or_gates': {
        'mean': round(or_stats['mean'], 2),
        'sd': round(or_stats['sd'], 2),
        'ci_95': [round(or_stats['ci_lower'], 2), round(or_stats['ci_upper'], 2)],
        'range': [or_stats['min'], or_stats['max']]
    },
    'and_gates': {
        'mean': round(and_stats['mean'], 2),
        'sd': round(and_stats['sd'], 2),
        'ci_95': [round(and_stats['ci_lower'], 2), round(and_stats['ci_upper'], 2)],
        'range': [and_stats['min'], and_stats['max']]
    },
    'not_gates': {
        'mean': round(not_stats['mean'], 2),
        'sd': round(not_stats['sd'], 2),
        'ci_95': [round(not_stats['ci_lower'], 2), round(not_stats['ci_upper'], 2)],
        'range': [not_stats['min'], not_stats['max']]
    },
    'architecture_pattern': {
        'observed': f"100:{round(norm_or)}:{round(norm_and)}:{round(norm_not)}",
        'theoretical': "100:12:6:2",
        'normalized_values': [100, round(norm_or, 1), round(norm_and, 1), round(norm_not, 1)]
    },
    'ratios': {
        'or_and': {
            'mean': round(or_and_stats['mean'], 3),
            'sd': round(or_and_stats['sd'], 3),
            'ci_95': [round(or_and_stats['ci_lower'], 3), round(or_and_stats['ci_upper'], 3)]
        }
    }
}

with open('paper_statistics.json', 'w') as f:
    json.dump(results, f, indent=2)

print()
print("✅ Statistics saved to paper_statistics.json")
print("=" * 80)

