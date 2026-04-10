"""Experiment orchestration modules."""

from joint_sparse_recovery.experiments.rank_aware_compare import run_rank_aware_comparison
from joint_sparse_recovery.experiments.step_size_compare import run_step_size_comparison
from joint_sparse_recovery.experiments.strong_phase import run_strong_phase_experiment
from joint_sparse_recovery.experiments.weak_phase import run_weak_phase_experiment

__all__ = [
    "run_rank_aware_comparison",
    "run_step_size_comparison",
    "run_strong_phase_experiment",
    "run_weak_phase_experiment",
]
