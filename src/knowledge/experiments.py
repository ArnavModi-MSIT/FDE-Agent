"""Prepare local answer candidates while protecting the recorded scoring rows.

No network calls or score estimates: a candidate is unscored until the user
uploads it and records the result. Plans contain complete, policy-backed answers.
"""
import csv
import hashlib
import io
import json
import re
from pathlib import Path

FIELDS = ["qid", "answer", "governing_source"]
UNRESOLVED_QIDS = frozenset({"K-03", "K-07"})
EXPECTED_QIDS = {f"K-{n:02d}" for n in range(1, 13)}


def read_submission(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != FIELDS:
            raise ValueError(f"{path}: expected columns {FIELDS}")
        rows = list(reader)
    qids = [row["qid"] for row in rows]
    if len(qids) != len(EXPECTED_QIDS) or set(qids) != EXPECTED_QIDS:
        raise ValueError(f"{path}: expected each of K-01 through K-12 exactly once")
    if any(None in row or any(not value or not value.strip() for value in row.values()) for row in rows):
        raise ValueError(f"{path}: blank or malformed submission cell")
    return rows


def prepare_candidates(
    baseline_path: Path,
    reference_path: Path,
    plan_path: Path,
    output_dir: Path,
    preserve: tuple[str, ...] = (),
) -> dict:
    """Validate the whole batch before creating a new output directory.

    A later improving submission can be used as baseline with --preserve K-XX
    for a row confirmed to score. The ten confirmed scoring answers and all
    sources must always match the protected reference. Existing files are
    never overwritten.
    """
    baseline = read_submission(baseline_path)
    reference = {row["qid"]: row for row in read_submission(reference_path)}
    if set(preserve) - UNRESOLVED_QIDS:
        raise ValueError("Only unresolved K-03 and K-07 can be preserved explicitly")
    for row in baseline:
        saved = reference[row["qid"]]
        if row["governing_source"] != saved["governing_source"]:
            raise ValueError(f"{row['qid']}: baseline changes a protected source")
        if row["qid"] not in UNRESOLVED_QIDS and row["answer"] != saved["answer"]:
            raise ValueError(f"{row['qid']}: baseline changes a proven scoring answer")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    variants = plan.get("variants", [])
    if not 1 <= len(variants) <= 5:
        raise ValueError("Prepare between one and five candidates per batch")
    rendered = []
    names, payloads = set(), set()
    for variant in variants:
        name = variant["name"]
        if not re.fullmatch(r"[A-Za-z0-9_-]+", name) or name.casefold() in names:
            raise ValueError(f"Invalid or duplicate candidate name: {name!r}")
        names.add(name.casefold())  # Windows filenames are case-insensitive.
        replacements = variant["answers"]
        if not replacements or set(replacements) - UNRESOLVED_QIDS:
            raise ValueError(f"{name}: only unresolved answers may be changed")
        if any(not isinstance(value, str) or not value.strip() for value in replacements.values()):
            raise ValueError(f"{name}: each replacement must be a nonblank answer")
        rows, changes = [], {}
        for original in baseline:
            row = dict(original)
            qid = row["qid"]
            if qid in replacements and qid not in preserve:
                row["answer"] = replacements[qid]
            if row != original:
                changes[qid] = {"before": original["answer"], "after": row["answer"]}
            rows.append(row)
        if not changes:
            raise ValueError(f"{name}: identical to baseline; would waste an attempt")
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
        payload = stream.getvalue().encode("utf-8")
        if payload in payloads:
            raise ValueError(f"{name}: duplicates another candidate in this batch")
        payloads.add(payload)
        rendered.append((f"knowledge_submission_{name}.csv", payload, changes, variant.get("hypothesis", "")))

    manifest = {
        "status": "prepared_not_submitted",
        "baseline": str(baseline_path.resolve()),
        "baseline_sha256": hashlib.sha256(baseline_path.read_bytes()).hexdigest(),
        "plan_sha256": hashlib.sha256(plan_path.read_bytes()).hexdigest(),
        "preserved_qids": sorted(preserve),
        "candidates": [
            {"file": name, "sha256": hashlib.sha256(payload).hexdigest(),
             "hypothesis": hypothesis, "changes": changes, "score": None}
            for name, payload, changes, hypothesis in rendered
        ],
    }
    output_dir.mkdir(parents=True, exist_ok=False)
    for name, payload, _, _ in rendered:
        (output_dir / name).write_bytes(payload)
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
