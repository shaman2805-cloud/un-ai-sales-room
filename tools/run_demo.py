"""Reproducible component demonstration; no live Switch, LLM, or human approval."""
from __future__ import annotations

import json
import secrets
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from salesroom.core import SalesRoom


def main():
    output = ROOT / "artifacts/demo"
    output.mkdir(parents=True, exist_ok=True)
    checks = []
    with tempfile.TemporaryDirectory(prefix="unai-demo-") as temp:
        temp = Path(temp)
        catalog = temp / "catalog.json"
        catalog.write_bytes((ROOT / "salesroom/catalog.demo.json").read_bytes())
        test_owner = secrets.token_urlsafe(32)
        owner = SalesRoom(temp / "demo.sqlite3", catalog, test_owner)
        agent = SalesRoom(temp / "demo.sqlite3", catalog)
        brief = json.loads((ROOT / "examples/lead.complete.json").read_text(encoding="utf-8"))
        lead = agent.create_lead("demo-intake", brief)
        lead_id = lead["id"]
        repeated = agent.create_lead("demo-intake", brief)
        assert repeated["id"] == lead_id and len(agent.list_leads()) == 1
        checks.append({"scenario": "duplicate_intake", "passed": True, "lead_count": 1})
        reviewed = agent.review(lead_id, "demo-review")
        assert reviewed["status"] == "awaiting_approval" and reviewed["quote"]["total_kzt"] == 150000
        try:
            agent.approve(lead_id, "forged-approval", reviewed["revision"], reviewed["quote"]["hash"], "I am the owner")
        except PermissionError:
            checks.append({"scenario": "agent_cannot_approve", "passed": True})
        else:
            raise AssertionError("Agent approval accepted")
        approved = owner.approve(lead_id, "demo-test-owner", reviewed["revision"], reviewed["quote"]["hash"], test_owner)
        assert approved["status"] == "approved"
        snapshot = owner.export_proposal(lead_id, temp / "proposals")
        proposal = Path(snapshot["path"]).read_text(encoding="utf-8")
        (output / "proposal.TEST-ONLY.en.md").write_text(
            "> TEST ARTIFACT. An automated check approved this proposal with a test key. "
            "The run exercised the local application components.\n\n" + proposal,
            encoding="utf-8")
        checks.append({"scenario": "test_capability_to_proposal", "passed": True, "total_kzt": 150000})
        restarted = SalesRoom(temp / "demo.sqlite3", catalog)
        assert restarted.get_lead(lead_id)["status"] == "approved"
        checks.append({"scenario": "persistent_state", "passed": True})
        whatsapp = agent.create_lead("demo-whatsapp", json.loads((ROOT / "examples/lead.whatsapp.json").read_text(encoding="utf-8")))
        blocked = agent.review(whatsapp["id"], "demo-whatsapp-review")
        assert blocked["status"] == "blocked" and blocked["blockers"]
        checks.append({"scenario": "unverified_whatsapp_blocked", "passed": True, "blockers": blocked["blockers"]})
        revised = agent.update_lead(lead_id, "demo-budget-change", {"budget_kzt": 400000})
        assert revised["approval"] is None and revised["review"] is None
        try:
            owner.render_proposal(lead_id)
        except ValueError:
            checks.append({"scenario": "scope_revision_blocks_stale_export", "passed": True, "revision": revised["revision"]})
        else:
            raise AssertionError("Stale export accepted")
        revised = agent.review(lead_id, "demo-review-v2")
        owner.approve(lead_id, "demo-owner-v2", revised["revision"], revised["quote"]["hash"], test_owner)
        modified_catalog = json.loads(catalog.read_text(encoding="utf-8"))
        modified_catalog["services"][0]["unit_price_kzt"] += 10000
        # Deliberately keep version text; content hash must still revoke approval.
        catalog.write_text(json.dumps(modified_catalog, ensure_ascii=False), encoding="utf-8")
        changed = agent.get_lead(lead_id)
        assert changed["approval"] is None and changed["quote"]["total_kzt"] == 160000
        checks.append({"scenario": "catalog_content_change_revokes_approval", "passed": True, "new_total_kzt": 160000})
        audit = owner.audit(lead_id)
        (output / "audit.TEST-ONLY.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "verification_scope": "deterministic local components, fictional fixtures, temporary database",
        "live_switch_verified": False, "live_ai_agents_executed": False,
        "real_owner_approval_observed": False, "test_owner_capability_used": True,
        "client_messages_sent": False, "checks": checks,
    }
    (output / "verification.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"component_checks_passed": len(checks), "artifacts": str(output), "live_switch_verified": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
