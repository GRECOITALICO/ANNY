"""Public GitHub principal contract for ANNY.

This module defines the public trust boundary used by ANNY when a deployment
connects to the private Repository Fabric service. Callers must not be able to
assert a GitHub identity by supplying a login or user id in a request payload.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from typing import Callable, Optional


@dataclass(frozen=True)
class GitHubIdentity:
    user_id: str
    login: str


class AuthenticationError(Exception):
    """Raised when an authenticated GitHub principal cannot be established."""


@dataclass(frozen=True)
class AuthenticatedGitHubPrincipal:
    identity: GitHubIdentity
    session_id: str
    issued_at: datetime
    expires_at: datetime
    provider: str = "github"

    def is_expired(self, now: Optional[datetime] = None) -> bool:
        current = now or datetime.now(timezone.utc)
        return current >= self.expires_at


class GitHubPrincipalAuthenticator:
    """Create a short-lived ANNY principal from a trusted GitHub identity source."""

    def __init__(self, identity_supplier: Callable[[], GitHubIdentity], ttl_seconds: int = 900):
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        self.identity_supplier = identity_supplier
        self.ttl_seconds = ttl_seconds

    def authenticate(self) -> AuthenticatedGitHubPrincipal:
        identity = self.identity_supplier()
        if not isinstance(identity, GitHubIdentity):
            raise AuthenticationError("Identity supplier did not return a GitHubIdentity")
        if not identity.user_id or not identity.login:
            raise AuthenticationError("Authenticated GitHub identity is incomplete")
        issued_at = datetime.now(timezone.utc)
        return AuthenticatedGitHubPrincipal(
            identity=identity,
            session_id=token_urlsafe(32),
            issued_at=issued_at,
            expires_at=issued_at + timedelta(seconds=self.ttl_seconds),
        )


def require_fresh_principal(principal: AuthenticatedGitHubPrincipal, now: Optional[datetime] = None) -> GitHubIdentity:
    if principal.provider != "github":
        raise AuthenticationError("Unsupported identity provider")
    if principal.is_expired(now):
        raise AuthenticationError("GitHub authentication session expired")
    return principal.identity
