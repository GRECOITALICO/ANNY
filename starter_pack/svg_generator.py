#!/usr/bin/env python3
"""ANNY SVG Diagram Generator.

Generates organizational diagrams as inline SVG XML from canonical data.
No external rendering dependencies required.
"""
from __future__ import annotations


def _svg_header(width: int, height: int) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" font-family="Arial, Helvetica, sans-serif">\n'


def _svg_footer() -> str:
    return '</svg>\n'


def _svg_rect(x, y, w, h, fill, stroke="#333", rx=8, opacity=1.0) -> str:
    return f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="1.5" opacity="{opacity}"/>\n'


def _svg_text(x, y, text, size=14, anchor="middle", weight="normal", fill="#222") -> str:
    return f'  <text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}">{text}</text>\n'


def _svg_line(x1, y1, x2, y2, stroke="#666", width=1.5, dash="") -> str:
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}"{d}/>\n'


def _svg_arrow(x1, y1, x2, y2, stroke="#666", width=1.5) -> str:
    mid = "arrow_marker"
    return (
        f'  <defs><marker id="{mid}" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">'
        f'<polygon points="0 0, 10 3.5, 0 7" fill="{stroke}"/></marker></defs>\n'
        f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{width}" marker-end="url(#{mid})"/>\n'
    )


# =====================================================================
# ORGANIZATION CHART
# =====================================================================

def generate_org_chart_svg(snap) -> str:
    """Generate an organization chart SVG from the canonical snapshot."""
    departments = sorted(snap.departments.keys())
    n = len(departments)

    col_w = 160
    col_gap = 20
    total_w = max(n * (col_w + col_gap) + 80, 800)
    total_h = 420

    svg = _svg_header(total_w, total_h)

    # Background
    svg += _svg_rect(0, 0, total_w, total_h, "#f8f9fa", stroke="none")

    # Title
    svg += _svg_text(total_w // 2, 30, "Organization Chart", size=20, weight="bold")

    # L0 box
    l0_name = snap.l0["name"] if snap.l0 else "L0"
    l0_x = total_w // 2 - 80
    svg += _svg_rect(l0_x, 50, 160, 50, "#1a73e8")
    svg += _svg_text(total_w // 2, 75, l0_name, size=16, weight="bold", fill="white")
    svg += _svg_text(total_w // 2, 92, "L0 — Root Authority", size=10, fill="#cce0ff")

    # L1 + L2 columns
    start_x = 40
    for i, dept in enumerate(departments):
        data = snap.departments[dept]
        director = data.get("director")
        worker = data.get("worker")

        cx = start_x + i * (col_w + col_gap) + col_w // 2

        # Line from L0 to L1
        svg += _svg_line(total_w // 2, 100, cx, 150, stroke="#1a73e8")

        # L1 box
        d_name = director["name"] if director else "—"
        svg += _svg_rect(cx - col_w // 2, 150, col_w, 60, "#34a853")
        svg += _svg_text(cx, 175, d_name, size=14, weight="bold", fill="white")
        svg += _svg_text(cx, 195, f"L1 — {dept[:18]}", size=9, fill="#c6f0d0")

        # Line from L1 to L2
        svg += _svg_line(cx, 210, cx, 260, stroke="#34a853")

        # L2 box
        w_name = worker["name"] if worker else "—"
        svg += _svg_rect(cx - col_w // 2, 260, col_w, 60, "#fbbc04")
        svg += _svg_text(cx, 285, w_name, size=14, weight="bold", fill="#333")
        svg += _svg_text(cx, 305, f"L2 — {dept[:18]}", size=9, fill="#665500")

    # Legend
    ly = total_h - 50
    svg += _svg_rect(20, ly, 20, 15, "#1a73e8", rx=3)
    svg += _svg_text(50, ly + 12, "L0 — Authority", size=11, anchor="start")
    svg += _svg_rect(200, ly, 20, 15, "#34a853", rx=3)
    svg += _svg_text(230, ly + 12, "L1 — Directors", size=11, anchor="start")
    svg += _svg_rect(380, ly, 20, 15, "#fbbc04", rx=3)
    svg += _svg_text(410, ly + 12, "L2 — Specialists", size=11, anchor="start")

    svg += _svg_footer()
    return svg


# =====================================================================
# AUTHORITY MAP
# =====================================================================

def generate_authority_map_svg(snap) -> str:
    """Generate an authority map showing permission flows."""
    departments = sorted(snap.departments.keys())
    n = len(departments)
    total_w = max(n * 180 + 80, 800)
    total_h = 500

    svg = _svg_header(total_w, total_h)
    svg += _svg_rect(0, 0, total_w, total_h, "#fafafa", stroke="none")
    svg += _svg_text(total_w // 2, 30, "Authority Map", size=20, weight="bold")

    # L0
    l0_name = snap.l0["name"] if snap.l0 else "L0"
    svg += _svg_rect(total_w // 2 - 120, 50, 240, 55, "#1a73e8")
    svg += _svg_text(total_w // 2, 75, f"{l0_name} — FULL AUTHORITY", size=14, weight="bold", fill="white")
    svg += _svg_text(total_w // 2, 95, "Can: create, delegate, certify, audit", size=9, fill="#cce0ff")

    for i, dept in enumerate(departments):
        data = snap.departments[dept]
        director = data.get("director")
        worker = data.get("worker")
        cx = 90 + i * 170

        svg += _svg_line(total_w // 2, 105, cx, 140, stroke="#1a73e8", dash="4,4")

        d_name = director["name"] if director else "—"
        svg += _svg_rect(cx - 70, 140, 140, 55, "#34a853")
        svg += _svg_text(cx, 162, d_name, size=12, weight="bold", fill="white")
        svg += _svg_text(cx, 180, f"{dept[:16]} only", size=9, fill="#c6f0d0")

        svg += _svg_line(cx, 195, cx, 240, stroke="#34a853", dash="4,4")

        w_name = worker["name"] if worker else "—"
        svg += _svg_rect(cx - 70, 240, 140, 55, "#fbbc04")
        svg += _svg_text(cx, 262, w_name, size=12, weight="bold", fill="#333")
        svg += _svg_text(cx, 280, "Tasks only", size=9, fill="#665500")

    # Rules
    ry = 340
    svg += _svg_text(total_w // 2, ry, "Authority Rules", size=16, weight="bold")
    rules = [
        "L2 CANNOT promote itself",
        "L1 CANNOT act outside department",
        "L0 is the ONLY cross-department authority",
        "Authority is NEVER self-assigned",
    ]
    for j, r in enumerate(rules):
        svg += _svg_text(total_w // 2, ry + 25 + j * 22, r, size=12, fill="#c62828")

    svg += _svg_footer()
    return svg


# =====================================================================
# MISSION LIFECYCLE
# =====================================================================

def generate_mission_lifecycle_svg() -> str:
    """Generate a mission lifecycle state diagram."""
    total_w = 700
    total_h = 350

    svg = _svg_header(total_w, total_h)
    svg += _svg_rect(0, 0, total_w, total_h, "#fafafa", stroke="none")
    svg += _svg_text(total_w // 2, 30, "Mission Lifecycle", size=20, weight="bold")

    states = [
        ("CREATED", 80, 100, "#e3f2fd", "#1565c0"),
        ("DELEGATED", 230, 100, "#e8f5e9", "#2e7d32"),
        ("IN_PROGRESS", 380, 100, "#fff3e0", "#e65100"),
        ("REVIEW", 530, 100, "#f3e5f5", "#6a1b9a"),
        ("COMPLETED", 530, 230, "#e8f5e9", "#1b5e20"),
        ("FAILED", 230, 230, "#ffebee", "#b71c1c"),
    ]

    for name, x, y, fill, text_color in states:
        svg += _svg_rect(x - 60, y - 20, 120, 40, fill, stroke=text_color)
        svg += _svg_text(x, y + 5, name, size=11, weight="bold", fill=text_color)

    # Arrows
    arrows = [
        (140, 100, 170, 100),   # CREATED -> DELEGATED
        (290, 100, 320, 100),   # DELEGATED -> IN_PROGRESS
        (440, 100, 470, 100),   # IN_PROGRESS -> REVIEW
        (530, 120, 530, 210),   # REVIEW -> COMPLETED
        (470, 120, 290, 210),   # REVIEW -> FAILED (reject)
        (230, 210, 380, 80),    # FAILED -> IN_PROGRESS (rework)
    ]

    for i, (x1, y1, x2, y2) in enumerate(arrows):
        mid = f"am_{i}"
        svg += (
            f'  <defs><marker id="{mid}" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">'
            f'<polygon points="0 0, 8 3, 0 6" fill="#555"/></marker></defs>\n'
            f'  <line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#555" stroke-width="1.5" marker-end="url(#{mid})"/>\n'
        )

    # Labels
    svg += _svg_text(155, 90, "L0", size=9, fill="#888")
    svg += _svg_text(305, 90, "L1", size=9, fill="#888")
    svg += _svg_text(455, 90, "L2", size=9, fill="#888")
    svg += _svg_text(545, 165, "approved", size=9, fill="#888")
    svg += _svg_text(370, 175, "rejected", size=9, fill="#888")

    svg += _svg_footer()
    return svg


# =====================================================================
# ENVIRONMENT MAP
# =====================================================================

def generate_environment_map_svg() -> str:
    """Generate an environment map diagram."""
    total_w = 700
    total_h = 300

    svg = _svg_header(total_w, total_h)
    svg += _svg_rect(0, 0, total_w, total_h, "#fafafa", stroke="none")
    svg += _svg_text(total_w // 2, 30, "Environment Map", size=20, weight="bold")
    svg += _svg_text(total_w // 2, 52, "Environment ≠ Authority", size=13, fill="#c62828", weight="bold")

    envs = [
        ("DEVELOPMENT", 100, "#e3f2fd", "#1565c0"),
        ("TEST", 250, "#e8f5e9", "#2e7d32"),
        ("STAGING", 400, "#fff3e0", "#e65100"),
        ("PRODUCTION", 550, "#ffebee", "#b71c1c"),
    ]

    for name, x, fill, text_color in envs:
        svg += _svg_rect(x - 65, 80, 130, 80, fill, stroke=text_color)
        svg += _svg_text(x, 115, name, size=12, weight="bold", fill=text_color)
        svg += _svg_text(x, 145, "↓", size=18, fill=text_color)

    # Flow arrows
    for i in range(3):
        x1 = envs[i][1] + 65
        x2 = envs[i + 1][1] - 65
        svg += f'  <line x1="{x1}" y1="120" x2="{x2}" y2="120" stroke="#999" stroke-width="1.5" stroke-dasharray="5,5"/>\n'

    # Warning box
    svg += _svg_rect(100, 200, 500, 60, "#fff8e1", stroke="#f9a825", rx=5)
    svg += _svg_text(350, 225, "Being in an environment does NOT grant authority.", size=13, weight="bold", fill="#e65100")
    svg += _svg_text(350, 245, "Authority comes from your role (L0/L1/L2), not from where you are.", size=11, fill="#666")

    svg += _svg_footer()
    return svg


# =====================================================================
# REPOSITORY MAP
# =====================================================================

def generate_repository_map_svg(snap) -> str:
    """Generate a repository map diagram."""
    total_w = 700
    total_h = 350

    svg = _svg_header(total_w, total_h)
    svg += _svg_rect(0, 0, total_w, total_h, "#fafafa", stroke="none")
    svg += _svg_text(total_w // 2, 30, "Repository Map", size=20, weight="bold")

    # Canonical box
    svg += _svg_rect(50, 60, 280, 120, "#e3f2fd", stroke="#1565c0")
    svg += _svg_text(190, 85, "CANONICAL (Git)", size=14, weight="bold", fill="#1565c0")
    items = ["actors/", "missions/records/", "decisions/records/", "evidence/records/", "state/"]
    for j, item in enumerate(items):
        svg += _svg_text(190, 105 + j * 16, item, size=11, fill="#333")

    # Operational box
    svg += _svg_rect(370, 60, 280, 120, "#fff3e0", stroke="#e65100")
    svg += _svg_text(510, 85, "OPERATIONAL (Runtime)", size=14, weight="bold", fill="#e65100")
    items2 = ["Private Memory", "Gateway Audit Logs", "Sync Engine Cache", "Actor Runtime State"]
    for j, item in enumerate(items2):
        svg += _svg_text(510, 105 + j * 16, item, size=11, fill="#333")

    # RF box
    svg += _svg_rect(200, 210, 300, 50, "#f3e5f5", stroke="#6a1b9a")
    svg += _svg_text(350, 235, "Repository Fabric (RF)", size=14, weight="bold", fill="#6a1b9a")
    svg += _svg_text(350, 250, "Governs all canonical writes", size=10, fill="#666")

    # Arrow from RF to Canonical
    svg += f'  <line x1="280" y1="210" x2="190" y2="180" stroke="#6a1b9a" stroke-width="1.5" stroke-dasharray="5,5"/>\n'

    # Source of truth
    svg += _svg_rect(100, 280, 500, 40, "#e8f5e9", stroke="#2e7d32", rx=5)
    svg += _svg_text(350, 305, "The Git repository is the SINGLE SOURCE OF TRUTH", size=13, weight="bold", fill="#1b5e20")

    svg += _svg_footer()
    return svg


# =====================================================================
# WORKSPACE MAP
# =====================================================================

def generate_workspace_map_svg(snap) -> str:
    """Generate a workspace map showing all department workspaces."""
    departments = sorted(snap.departments.keys())
    n = len(departments)
    col_w = 150
    total_w = max(n * (col_w + 15) + 60, 800)
    total_h = 280

    svg = _svg_header(total_w, total_h)
    svg += _svg_rect(0, 0, total_w, total_h, "#fafafa", stroke="none")
    svg += _svg_text(total_w // 2, 30, "Workspace Map", size=20, weight="bold")

    colors = ["#e3f2fd", "#e8f5e9", "#fff3e0", "#f3e5f5", "#ffebee", "#e0f7fa", "#fbe9e7", "#f1f8e9"]

    for i, dept in enumerate(departments):
        x = 30 + i * (col_w + 15)
        fill = colors[i % len(colors)]
        data = snap.departments[dept]
        director = data.get("director")
        worker = data.get("worker")

        svg += _svg_rect(x, 50, col_w, 190, fill, stroke="#999")
        svg += _svg_text(x + col_w // 2, 72, dept[:16], size=11, weight="bold")

        if director:
            svg += _svg_rect(x + 10, 85, col_w - 20, 35, "white", stroke="#34a853", rx=4)
            svg += _svg_text(x + col_w // 2, 102, director["name"], size=10, weight="bold", fill="#2e7d32")
            svg += _svg_text(x + col_w // 2, 115, "L1 Director", size=8, fill="#666")

        if worker:
            svg += _svg_rect(x + 10, 130, col_w - 20, 35, "white", stroke="#fbbc04", rx=4)
            svg += _svg_text(x + col_w // 2, 147, worker["name"], size=10, weight="bold", fill="#665500")
            svg += _svg_text(x + col_w // 2, 160, "L2 Specialist", size=8, fill="#666")

        svg += _svg_text(x + col_w // 2, 190, "In → Work → Out", size=8, fill="#888")
        svg += _svg_text(x + col_w // 2, 205, "Evidence ↓", size=8, fill="#888")
        svg += _svg_text(x + col_w // 2, 225, "📁 Records", size=9, fill="#555")

    svg += _svg_footer()
    return svg
