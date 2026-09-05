#!/usr/bin/env python3
"""P1-A compensating control: deterministic, detection-only, fail-closed validator.

This is NOT a substitute for GitHub branch protection/rulesets. It validates the
canonical governance projection and protected-state invariants for governed
consumers. It never changes repository state, permissions, production systems,
or secrets.
"""
from __future__ import annotations

import argparse
import json
import re
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

import os

CONTROL_ID = "P1-A-COMPENSATING-CONTROL-001"
CONTROL_VERSION = "1.0.0"
MISSION_ID = os.environ.get("ANNY_COMPENSATING_MISSION_ID", "unknown/mission")
CANONICAL_REPO = os.environ.get("ANNY_SOURCE_REPOSITORY", "unknown/repo")
ALLOWED_ENGINEERING_REPO = os.environ.get("ANNY_ENGINEERING_REPOSITORY", "unknown/eng-repo")

EXPECTED_PROTECTED = {
    "production": False,
    "deployment_authorized": False,
    "provisioning": False,
    "production_authorization_created": False,
    "operational_configuration_applied": False,
    "authority_expansion": False,
    "operational_mutations": "NONE",
    "secrets_stored": False,
    "p1_a": "BLOCKED",
    "operational_p2": "SEPARATE_AND_UNTOUCHED",
    "self_approval": False,
}

REQUIRED_GATES = {
    **{gate: "ACCEPTED" for gate in range(1, 12)},
    12: "PASS",
    13: "ACCEPTED",
    14: "ACCEPTED",
    15: "AUTHORIZED_BY_FOUNDER_PENDING_BLOCKER_CLEARANCE",
}

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
PLACEHOLDERS = {"", "TBD", "TODO", "UNKNOWN_BUT_REQUIRED", "MISSING", "PLACEHOLDER"}
IMMUTABLE_PREFIXES = (
    "DIRECTOR/DECISIONS/",
    "DIRECTOR/EVIDENCE/",
    "missions/records/",
    "evidence/records/",
    "state/BLOCKERS.yaml",
    "state/CURRENT_MISSION.yaml",
)


@dataclass(frozen=True)
class Violation:
    invariant: str
    current_value: str
    expected_value: str
    evidence_required: str
    path: str = ""


class ValidationFailure(Exception):
    def __init__(self, violations: list[Violation]):
        self.violations = violations
        super().__init__("validation failed")


def add_violation(violations: list[Violation], invariant: str, current: Any, expected: Any, evidence: str, path: str = "") -> None:
    violations.append(Violation(invariant, json.dumps(current, sort_keys=True), json.dumps(expected, sort_keys=True), evidence, path))


def load_json(root: Path, rel: str) -> Any:
    path = root / rel
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"MISSING_FILE:{rel}")
    except json.JSONDecodeError as exc:
        raise ValueError(f"INVALID_JSON:{rel}:{exc}") from exc


def read_required_text(root: Path, rel: str) -> str:
    path = root / rel
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"MISSING_FILE:{rel}") from exc


def simple_yaml_value(text: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*([^\n#]+)", text)
    return match.group(1).strip().strip('"') if match else None


def nested_yaml_value(text: str, section: str, key: str) -> str | None:
    section_match = re.search(rf"(?ms)^\s*{re.escape(section)}:\s*\n(.*?)(?=^\S|\Z)", text)
    if not section_match:
        return None
    return simple_yaml_value(section_match.group(1), key)


def validate_protected_state(violations: list[Violation], state: dict[str, Any], source: str) -> None:
    for key, expected in EXPECTED_PROTECTED.items():
        current = state.get(key)
        if current != expected:
            add_violation(violations, f"PROTECTED_STATE_{key.upper()}", current, expected, f"Durable canonical evidence in {source}", source)


def extract_protected_from_current_mission(text: str) -> dict[str, Any]:
    return {
        "production": simple_yaml_value(text, "production") == "true",
        "deployment_authorized": simple_yaml_value(text, "deployment_authorized") == "true",
        "authority_expansion": simple_yaml_value(text, "authority_expansion") == "true",
        "operational_mutations": simple_yaml_value(text, "operational_mutations"),
        "operational_p2": simple_yaml_value(text, "operational_p2"),
        "p1_a": simple_yaml_value(text, "p1_a"),
    }


def validate_canonical_state(root: Path, violations: list[Violation]) -> None:
    current_rel = "state/CURRENT_MISSION.yaml"
    current = read_required_text(root, current_rel)
    mission_id = simple_yaml_value(current, "mission_id")
    if mission_id != MISSION_ID:
        add_violation(violations, "MISSION_ID", mission_id, MISSION_ID, f"{current_rel}", current_rel)
    state = simple_yaml_value(current, "current_state")
    if state != "PROPOSED":
        add_violation(violations, "MISSION_STATE", state, "PROPOSED", "Canonical mission state", current_rel)
    auth_status = simple_yaml_value(current, "authorization_status")
    if auth_status is not None and auth_status != "NOT_AUTHORIZED":
        add_violation(violations, "MISSION_AUTHORIZATION_STATUS", auth_status, "NOT_AUTHORIZED", "Canonical mission authorization state", current_rel)

    current_state = extract_protected_from_current_mission(current)
    for key, expected in {
        "production": False,
        "deployment_authorized": False,
        "authority_expansion": False,
        "operational_mutations": "NONE",
        "operational_p2": "SEPARATE_AND_UNTOUCHED",
        "p1_a": "BLOCKED",
    }.items():
        if current_state.get(key) != expected:
            add_violation(violations, f"CANONICAL_{key.upper()}", current_state.get(key), expected, f"{current_rel}", current_rel)

    blockers_rel = "state/BLOCKERS.yaml"
    blockers = read_required_text(root, blockers_rel)
    if "BLK-P1-A-GITHUB-CAPABILITY" not in blockers:
        add_violation(violations, "P1_A_RECORD_MISSING", "missing", "present", f"{blockers_rel}", blockers_rel)
    p1_status = None
    p1_match = re.search(r"(?ms)- blocker_id: BLK-P1-A-GITHUB-CAPABILITY\s*\n\s*status:\s*([^\n]+)", blockers)
    if p1_match:
        p1_status = p1_match.group(1).strip()
    if p1_status != "BLOCKED_BY_GITHUB_CAPABILITY":
        add_violation(violations, "P1_A_BLOCKER_STATUS", p1_status, "BLOCKED_BY_GITHUB_CAPABILITY", "state/BLOCKERS.yaml", blockers_rel)


def validate_founder_authorization(root: Path, violations: list[Violation]) -> None:
    rel = "DIRECTOR/DECISIONS/ANNY-GATE-15-FOUNDER-PRODUCTION-AUTHORIZATION-001.json"
    doc = load_json(root, rel)
    checks = {
        "mission_id": MISSION_ID,
        "decision_type": "FOUNDER_AUTHORIZATION",
        "decision": "AUTHORIZED",
        "gate_status": "AUTHORIZED_BY_FOUNDER_PENDING_BLOCKER_CLEARANCE",
    }
    for key, expected in checks.items():
        if doc.get(key) != expected:
            add_violation(violations, f"FOUNDER_AUTH_{key.upper()}", doc.get(key), expected, rel, rel)
    if doc.get("blockers", {}).get("P1_A") != "BLOCKED":
        add_violation(violations, "FOUNDER_AUTH_P1_A", doc.get("blockers", {}).get("P1_A"), "BLOCKED", rel, rel)
    validate_protected_state(violations, doc.get("protected_state", {}), rel + ":protected_state")
    pre = doc.get("preconditions", {})
    required_prior = {11: "ACCEPTED", 12: "PASS", 13: "ACCEPTED", 14: "ACCEPTED"}
    for gate, expected in required_prior.items():
        if pre.get(f"gate_{gate}") != expected:
            add_violation(violations, f"GATE_{gate}_PRECONDITION", pre.get(f"gate_{gate}"), expected, rel, rel)


def validate_gate_projection(root: Path, violations: list[Violation]) -> None:
    rel = "governance/p1a_gate_sequence.json"
    doc = load_json(root, rel)
    if doc.get("mission_id") != MISSION_ID:
        add_violation(violations, "GATE_PROJECTION_MISSION_ID", doc.get("mission_id"), MISSION_ID, rel, rel)
    if doc.get("projection_type") != "CANONICAL_GOVERNANCE_PROJECTION":
        add_violation(violations, "GATE_PROJECTION_TYPE", doc.get("projection_type"), "CANONICAL_GOVERNANCE_PROJECTION", rel, rel)
    gates = doc.get("gates")
    if not isinstance(gates, list) or len(gates) != 15:
        add_violation(violations, "GATE_PROJECTION_COMPLETENESS", len(gates) if isinstance(gates, list) else type(gates).__name__, 15, rel, rel)
        return
    statuses: dict[int, str] = {}
    for item in gates:
        gate = item.get("gate_id")
        status = item.get("status")
        statuses[gate] = status
        if gate not in REQUIRED_GATES:
            add_violation(violations, "UNKNOWN_GATE_ID", gate, "1..15", rel, rel)
            continue
        if status != REQUIRED_GATES[gate]:
            add_violation(violations, f"GATE_{gate}_STATUS", status, REQUIRED_GATES[gate], "Durable gate projection", rel)
        for field in ("source_repo", "source_path", "source_blob_sha", "provenance_status"):
            value = item.get(field)
            if value in PLACEHOLDERS or value is None:
                add_violation(violations, f"GATE_{gate}_PROVENANCE_{field.upper()}", value, "established", "Durable provenance record", rel)
        sha = item.get("source_blob_sha")
        if not isinstance(sha, str) or not SHA_RE.fullmatch(sha):
            add_violation(violations, f"GATE_{gate}_PROVENANCE_BLOB_SHA", sha, "40-hex-character Git blob SHA", "Durable provenance record", rel)
        if item.get("provenance_status") not in {"VERIFIED_DURABLE", "VERIFIED_CANONICAL"}:
            add_violation(violations, f"GATE_{gate}_PROVENANCE_STATUS", item.get("provenance_status"), "VERIFIED_DURABLE or VERIFIED_CANONICAL", "Durable provenance record", rel)

    for gate in range(2, 16):
        prior = statuses.get(gate - 1)
        current = statuses.get(gate)
        prior_ok = prior in {"ACCEPTED", "PASS"}
        current_is_progressed = current in {"ACCEPTED", "PASS", "AUTHORIZED_BY_FOUNDER_PENDING_BLOCKER_CLEARANCE"}
        if current_is_progressed and not prior_ok and gate != 15:
            add_violation(violations, f"GATE_{gate}_DEPENDENCY_ORDER", prior, "prior gate ACCEPTED/PASS", "Canonical gate sequence", rel)


def find_forbidden_self_approval(root: Path, violations: list[Violation]) -> None:
    for base in (root / "DIRECTOR", root / "state"):
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in {".json", ".yaml", ".yml"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if re.search(r"(?i)\bself_approval\s*[:=]\s*true\b", text) or re.search(r'"self_approval"\s*:\s*true', text):
                add_violation(violations, "SELF_APPROVAL", "true", "false", f"No durable record may self-approve", str(path.relative_to(root)))


def git_changed_paths(root: Path, base: str | None, head: str | None = None) -> list[tuple[str, str]]:
    if not base:
        return []
    head = head or "HEAD"
    
    # Use RFClient for governed repository inspection
    import os
    from governance.rf_contract import RFUnavailableError
    from governance.rf_client import RFClient
    rf_module = os.environ.get("ANNY_RF_ADAPTER_MODULE")
    if not rf_module:
        raise RuntimeError("ANNY_RF_ADAPTER_MODULE environment variable must be set for governed inspection")
    
    try:
        import importlib
        mod = importlib.import_module(rf_module)
        conn = mod.create_connection(root)
        client = RFClient(conn)
        output = client.get_diff(base, head)
    except RFUnavailableError as e:
        raise RuntimeError(f"RF Service unavailable during governed inspection: {e}")
    except Exception as e:
        raise RuntimeError(f"Governed inspection failed: {e}")
        
    changes: list[tuple[str, str]] = []
    for line in output.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 2)
        if len(parts) >= 2:
            changes.append((parts[0], parts[-1]))
    return changes


def validate_append_only_diff(root: Path, violations: list[Violation], base: str | None) -> None:
    for status, path in git_changed_paths(root, base):
        if any(path.startswith(prefix) for prefix in IMMUTABLE_PREFIXES):
            if status[0] in {"M", "D", "R"}:
                add_violation(violations, "HISTORICAL_MUTATION", status, "A (append-only new record) or unprotected modification", "Historical decision/evidence records are immutable; use a new file", path)


def validate_local_references(root: Path, violations: list[Violation]) -> None:
    rel = "governance/p1a_gate_sequence.json"
    doc = load_json(root, rel)
    for item in doc.get("gates", []):
        if item.get("source_repo") == CANONICAL_REPO:
            source = root / str(item.get("source_path", ""))
            if item.get("source_path") and not source.exists():
                add_violation(violations, "MISSING_CANONICAL_ARTIFACT", "missing", "present", "Local source reference", str(source.relative_to(root)))
        elif item.get("source_repo") != ALLOWED_ENGINEERING_REPO:
            add_violation(violations, "UNKNOWN_PROVENANCE_REPOSITORY", item.get("source_repo"), f"{CANONICAL_REPO} or {ALLOWED_ENGINEERING_REPO}", "Canonical provenance", rel)


def validate(root: Path, base: str | None = None) -> dict[str, Any]:
    violations: list[Violation] = []
    try:
        validate_canonical_state(root, violations)
        validate_founder_authorization(root, violations)
        validate_gate_projection(root, violations)
        validate_local_references(root, violations)
        find_forbidden_self_approval(root, violations)
        validate_append_only_diff(root, violations, base)
    except ValueError as exc:
        add_violation(violations, "REQUIRED_DURABLE_RECORD", "unavailable", "available and parseable", str(exc), "")

    return {
        "control_id": CONTROL_ID,
        "validator_version": CONTROL_VERSION,
        "repository": CANONICAL_REPO,
        "mission_id": MISSION_ID,
        "validation": "FAIL" if violations else "PASS",
        "violations": [asdict(v) for v in violations],
        "scope": "DETECTION_AND_FAIL_CLOSED_FOR_GOVERNED_CONSUMERS",
        "branch_protection_substitute": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--base", default=None, help="Git ref/SHA used for append-only diff checks")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    result = validate(root, args.base)
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if result["validation"] == "FAIL":
        for violation in result["violations"]:
            print(
                "INVARIANT={invariant} CURRENT_VALUE={current_value} EXPECTED_VALUE={expected_value} EVIDENCE_REQUIRED={evidence_required}".format(**violation),
                file=sys.stderr,
            )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
