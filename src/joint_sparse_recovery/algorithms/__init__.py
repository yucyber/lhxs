"""Algorithm implementations for joint sparse recovery."""

from joint_sparse_recovery.algorithms.base import SparseRecoveryResult
from joint_sparse_recovery.algorithms.ra_somp_music import ra_somp_music
from joint_sparse_recovery.algorithms.scosamp import scosamp
from joint_sparse_recovery.algorithms.shtp import shtp, snhtp
from joint_sparse_recovery.algorithms.siht import siht, sniht

ALGORITHM_REGISTRY = {
    "SIHT": siht,
    "SNIHT": sniht,
    "SHTP": shtp,
    "SNHTP": snhtp,
    "SCoSaMP": scosamp,
    "RA-SOMP+MUSIC": ra_somp_music,
}

__all__ = [
    "ALGORITHM_REGISTRY",
    "SparseRecoveryResult",
    "ra_somp_music",
    "scosamp",
    "shtp",
    "siht",
    "sniht",
    "snhtp",
]
