#!/usr/bin/env python3
"""ANNY Genesis Bootstrap - Creates a new organization from empty state.

This module implements the Genesis procedure defined in Phase 5H.
It reads GENESIS.yaml, validates the empty state, and provisions
the initial organizational structure.

NO instance-specific data. NO hardcoded actor names.
NO embedded credentials. NO Azure-specific endpoints.
"""
from __future__ import annotations

import datetime
import os
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

import yaml

from starter_pack.model import STANDARD_DEPARTMENTS
from starter_pack.generator import generate_starter_pack


@dataclass
class GenesisInput:
    """Inputs required to execute the Genesis procedure."""
    enterprise_name: str
    owner_identity: str
    github_repo: str  # owner/repo format
    azure_storage_account: Optional[str] = None
    # We no longer accept custom departments. Standard 17-actor structure is enforced.


@dataclass
class GenesisResult:
    """Result of a Genesis execution."""
    success: bool
    enterprise_name: str
    root_actor_id: str
    directors_created: list
    genesis_commit_sha: Optional[str] = None
    genesis_timestamp: str = ""
    error: Optional[str] = None


def _generate_actor_id(prefix: str) -> str:
    """Generate a unique actor ID."""
    short_uuid = uuid.uuid4().hex[:12].upper()
    return f"ACT-{prefix}-{short_uuid}"


def _create_actor_yaml(actor_id: str, name: str, actor_type: str,
                       role: str, department: str, level: str,
                       authority_level: str, parent: Optional[str] = None,
                       capabilities: list = None) -> dict:
    """Create an actor YAML record."""
    return {
        "actor_id": actor_id,
        "actor_type": actor_type,
        "name": name,
        "role": role,
        "department": department,
        "level": level,
        "authority_level": authority_level,
        "status": "ACTIVE",
        "authority_scope": ["*"] if level == "L0" else [department.lower()],
        "parent_director": parent,
        "capabilities": capabilities or [],
        "description": f"{role} for {department}",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
        "created_by": "GENESIS",
    }


def validate_genesis_state(repo_root: str) -> tuple:
    """Validate that the repository is in a valid Genesis state.
    
    Returns (is_valid, genesis_data, errors)
    """
    errors = []
    genesis_path = Path(repo_root) / "genesis" / "GENESIS.yaml"
    
    if not genesis_path.exists():
        return False, None, ["GENESIS.yaml not found"]
    
    with open(genesis_path, 'r') as f:
        genesis_data = yaml.safe_load(f)
    
    if genesis_data is None:
        return False, None, ["GENESIS.yaml is empty or invalid"]
    
    # Check genesis_state
    state = genesis_data.get("genesis_state")
    if state != "UNINITIALIZED":
        errors.append(f"genesis_state is '{state}', expected 'UNINITIALIZED'")
    
    # Check empty collections
    for collection in ["actors", "missions", "decisions", "evidence"]:
        val = genesis_data.get(collection)
        if val is not None and val != []:
            errors.append(f"{collection} must be empty, found: {val}")
    
    # Check enterprise is null
    enterprise = genesis_data.get("enterprise", {})
    for field_name in ["name", "owner", "authority_root"]:
        if enterprise and enterprise.get(field_name) is not None:
            errors.append(f"enterprise.{field_name} must be null")
    
    # Check actors directory is empty
    actors_dir = Path(repo_root) / "actors"
    if actors_dir.exists():
        actor_files = [f for f in actors_dir.iterdir() 
                       if f.suffix in ('.yaml', '.yml') and f.name != 'ACTOR_SCHEMA.yaml']
        if actor_files:
            errors.append(f"actors/ directory must be empty, found: {[f.name for f in actor_files]}")
    
    # Check missions directory is empty
    missions_dir = Path(repo_root) / "missions" / "records"
    if missions_dir.exists():
        mission_files = [f for f in missions_dir.iterdir() if f.name != '.gitkeep']
        if mission_files:
            errors.append(f"missions/records/ must be empty, found {len(mission_files)} files")
    
    return len(errors) == 0, genesis_data, errors


def execute_genesis(repo_root: str, genesis_input: GenesisInput) -> GenesisResult:
    """Execute the Genesis procedure to create a new organization.
    
    Steps:
    1. Validate Genesis state
    2. Create L0 root authority
    3. Create initial L1 directors
    4. Initialize state
    5. Update GENESIS.yaml
    6. Record genesis evidence
    """
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    repo = Path(repo_root)
    
    # Step 1: Validate
    is_valid, genesis_data, errors = validate_genesis_state(repo_root)
    if not is_valid:
        return GenesisResult(
            success=False,
            enterprise_name=genesis_input.enterprise_name,
            root_actor_id="",
            directors_created=[],
            genesis_timestamp=timestamp,
            error=f"Genesis validation failed: {errors}"
        )
    
    # Step 2: Create L0 root authority
    root_id = _generate_actor_id("ROOT")
    root_actor = _create_actor_yaml(
        actor_id=root_id,
        name=genesis_input.enterprise_name.upper(),
        actor_type="system",
        role="System Root",
        department="Executive",
        level="L0",
        authority_level="L0",
        capabilities=["full_authority", "delegate", "certify"]
    )
    
    # Ensure actors directory exists
    actors_dir = repo / "actors"
    actors_dir.mkdir(parents=True, exist_ok=True)
    
    root_path = actors_dir / f"{root_id}.yaml"
    with open(root_path, 'w') as f:
        yaml.dump(root_actor, f, default_flow_style=False, sort_keys=False)
    
    # Step 3: Create L1 directors and L2 workers
    directors_created = []
    workers_created = []
    
    for dept_model in STANDARD_DEPARTMENTS:
        dept = dept_model["name"]
        dir_name = dept_model["director_name"]
        work_name = dept_model["worker_name"]
        
        # Create L1
        director_id = _generate_actor_id(dept_model["prefix"])
        director = _create_actor_yaml(
            actor_id=director_id,
            name=dir_name,
            actor_type="director",
            role=f"Director of {dept}",
            department=dept,
            level="L1",
            authority_level="L1",
            parent=root_id,
            capabilities=["manage", "delegate", "execute"]
        )
        with open(actors_dir / f"{director_id}.yaml", 'w') as f:
            yaml.dump(director, f, default_flow_style=False, sort_keys=False)
        directors_created.append({"actor_id": director_id, "department": dept})
        
        # Create L2
        worker_id = _generate_actor_id(f"WORK")
        worker = _create_actor_yaml(
            actor_id=worker_id,
            name=work_name,
            actor_type="worker",
            role=f"{work_name} — {dept} Specialist",
            department=dept,
            level="L2",
            authority_level="L2",
            parent=director_id,
            capabilities=["execute"]
        )
        with open(actors_dir / f"{worker_id}.yaml", 'w') as f:
            yaml.dump(worker, f, default_flow_style=False, sort_keys=False)
        workers_created.append({"actor_id": worker_id, "department": dept})
    
    # Step 4: Initialize state
    state_dir = repo / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    
    current_state = {
        "state_version": "1.0",
        "enterprise_name": genesis_input.enterprise_name,
        "genesis_timestamp": timestamp,
        "current_phase": "GENESIS_COMPLETE",
        "owner": genesis_input.owner_identity,
        "github_repo": genesis_input.github_repo,
        "azure_storage_account": genesis_input.azure_storage_account,
    }
    with open(state_dir / "CURRENT_STATE.yaml", 'w') as f:
        yaml.dump(current_state, f, default_flow_style=False, sort_keys=False)
    
    blockers = {"blockers": []}
    with open(state_dir / "BLOCKERS.yaml", 'w') as f:
        yaml.dump(blockers, f, default_flow_style=False, sort_keys=False)
    
    # Step 5: Update GENESIS.yaml
    genesis_data["genesis_state"] = "INITIALIZED"
    genesis_data["enterprise"] = {
        "name": genesis_input.enterprise_name,
        "owner": genesis_input.owner_identity,
        "authority_root": root_id,
    }
    genesis_data["actors"] = [root_id] + [d["actor_id"] for d in directors_created] + [w["actor_id"] for w in workers_created]
    
    # We will generate IDs now so they can be injected into GENESIS.yaml
    decision_id = f"DEC-genesis-{uuid.uuid4().hex[:12].upper()}"
    evidence_id = f"EVD-genesis-{uuid.uuid4().hex[:12].upper()}"
    
    genesis_data["decisions"] = [decision_id]
    genesis_data["evidence"] = [evidence_id]
    
    if "topology" not in genesis_data:
        genesis_data["topology"] = {}
    genesis_data["topology"]["repositories"] = [genesis_input.github_repo]

    
    genesis_path = repo / "genesis" / "GENESIS.yaml"
    with open(genesis_path, 'w') as f:
        yaml.dump(genesis_data, f, default_flow_style=False, sort_keys=False)
    
    # Step 6: Ensure empty directories exist for instance state
    for subdir in [
        "missions/records", "decisions/records", "evidence/records",
        "messages/incoming", "messages/outgoing",
        "HANDOFFS", "audits", "certification", "fabric/records"
    ]:
        (repo / subdir).mkdir(parents=True, exist_ok=True)
        gitkeep = repo / subdir / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
            
    # Step 7: Record Genesis Decision and Evidence (IDs generated in Step 5)
    
    decision = {
        "decision_id": decision_id,
        "decision_type": "STRUCTURAL_PROVISIONING",
        "status": "APPROVED",
        "subject": "GENESIS_INITIALIZATION",
        "authority": "L0",
        "authority_scope": ["*"],
        "created_at": timestamp,
        "mission_id": "genesis",
        "decision": "INITIALIZE_ENTERPRISE",
        "rationale": "Phase 5H Genesis procedure execution.",
        "constraints": ["MUST_FOLLOW_GENESIS_CONTRACT"],
        "created_by": root_id
    }
    with open(repo / "decisions" / "records" / f"{decision_id}.yaml", 'w') as f:
        yaml.dump(decision, f, default_flow_style=False, sort_keys=False)
        
    evidence = {
        "evidence_id": evidence_id,
        "evidence_type": "PROVENANCE",
        "status": "VALIDATED",
        "content_hash": "genesis",
        "created_at": timestamp,
        "provenance": {
            "source": "bootstrap.py",
            "method": "GENESIS",
            "actor": root_id
        }
    }
    with open(repo / "evidence" / "records" / f"{evidence_id}.yaml", 'w') as f:
        yaml.dump(evidence, f, default_flow_style=False, sort_keys=False)
    
    # Step 8: Generate Customer Starter Pack
    generate_starter_pack(repo_root)
    
    return GenesisResult(
        success=True,
        enterprise_name=genesis_input.enterprise_name,
        root_actor_id=root_id,
        directors_created=directors_created,
        genesis_timestamp=timestamp,
    )


def main():
    """CLI entry point for Genesis bootstrap."""
    import argparse
    parser = argparse.ArgumentParser(description="ANNY Genesis Bootstrap")
    parser.add_argument("--repo-root", required=True, help="Path to the target repository")
    parser.add_argument("--enterprise-name", required=True, help="Name of the new enterprise")
    parser.add_argument("--owner", required=True, help="GitHub username of the owner")
    parser.add_argument("--github-repo", required=True, help="Target GitHub repo (owner/repo)")
    parser.add_argument("--azure-storage", default=None, help="Optional Azure storage account")
    parser.add_argument("--departments", nargs="+", default=["Engineering"],
                        help="Initial department names")
    args = parser.parse_args()
    
    genesis_input = GenesisInput(
        enterprise_name=args.enterprise_name,
        owner_identity=args.owner,
        github_repo=args.github_repo,
        azure_storage_account=args.azure_storage,
    )
    
    result = execute_genesis(args.repo_root, genesis_input)
    
    if result.success:
        print(f"GENESIS_STATUS=SUCCESS")
        print(f"ENTERPRISE={result.enterprise_name}")
        print(f"ROOT_ACTOR={result.root_actor_id}")
        print(f"DIRECTORS={[d['actor_id'] for d in result.directors_created]}")
        print(f"TIMESTAMP={result.genesis_timestamp}")
    else:
        print(f"GENESIS_STATUS=FAILED")
        print(f"ERROR={result.error}")
        sys.exit(1)


if __name__ == "__main__":
    import sys
    main()
