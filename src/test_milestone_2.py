from scope_agent import extract_scope_and_deliverables
from risk_delivery_agent import detect_risks_and_forecast_delivery
from blocker_action_agent import identify_blockers_and_action_items


print("\n" + "=" * 70)
print("MILESTONE 2 - MULTI-AGENT VALIDATION")
print("=" * 70)


print("\n\n===== 1. SCOPE AND DELIVERABLE EXTRACTION =====\n")
scope_result = extract_scope_and_deliverables()
print(scope_result)


print("\n\n===== 2. RISK DETECTION AND DELIVERY FORECAST =====\n")
risk_result = detect_risks_and_forecast_delivery()
print(risk_result)


print("\n\n===== 3. BLOCKER AND ACTION ITEM IDENTIFICATION =====\n")
blocker_result = identify_blockers_and_action_items()
print(blocker_result)


print("\n\n" + "=" * 70)
print("MILESTONE 2 VALIDATION COMPLETED")
print("=" * 70)