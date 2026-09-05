#!/usr/bin/env python3
"""RF Contract — Public Definitions and Exceptions.

This module is part of the PUBLIC ANNY distribution.
It defines the contract types and exceptions for the RF boundary.
It does NOT contain any private RF implementation.
"""


class RFUnavailableError(Exception):
    """Raised when the RF service is not available."""
    pass


class RFBypassError(Exception):
    """Raised when an attempt is made to bypass RF for a governed operation."""
    pass


class GitHubUnavailableError(Exception):
    """Raised when GitHub is not reachable for a durable operation."""
    pass


class RFOperationResult:
    """Result of an RF governed operation."""
    __slots__ = (
        "status", "rf_path_used", "direct_github_path_used",
        "governed_operation", "mutation_persisted", "commit_created",
        "source_sha", "result_sha", "authority_checked",
        "audit_emitted", "provenance_emitted", "records_created",
        "mission_id",
    )

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return {s: getattr(self, s, None) for s in self.__slots__}


class RFReconstructionResult:
    """Result of an RF state reconstruction."""
    __slots__ = (
        "rf_path_used", "direct_github_path_used",
        "reconstructed_sha", "l0", "l1_actors", "l2_actors", "actors",
    )

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self):
        return {s: getattr(self, s, None) for s in self.__slots__}
