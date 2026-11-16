"""Synthetic data generator for the Project Cost & Budget Intelligence practice project.
All names and numbers are made up. Re-running produces identical files (fixed seed)."""
import random
import csv
from datetime import date
from pathlib import Path

random.seed(42)
OUT = Path(__file__).parent

cost_centers = [
    ("CC10", "Manufacturing"), ("CC20", "Logistics"), ("CC30", "IT Infrastructure"),
    ("CC40", "Facilities"), ("CC50", "Research and Development"),
]

vendors = [
    ("V001", "Apex Industrial Supply"), ("V002", "BlueRiver Engineering"),
    ("V003", "Cobalt Systems"), ("V004", "Delta Contractors"),
    ("V005", "Evergreen Facilities"), ("V006", "Falcon Logistics"),
    ("V007", "Granite Equipment"), ("V008", "Horizon Software"),
    ("V009", "Ionic Electricals"), ("V010", "Juniper Consulting"),
]

project_names = [
    "Plant Line Upgrade", "Warehouse Expansion", "Data Center Refresh", "Office Renovation",
    "Lab Equipment Install", "Packaging Automation", "Fleet Tracking System", "Solar Rooftop",
    "ERP Integration", "Cold Storage Build", "Network Modernization", "Safety Systems Retrofit",
    "Assembly Robotics", "Cafeteria Remodel", "Test Bench Setup", "Dock Automation",
    "Backup Power Upgrade", "Quality Lab Expansion", "Visitor Center Build", "Pilot Plant Setup",
]

# months: fiscal year April 2025 - March 2026
months = [date(2025, m, 1) for m in range(4, 13)] + [date(2026, m, 1) for m in range(1, 4)]

projects = []
for i, name in enumerate(project_names):
    pid = f"P{100 + i * 10}"
    cc = cost_centers[i % len(cost_centers)][0]
    ptype = "Capex" if i % 3 != 2 else "Opex"
    start = months[random.randint(0, 3)]
    projects.append({"PROJECT_ID": pid, "PROJECT_NAME": name, "COST_CENTER_ID": cc,
                     "PROJECT_TYPE": ptype, "START_DATE": start.isoformat()})

def write(name, header, rows):
    with open(OUT / name, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)

write("dim_cost_center.csv", ["COST_CENTER_ID", "COST_CENTER_NAME"], cost_centers)
write("dim_vendor.csv", ["VENDOR_ID", "VENDOR_NAME"], vendors)
write("dim_project.csv", list(projects[0].keys()), [list(p.values()) for p in projects])

# monthly actual vs budget
cost_rows = []
capex_rows = []
for p in projects:
    base = random.randint(40, 160) * 1000          # monthly budget level
    bias = random.uniform(-0.08, 0.18)             # some projects drift over budget
    total_budget = total_actual = 0
    for m in months:
        if m < date.fromisoformat(p["START_DATE"]):
            continue
        budget = round(base * random.uniform(0.9, 1.1), 2)
        actual = round(budget * (1 + bias + random.uniform(-0.12, 0.12)), 2)
        total_budget += budget
        total_actual += actual
        cost_rows.append([p["PROJECT_ID"], m.isoformat(), actual, budget, "USD"])
    if p["PROJECT_TYPE"] == "Capex":
        approved = round(total_budget * random.uniform(1.1, 1.4), 2)
        committed = round(max(approved - total_actual, 0) * random.uniform(0.2, 0.7), 2)
        progress = min(100, round(total_actual / approved * 100 + random.uniform(-8, 8)))
        status = ("Completed" if progress >= 98 else
                  "On Track" if total_actual <= total_budget * 1.05 else "At Risk")
        capex_rows.append([p["PROJECT_ID"], approved, round(total_actual, 2), committed,
                           max(progress, 0), status, "USD"])

write("fact_cost.csv", ["PROJECT_ID", "PERIOD", "ACTUAL", "BUDGET", "CURRENCY"], cost_rows)
write("fact_capex_status.csv",
      ["PROJECT_ID", "APPROVED_BUDGET", "SPENT_TO_DATE", "COMMITTED", "PROGRESS_PCT", "STATUS", "CURRENCY"],
      capex_rows)

# purchase requisitions / purchase orders
statuses = ["PR Created", "PO Issued", "Goods Received", "Invoiced"]
weights = [0.15, 0.30, 0.25, 0.30]
pr_rows = []
for n in range(1, 121):
    p = random.choice(projects)
    vendor = random.choice(vendors)[0]
    created = random.choice(months) .replace(day=random.randint(1, 28))
    pr_amount = random.randint(5, 150) * 1000
    status = random.choices(statuses, weights)[0]
    po_number = "" if status == "PR Created" else f"45{n:08d}"
    po_amount = "" if status == "PR Created" else round(pr_amount * random.uniform(0.92, 1.08), 2)
    pr_rows.append([f"10{n:08d}", po_number, p["PROJECT_ID"], vendor, created.isoformat(),
                    pr_amount, po_amount, status, "USD"])
write("fact_pr_po.csv",
      ["PR_NUMBER", "PO_NUMBER", "PROJECT_ID", "VENDOR_ID", "CREATED_DATE", "PR_AMOUNT", "PO_AMOUNT", "STATUS", "CURRENCY"],
      pr_rows)
print("done")
