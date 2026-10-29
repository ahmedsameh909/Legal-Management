import random
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from datetime import datetime, timedelta

# Master Data Lists
CLIENT_COMPANIES = [
    "Northstar Trading Group", "Cedar Medical Supplies", "Atlas Construction Ltd.",
    "Blue Harbor Logistics", "Pioneer Foods Company", "Summit Technology Group",
    "Apex Global Holding", "Nile Valley Real Estate", "Sphinx Pharma Ltd.",
    "Delta Telecom Egypt", "Horizon Energy Corp", "Red Sea Maritime Services",
    "Cairo Capital Investments", "Pyramids Engineering Works", "Green Oasis Agriculture"
]

OPPONENT_COMPANIES = [
    "Meridian Supply Partners", "Crownline Importers", "Eastgate Property Holdings",
    "Silver Oak Distribution", "Redstone Industrial Services", "Westfield Retail Group", "Global Logistics Express", "Crestview Holdings", "Vanguard Metal Works",
    "Taurus Heavy Industries", "Bayside Chemical Co.", "Starlight Electronics"
]

CASE_SUBJECTS = [
    "Commercial Supply Agreement Dispute", "Construction Services Payment Claim",
    "Lease and Property Damages Matter", "Delayed Shipment Compensation Claim",
    "Product Warranty Dispute", "Software Services Contract Dispute",
    "Confidentiality Agreement Breach", "Outstanding Invoice Recovery",
    "Intellectual Property Infringement", "Unfair Competition Claim",
    "Shareholder Dividend Dispute", "Labor Contract Termination Dispute"
]

JUDGES = [
    "Judge Morgan", "Judge Ibrahim", "Judge Williams", "Judge Hassan",
    "Judge Patel", "Judge Carter", "Judge El-Sayed", "Judge Abdelrahman",
    "Judge Mahmoud", "Judge Al-Mansour"
]

COURT_DEGREES = ["primary", "appeal", "cassation"]
CASE_STATES = ["draft", "in_progress", "pending", "won", "settled", "lost"]
CONTRACT_TYPES = ["retainer", "consultation", "settlement", "nda", "other"]
CONTRACT_STATES = ["draft", "active", "expired", "terminated"]
HEARING_STATES = ["scheduled", "attended", "postponed", "cancelled"]


def create_field(parent, name, value=None, ref=None):
    attributes = {"name": name}
    if ref is not None:
        attributes["ref"] = ref
    field = ET.SubElement(parent, "field", attributes)
    if value is not None:
        field.text = str(value)
    return field


def create_record(parent, record_id, model):
    return ET.SubElement(parent, "record", id=record_id, model=model)


def generate_xml(seed=2026):
    rng = random.Random(seed)
    root = ET.Element("odoo", noupdate="1")

    # 1. Generate 50 Clients (res.partner)
    clients = []
    for i in range(1, 51):
        client_id = f"demo_legal_client_{i:03d}"
        company_name = f"{CLIENT_COMPANIES[(i-1) % len(CLIENT_COMPANIES)]} #{i}"
        
        client = create_record(root, client_id, "res.partner")
        create_field(client, "name", company_name)
        create_field(client, "email", f"legal@{company_name.lower().replace(' ', '').replace('#', '')}.example")
        create_field(client, "phone", f"+20100{i:06d}")
        create_field(client, "is_company", True)
        create_field(client, "is_legal_client", True)
        create_field(client, "national_id", f"EGY-TAX-{7000 + i:05d}")
        clients.append(client_id)

    # 2. Generate 50 Opponents (res.partner)
    opponents = []
    for i in range(1, 51):
        opponent_id = f"demo_legal_opponent_{i:03d}"
        company_name = f"{OPPONENT_COMPANIES[(i-1) % len(OPPONENT_COMPANIES)]} #{i}"

        opponent = create_record(root, opponent_id, "res.partner")
        create_field(opponent, "name", company_name)
        create_field(opponent, "email", f"disputes@{company_name.lower().replace(' ', '').replace('#', '')}.example")
        create_field(opponent, "phone", f"+20120{i:06d}")
        create_field(opponent, "is_company", True)
        create_field(opponent, "is_opponent", True)
        opponents.append(opponent_id)

    # 3. Generate 100 Legal Cases (legal.case)
    cases = []
    for i in range(1, 101):
        case_id = f"demo_legal_case_{i:03d}"
        client_id = rng.choice(clients)
        opponent_id = rng.choice(opponents)
        case_title = f"{rng.choice(CASE_SUBJECTS)} ({i:03d})"

        case = create_record(root, case_id, "legal.case")
        create_field(case, "title", case_title)
        create_field(case, "client_id", ref=client_id)
        create_field(case, "opponent_id", ref=opponent_id)
        create_field(case, "lawyer_id", ref="base.user_admin")
        create_field(case, "court_name", rng.choice(COURT_DEGREES))
        create_field(case, "case_number", f"CIV-2026-{1000 + i:04d}")
        create_field(case, "claim_amount", rng.randrange(25000, 500000, 2500))
        create_field(case, "state", rng.choice(CASE_STATES))

        cases.append((case_id, client_id))

    # 4. Generate 1 to 4 Court Hearings per case (legal.hearing)
    hearing_counter = 1
    base_date = datetime(2026, 1, 15)

    for case_id, _ in cases:
        # Generate between 1 and 4 hearings per case
        num_hearings = rng.randint(1, 4)
        for h_idx in range(num_hearings):
            hearing_id = f"demo_legal_hearing_{hearing_counter:04d}"
            hearing_date = base_date + timedelta(days=rng.randint(0, 300), hours=rng.randint(8, 14))

            hearing = create_record(root, hearing_id, "legal.hearing")
            create_field(hearing, "case_id", ref=case_id)
            create_field(hearing, "lawyer_id", ref="base.user_admin")
            create_field(hearing, "date", hearing_date.strftime("%Y-%m-%d %H:%M:%S"))
            create_field(hearing, "court_room", f"Hall {rng.randint(1, 12)} / Room {rng.randint(101, 404)}")
            create_field(hearing, "judge_name", rng.choice(JUDGES))
            create_field(hearing, "summary", f"Session #{h_idx + 1}: Examination of expert testimony, witness statements, and evidentiary submissions.")
            create_field(hearing, "state", rng.choice(HEARING_STATES))

            hearing_counter += 1

    # 5. Generate 120 Legal Contracts (legal.contract)
    for i in range(1, 121):
        contract_id = f"demo_legal_contract_{i:03d}"
        case_id, client_id = rng.choice(cases)

        start_dt = datetime(2026, 1, 1) + timedelta(days=rng.randint(0, 180))
        end_dt = start_dt + timedelta(days=365)

        contract = create_record(root, contract_id, "legal.contract")
        create_field(contract, "title", f"Legal Representation Agreement #{i:03d}")
        create_field(contract, "partner_id", ref=client_id)
        create_field(contract, "case_id", ref=case_id)
        create_field(contract, "responsible_user_id", ref="base.user_admin")
        create_field(contract, "contract_type", rng.choice(CONTRACT_TYPES))
        create_field(contract, "start_date", start_dt.strftime("%Y-%m-%d"))
        create_field(contract, "end_date", end_dt.strftime("%Y-%m-%d"))
        create_field(contract, "contract_amount", rng.randrange(10000, 150000, 5000))
        create_field(contract, "state", rng.choice(CONTRACT_STATES))
        create_field(
            contract,
            "terms_and_conditions",
            f"<p>Standard legal services agreement #{i:03d}. Governed under local jurisdiction laws. Confidentiality and professional ethics enforced.</p>",
        )

    # 6. Save XML File
    output_path = Path(__file__).with_name("legal_management_demo.xml")
    rough_xml = ET.tostring(root, encoding="utf-8")
    pretty_xml = minidom.parseString(rough_xml).toprettyxml(indent="    ")
    clean_xml = "\n".join([line for line in pretty_xml.split("\n") if line.strip()])

    output_path.write_text(clean_xml, encoding="utf-8")
    print(
        f"Successfully generated {output_path} with:\n"
        f" - 50 Legal Clients\n"
        f" - 50 Opponents\n"
        f" - 100 Legal Cases\n"
        f" - {hearing_counter - 1} Court Hearings\n"
        f" - 120 Legal Contracts"
    )


if __name__ == "__main__":
    generate_xml()