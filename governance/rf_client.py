#!/usr/bin/env python3
"""RF Client — Public Distribution Boundary.

This module is part of the PUBLIC ANNY distribution.
It implements the RF Client which is strictly a protocol boundary connecting
to the private RF Service.

IT MUST NOT CONTAIN ANY PRIVATE IMPLEMENTATION SUCH AS:
- GitHub adapter implementations
- direct repository execution or durable mutation logic
- private governance enforcement internals
"""

from governance.rf_contract import (
    RFUnavailableError, 
    RFBypassError,
    RFOperationResult,
    RFReconstructionResult
)

class RFClient:
    """The public RF Client connecting ANNY to the Repository Fabric."""

    def __init__(self, connection_adapter):
        """Initialize with a connection adapter to the private RF service.
        
        The connection_adapter represents the network or IPC boundary 
        to the protected RF environment.
        """
        self._conn = connection_adapter

    def reconstruct_state(self) -> RFReconstructionResult:
        """Request state reconstruction from the RF service."""
        if not self._conn.is_available():
            raise RFUnavailableError("RF Service is unreachable.")
        
        # The client simply forwards the request to the private boundary.
        response = self._conn.send_request("reconstruct_state", {})
        
        return RFReconstructionResult(**response)

    def governed_mutation(self, request: dict) -> RFOperationResult:
        """Submit a governed mutation request to the RF service."""
        if not self._conn.is_available():
            raise RFUnavailableError("RF Service is unreachable.")
            
        # The client simply forwards the request to the private boundary.
        response = self._conn.send_request("governed_mutation", request)
        
        return RFOperationResult(**response)

    def get_local_sha(self) -> str:
        if not self._conn.is_available():
            raise RFUnavailableError("RF Service is unreachable.")
        return self._conn.send_request("get_local_sha", {})["sha"]

    def get_remote_sha(self) -> str:
        """Retrieve the canonical remote HEAD SHA without local mutation."""
        if not self._conn.is_available():
            raise RFUnavailableError("RF Service is unreachable.")
        return self._conn.send_request("get_remote_sha", {}).get("sha")

    def get_diff(self, base, head):
        """Retrieve the file differences between two SHAs."""
        if not self._conn.is_available():
            raise RFUnavailableError("RF Service is unreachable.")
        return self._conn.send_request("get_diff", {"base": base, "head": head}).get("diff", "")

    def sync_repository(self) -> None:
        if not self._conn.is_available():
            raise RFUnavailableError("RF Service is unreachable.")
        self._conn.send_request("sync_repository", {})

    def provision_repository(self, remote_url: str, target_path: str) -> None:
        if not self._conn.is_available():
            raise RFUnavailableError("RF Service is unreachable.")
        self._conn.send_request("provision_repository", {"remote_url": remote_url, "target_path": target_path})

