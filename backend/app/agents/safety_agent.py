import re
from datetime import datetime
from app.graph.state import PharmacyState
from app.db.database import SessionLocal
from app.db.models import Medicine, Prescription
from app.rules.safety_rules import MAX_QTY_PER_ORDER

# 1A️⃣ OTC ALLOWLIST LOGIC
# Policy: If prescription_required == false → prescription is NOT needed
# This is explicit, not implied

# 1B️⃣ MAX DOSAGE ENFORCEMENT
# Hard-coded safe daily limits (no schema change needed yet)
SAFE_DOSAGE_LIMITS = {
    "paracetamol": 4000,  # mg/day
    "ibuprofen": 3200,    # mg/day
    "aspirin": 4000,      # mg/day
    "amoxicillin": 3000,  # mg/day
    "ciprofloxacin": 1500,  # mg/day
}


def _extract_dosage_value(dosage_str: str) -> int:
    """Extract numeric dosage value from string (e.g., '500mg' -> 500)"""
    if not dosage_str:
        return 0
    match = re.search(r'(\d+)', dosage_str)
    return int(match.group(1)) if match else 0


def _get_safe_limit(medicine_name: str) -> int:
    """Get safe daily dosage limit for medicine (mg/day)"""
    name_lower = medicine_name.lower()
    for key, limit in SAFE_DOSAGE_LIMITS.items():
        if key in name_lower:
            return limit
    return float('inf')  # Unknown medicine: no dosage limit (handled elsewhere)


def safety_agent(state: PharmacyState) -> PharmacyState:
    # 🔒 HARD ASSERTION — non-negotiable
    assert isinstance(state, dict), f"STATE CORRUPTED: {type(state)}"

    db = SessionLocal()

    violations = []
    clarification_questions = []
    reasoning_steps = []
    error_type = None  # Will be VALIDATION, SAFETY, or SYSTEM
    decision = "approved"  # Can be: approved, clarification_required, blocked

    customer_id = state["customer"]["id"]
    medicines = state.get("extraction", {}).get("medicines", [])

    if not medicines:
        error_type = "VALIDATION"
        violations.append("No medicines requested")
        reasoning_steps.append("No medicines found in extraction")
        decision = "blocked"
    else:
        # --- Normalization helper ---
        def normalize(text):
            if not text:
                return ""
            t = text.lower().strip()
            t = re.sub(r"\b\d+\s*mg\b", "", t)
            t = re.sub(r"\b\d+\s*mcg\b", "", t)
            t = re.sub(r"\b\d+\s*ml\b", "", t)
            t = re.sub(r"\s+", " ", t)
            return t.strip()

        all_meds = db.query(Medicine).all()
        for item in medicines:
            name = item["name"]
            quantity = item["quantity"]
            dosage_str = item.get("dosage", "")
            otc_hint = item.get("otc_hint", None)

            norm_name = normalize(name)
            medicine = None
            for m in all_meds:
                if norm_name == normalize(m.name):
                    medicine = m
                    break
            if not medicine:
                # Try partial match: input is substring of DB name or vice versa
                for m in all_meds:
                    db_norm = normalize(m.name)
                    if norm_name in db_norm or db_norm in norm_name:
                        medicine = m
                        break
            if not medicine:
                error_type = "VALIDATION"
                violations.append(f"Medicine not found: {name}")
                reasoning_steps.append(
                    f"❌ Medicine '{name}' not found in inventory (full normalization failed)"
                )
                decision = "blocked"
                continue

            if not medicine:
                error_type = "VALIDATION"
                violations.append(f"Medicine not found: {name}")
                reasoning_steps.append(
                    f"❌ Medicine '{name}' not found in inventory"
                )
                decision = "blocked"
                continue

            reasoning_steps.append(
                f"✅ Found medicine '{medicine.name}' (OTC={not medicine.prescription_required})"
            )

            # 2️⃣ Quantity rule
            if quantity > MAX_QTY_PER_ORDER:
                error_type = "SAFETY"
                violations.append(
                    f"Quantity {quantity} exceeds allowed limit ({MAX_QTY_PER_ORDER})"
                )
                reasoning_steps.append(
                    f"⚠️ Quantity {quantity} exceeds max limit of {MAX_QTY_PER_ORDER}"
                )
                decision = "blocked"

            # 3️⃣ Stock check (always required)
            if medicine.stock_quantity < quantity:
                error_type = "VALIDATION"
                violations.append(
                    f"Insufficient stock for {medicine.name} "
                    f"(available: {medicine.stock_quantity}, requested: {quantity})"
                )
                reasoning_steps.append(
                    f"❌ Stock insufficient: {medicine.stock_quantity} available, {quantity} requested"
                )
                decision = "blocked"
            else:
                reasoning_steps.append(
                    f"✅ Stock available: {medicine.stock_quantity} units"
                )

            # 1B️⃣ MAX DOSAGE ENFORCEMENT
            # Parse dosage and validate against safe limits
            dosage_value = _extract_dosage_value(dosage_str)
            safe_limit = _get_safe_limit(medicine.name)
            
            if dosage_value > 0 and safe_limit != float('inf'):
                if dosage_value > safe_limit:
                    error_type = "SAFETY"
                    violations.append(
                        f"Dosage {dosage_value}mg exceeds safe daily limit ({safe_limit}mg)"
                    )
                    reasoning_steps.append(
                        f"⚠️ Dosage {dosage_value}mg exceeds safe daily limit of {safe_limit}mg"
                    )
                    decision = "blocked"
                else:
                    reasoning_steps.append(
                        f"✅ Dosage {dosage_value}mg within safe limit ({safe_limit}mg/day)"
                    )
            elif dosage_value == 0:
                # 1C️⃣ CLARIFICATION INSTEAD OF HARD BLOCK
                # Missing dosage info: ask instead of block
                clarification_questions.append(
                    f"How many mg per dose of {medicine.name}? (e.g., 500mg)"
                )
                reasoning_steps.append(
                    f"❓ Dosage not specified for {medicine.name}"
                )
                if decision == "approved":
                    decision = "clarification_required"

            # 4️⃣ Prescription check — ONLY if required
            # 1A️⃣ OTC ALLOWLIST LOGIC: If prescription_required == false, skip prescription check
            if medicine.prescription_required:
                prescription = (
                    db.query(Prescription)
                    .filter(
                        Prescription.customer_id == customer_id,
                        Prescription.medicine_id == medicine.id,
                        Prescription.valid_until >= datetime.utcnow()
                    )
                    .first()
                )

                if not prescription:
                    error_type = "SAFETY"
                    violations.append(
                        f"Valid prescription required for {medicine.name}"
                    )
                    reasoning_steps.append(
                        f"❌ No valid prescription found for Rx medicine '{medicine.name}'"
                    )
                    decision = "blocked"
                else:
                    reasoning_steps.append(
                        f"✅ Valid prescription found for Rx medicine '{medicine.name}'"
                    )
            else:
                # ✅ OTC medicine — EXPLICITLY allowed without prescription (OTC allowlist)
                reasoning_steps.append(
                    f"✅ '{medicine.name}' is OTC — no prescription required (OTC allowlist)"
                )

    # Finalize decision
    # 1C️⃣ CLARIFICATION INSTEAD OF HARD BLOCK
    if len(violations) > 0:
        approved = False
        decision = "blocked"
    elif len(clarification_questions) > 0:
        approved = False
        decision = "clarification_required"
    else:
        approved = True
        decision = "approved"
    
    # Set error_type
    if approved and not error_type:
        error_type = None  # Success path
    elif not approved and not error_type:
        error_type = "SAFETY" if decision == "blocked" else None

    state["safety"] = {
        "approved": approved,
        "decision": decision,  # approved, clarification_required, or blocked
        "reason": "All safety checks passed" if approved else ("Clarification needed" if decision == "clarification_required" else "Request blocked by safety rules"),
        "violations": violations,
        "clarification_questions": clarification_questions,
        "error_type": error_type  # VALIDATION, SAFETY, SYSTEM, or None if approved
    }

    state["decision_trace"].append({
        "agent": "safety_agent",
        "input": medicines,
        "reasoning": reasoning_steps,
        "decision": decision,
        "output": state["safety"]
    })

    db.close()
    return state
