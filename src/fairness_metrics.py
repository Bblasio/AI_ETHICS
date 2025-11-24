"""
Fairness metrics calculation and visualization utilities.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from aif360.metrics import ClassificationMetric
from aif360.algorithms.preprocessing import Reweighing

def calculate_fairness_metrics(dataset, privileged_groups, unprivileged_groups):
    """
    Calculate comprehensive fairness metrics.
    
    Args:
        dataset: AIF360 dataset object
        privileged_groups: List of privileged groups
        unprivileged_groups: List of unprivileged groups
        
    Returns:
        dict: Dictionary containing fairness metrics
    """
    # Split dataset
    train, test = dataset.split([0.7], shuffle=True, seed=42)
    
    # Calculate metrics
    metric = ClassificationMetric(
        test, 
        test,  # Using same set for demonstration
        unprivileged_groups=unprivileged_groups,
        privileged_groups=privileged_groups
    )
    
    metrics = {
        'disparate_impact': metric.disparate_impact(),
        'statistical_parity_difference': metric.statistical_parity_difference(),
        'equal_opportunity_difference': metric.equal_opportunity_difference(),
        'average_odds_difference': metric.average_odds_difference(),
        'theil_index': metric.theil_index()
    }
    
    return metrics

def plot_fairness_analysis(metrics_dict, save_path=None):
    """
    Create visualizations for fairness metrics.
    
    Args:
        metrics_dict (dict): Dictionary of fairness metrics
        save_path (str): Path to save the plot
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Key fairness metrics
    key_metrics = ['disparate_impact', 'statistical_parity_difference', 
                   'equal_opportunity_difference']
    values = [metrics_dict[metric] for metric in key_metrics]
    
    axes[0].bar(key_metrics, values, color=['skyblue', 'lightcoral', 'lightgreen'])
    axes[0].set_title('Key Fairness Metrics')
    axes[0].set_ylabel('Metric Value')
    axes[0].tick_params(axis='x', rotation=45)
    
    # Add ideal value lines
    axes[0].axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Ideal (Disparate Impact)')
    axes[0].axhline(y=0.0, color='blue', linestyle='--', alpha=0.7, label='Ideal (Parity)')
    axes[0].legend()
    
    # Plot 2: Metric interpretation
    metric_names = list(metrics_dict.keys())
    metric_values = list(metrics_dict.values())
    
    axes[1].bar(metric_names, metric_values, color='lightsteelblue')
    axes[1].set_title('All Fairness Metrics')
    axes[1].set_ylabel('Metric Value')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    plt.show()

def print_metrics_interpretation(metrics):
    """
    Print human-readable interpretation of fairness metrics.
    """
    print("\n" + "="*50)
    print("FAIRNESS METRICS INTERPRETATION")
    print("="*50)
    
    di = metrics['disparate_impact']
    if di < 0.8:
        print(f"⚠️  Disparate Impact: {di:.3f} - Potential adverse impact detected")
    elif di > 1.25:
        print(f"⚠️  Disparate Impact: {di:.3f} - Reverse discrimination possible")
    else:
        print(f"✅ Disparate Impact: {di:.3f} - Within acceptable range (0.8-1.25)")
    
    spd = metrics['statistical_parity_difference']
    if abs(spd) > 0.1:
        print(f"⚠️  Statistical Parity Difference: {spd:.3f} - Significant group difference")
    else:
        print(f"✅ Statistical Parity Difference: {spd:.3f} - Fair representation")