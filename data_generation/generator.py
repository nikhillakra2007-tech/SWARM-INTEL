"""
Large synthetic lending ecosystem generator - 50k scale, reproducible, 85/10/5 split, 10 scenario types, temporal, emerging networks.
"""
import uuid, hashlib, random
from datetime import datetime, timedelta, timezone
from collections import defaultdict

from .config import SEED, TARGETS, POPULATION, START_DATE, END_DATE
from .random_utils import RNG

rng = RNG(SEED)
START = datetime.fromisoformat(START_DATE).replace(tzinfo=timezone.utc)
END = datetime.fromisoformat(END_DATE).replace(tzinfo=timezone.utc)

def h(s): return hashlib.sha256(s.encode()).hexdigest()
def uid(name): return uuid.uuid5(uuid.NAMESPACE_DNS, name)

# Helpers for enums
OCCUPATIONS = ["ENGINEER","TEACHER","BUSINESS","DOCTOR","GOVERNMENT","IT","SALES","LAWYER","CONTRACTOR","AGENT","DRIVER","CLERK","OTHER"]
BANKS = ["SBI","HDFC","ICICI","AXIS","KOTAK","PNB","BOB","INDUSIND"]
CITIES = [("Mumbai","Maharashtra","400001",19.07,72.87),("Delhi","Delhi","110001",28.6,77.2),("Bengaluru","Karnataka","560001",12.97,77.59),("Hyderabad","Telangana","500001",17.38,78.48),("Kolkata","West Bengal","700001",22.57,88.36),("Pune","Maharashtra","411001",18.52,73.85),("Chennai","Tamil Nadu","600001",13.08,80.27),("Ahmedabad","Gujarat","380001",23.02,72.57)]
DEVICE_FPS = [f"fp_device_{i:05d}" for i in range(10000)]

SCENARIO_TYPES = ["SHARED_DEVICE","SHARED_BANK","SHARED_GUARANTOR","DEALER_CENTRIC","RAPID_BURST","IDENTITY_REUSE","IP_REUSE","LOCATION_ANOMALY","MIXED","EMERGING"]

class Ecosystem:
    def __init__(self):
        self.customers=[]; self.mobiles=[]; self.addresses=[]; self.banks=[]; self.devices=[]; self.ips=[]; self.locations=[]; self.dealers=[]; self.guarantors=[]
        self.c_mobile=[]; self.c_address=[]; self.c_bank=[]; self.c_device=[]; self.d_c=[]; self.apps=[]; self.loans=[]; self.loan_guar=[]; self.payments=[]; self.repay=[]
        self.relationships=[]; self.clusters=[]; self.cluster_members=[]
        self.ground_truth={} # customer_id -> label
        self.demo={} # DEMO_FRAUD_xxx -> members

def generate():
    eco = Ecosystem()
    # 1. Generate base entities
    print("Generating base entities...")
    # customers
    n = TARGETS["customers"]
    n_normal = int(n*POPULATION["normal"])
    n_susp = int(n*POPULATION["suspicious"])
    n_fraud = n - n_normal - n_susp
    labels = ["normal"]*n_normal + ["suspicious"]*n_susp + ["fraud"]*n_fraud
    rng.shuffle(labels)
    for i, lab in enumerate(labels, 1):
        cid = uid(f"CUST_{i:05d}")
        eco.customers.append({
            "customer_id": cid, "customer_ref": f"C{i:05d}", "full_name": f"Synth Customer {i}",
            "date_of_birth": f"1985-01-{(i%28)+1:02d}", "gender": rng.choice(["MALE","FEMALE"]),
            "pan_hash": h(f"pan_{i}"), "aadhaar_hash": h(f"aadhar_{i}"), "occupation": rng.choice(OCCUPATIONS),
            "income_band": rng.choice(["LOW","LOWER_MIDDLE","MIDDLE","UPPER_MIDDLE","HIGH"]),
            "customer_status": "SUSPECT" if lab in ("suspicious","fraud") else "ACTIVE",
            "created_at": START + timedelta(days=rng.randint(0,10))
        })
        eco.ground_truth[str(cid)] = lab

    # addresses
    for i in range(1, TARGETS["addresses"]+1):
        city, state, pin, lat, lon = rng.choice(CITIES)
        eco.addresses.append({"address_id": uid(f"ADDR_{i:05d}"), "address_hash": h(f"addr_{i}"), "address_text": f"{i} Synth Street, {city}", "city": city, "district": city, "state": state, "pincode": pin, "latitude": lat + rng.uniform(-0.1,0.1), "longitude": lon + rng.uniform(-0.1,0.1)})

    # mobiles
    for i in range(1, TARGETS["mobiles"]+1):
        eco.mobiles.append({"mobile_id": uid(f"MOB_{i:05d}"), "mobile_hash": h(f"mob_{i}_{rng.randint(7000000000,9999999999)}"), "country_code": "+91", "mobile_status": "ACTIVE"})

    # banks
    for i in range(1, TARGETS["bank_accounts"]+1):
        eco.banks.append({"bank_account_id": uid(f"BANK_{i:05d}"), "account_hash": h(f"bank_{i}"), "bank_name": rng.choice(BANKS), "ifsc": f"SBIN0{100000+i:06d}", "account_type": "SAVINGS", "account_status": "ACTIVE"})

    # devices
    for i in range(1, TARGETS["devices"]+1):
        eco.devices.append({"device_id": uid(f"DEV_{i:05d}"), "device_fingerprint": f"fp_{h(f'dev_{i}')[:12]}", "device_type": "MOBILE", "os": "Android 13", "browser": "Chrome", "manufacturer": "Synth", "model": f"M{i%20}"})

    # ips
    for i in range(1, TARGETS["ips"]+1):
        eco.ips.append({"ip_id": uid(f"IP_{i:05d}"), "ip_hash": h(f"ip_{i}_{rng.randint(1,255)}.{rng.randint(1,255)}"), "ip_version": "V4"})

    # locations
    for i, (city, state, pin, lat, lon) in enumerate(CITIES, 1):
        eco.locations.append({"location_id": uid(f"LOC_{i:05d}"), "latitude": lat, "longitude": lon, "city": city, "district": city, "state": state, "pincode": pin})
    for i in range(len(CITIES)+1, TARGETS["locations"]+1):
        city, state, pin, lat, lon = rng.choice(CITIES)
        eco.locations.append({"location_id": uid(f"LOC_{i:05d}"), "latitude": lat + rng.uniform(-0.5,0.5), "longitude": lon + rng.uniform(-0.5,0.5), "city": city, "district": city, "state": state, "pincode": pin})

    # dealers
    for i in range(1, TARGETS["dealers"]+1):
        eco.dealers.append({"dealer_id": uid(f"DEAL_{i:04d}"), "dealer_code": f"DL{i:04d}", "dealer_name": f"Dealer {i}", "dealer_type": rng.choice(["DSA","BRANCH","ONLINE"]), "address_id": rng.choice(eco.addresses)["address_id"], "dealer_status": "ACTIVE" if rng.uniform(0,1)>0.05 else "SUSPENDED"})

    # guarantors
    for i in range(1, TARGETS["guarantors"]+1):
        eco.guarantors.append({"guarantor_id": uid(f"GUAR_{i:05d}"), "guarantor_ref": f"G{i:05d}", "full_name": f"Guarantor {i}", "identity_hash": h(f"guar_{i}"), "mobile_id": rng.choice(eco.mobiles)["mobile_id"] if rng.uniform(0,1)>0.3 else None, "address_id": rng.choice(eco.addresses)["address_id"]})

    # 2. Generate links - normal: unique, suspicious/fraud: reuse
    print("Generating links...")
    # Build pools for reuse
    fraud_customers = [c for c in eco.customers if eco.ground_truth[str(c["customer_id"])]=="fraud"]
    susp_customers = [c for c in eco.customers if eco.ground_truth[str(c["customer_id"])]=="suspicious"]
    normal_customers = [c for c in eco.customers if eco.ground_truth[str(c["customer_id"])]=="normal"]

    # For fraud, create ecosystem pools
    fraud_device_pool = eco.devices[:200]  # reuse
    fraud_mobile_pool = eco.mobiles[:200]
    fraud_bank_pool = eco.banks[:200]
    fraud_addr_pool = eco.addresses[:100]

    # For each customer, assign links with overlapping distributions
    for c in eco.customers:
        label = eco.ground_truth[str(c["customer_id"])]
        # device_count 1-3 normal, 1-5 susp, 2-7 fraud but overlapping
        if label=="normal":
            dc = rng.randint(1,3) if rng.uniform(0,1)>0.7 else 1
            devs = [rng.choice(eco.devices)] if dc==1 else rng.choices(eco.devices, k=dc)
        elif label=="suspicious":
            dc = rng.randint(1,5)
            # 50% chance reuse
            if rng.uniform(0,1)>0.5:
                devs = [rng.choice(fraud_device_pool)]
            else:
                devs = [rng.choice(eco.devices)]
            if dc>1:
                devs += rng.choices(eco.devices, k=dc-1)
        else:
            dc = rng.randint(2,7) if rng.uniform(0,1)>0.3 else rng.randint(1,3)
            devs = [rng.choice(fraud_device_pool) for _ in range(min(dc,2))] + ([rng.choice(eco.devices)] if dc>2 else [])
        for d in set([x["device_id"] if isinstance(x, dict) else x for x in devs]):
            eco.c_device.append({"customer_id": c["customer_id"], "device_id": d if isinstance(d, uuid.UUID) else d})

        # mobile similar
        if label=="normal":
            eco.c_mobile.append({"customer_id": c["customer_id"], "mobile_id": rng.choice(eco.mobiles)["mobile_id"], "relationship_type": "PRIMARY", "is_primary": True})
            if rng.uniform(0,1)>0.8:
                eco.c_mobile.append({"customer_id": c["customer_id"], "mobile_id": rng.choice(eco.mobiles)["mobile_id"], "relationship_type": "SECONDARY", "is_primary": False})
        else:
            m = rng.choice(fraud_mobile_pool)["mobile_id"] if label=="fraud" and rng.uniform(0,1)>0.4 else rng.choice(eco.mobiles)["mobile_id"]
            eco.c_mobile.append({"customer_id": c["customer_id"], "mobile_id": m, "relationship_type": "PRIMARY", "is_primary": True})
            if rng.uniform(0,1)>0.5:
                eco.c_mobile.append({"customer_id": c["customer_id"], "mobile_id": rng.choice(fraud_mobile_pool)["mobile_id"] if label=="fraud" else rng.choice(eco.mobiles)["mobile_id"], "relationship_type": "SECONDARY", "is_primary": False})

        # bank
        bc = 1 if label=="normal" and rng.uniform(0,1)>0.2 else rng.randint(1,3)
        for _ in range(bc):
            bid = rng.choice(fraud_bank_pool)["bank_account_id"] if label=="fraud" and rng.uniform(0,1)>0.5 else rng.choice(eco.banks)["bank_account_id"]
            eco.c_bank.append({"customer_id": c["customer_id"], "bank_account_id": bid, "relationship_type": "PRIMARY" if _==0 else "SECONDARY", "is_primary": _==0})

        # address
        aid = rng.choice(fraud_addr_pool)["address_id"] if label=="fraud" and rng.uniform(0,1)>0.6 else rng.choice(eco.addresses)["address_id"]
        eco.c_address.append({"customer_id": c["customer_id"], "address_id": aid, "relationship_type": "RESIDENTIAL", "is_primary": True})

    # dealer_customer_links - assign dealer per customer, fraud concentrates on few dealers
    fraud_dealers = eco.dealers[:20]
    for c in eco.customers:
        label = eco.ground_truth[str(c["customer_id"])]
        if label=="fraud":
            d = rng.choice(fraud_dealers)
        else:
            d = rng.choice(eco.dealers)
        eco.d_c.append({"dealer_id": d["dealer_id"], "customer_id": c["customer_id"], "application_count": rng.randint(1,3)})

    # 3. Fraud ecosystems - create 10 scenario types
    print("Generating fraud ecosystems...")
    ecosystems = []
    # Create 40 ecosystems, 5 demo deterministic
    demo_defs = [
        ("F-9001", "SHARED_DEVICE", 8),
        ("F-9002", "SHARED_BANK", 10),
        ("F-9003", "RAPID_BURST", 6),
        ("F-9004", "EMERGING", 12),
        ("F-9005", "MIXED", 7),
    ]
    eid_counter = 0
    for idx, (demo_ref, scen, size) in enumerate(demo_defs):
        members = [fraud_customers[idx*10 + i] for i in range(size)]
        shared_dev = eco.devices[500+idx]
        shared_bank = eco.banks[500+idx]
        shared_guar = eco.guarantors[500+idx]
        dealer = fraud_dealers[idx]
        ecosystems.append({"ref": demo_ref, "scenario": scen, "members": members, "device": shared_dev, "bank": shared_bank, "guarantor": shared_guar, "dealer": dealer, "emerging": scen=="EMERGING"})
        for m in members:
            eco.demo.setdefault(demo_ref, []).append(str(m["customer_id"]))
        # Force relationships for demo: share device/bank/guarantor/dealer
        for m in members:
            # ensure device link exists
            eco.c_device.append({"customer_id": m["customer_id"], "device_id": shared_dev["device_id"]})
            eco.c_bank.append({"customer_id": m["customer_id"], "bank_account_id": shared_bank["bank_account_id"], "relationship_type": "SECONDARY", "is_primary": False})
            # relationships will be added later

    # Additional 35 ecosystems mixed
    for i in range(35):
        scen = rng.choice(SCENARIO_TYPES)
        size = rng.randint(5,12)
        members = rng.choices(fraud_customers, k=size)
        ecosystems.append({"ref": f"F-{8000+i:04d}", "scenario": scen, "members": members, "device": rng.choice(fraud_device_pool), "bank": rng.choice(fraud_bank_pool), "guarantor": rng.choice(eco.guarantors), "dealer": rng.choice(fraud_dealers), "emerging": rng.uniform(0,1)>0.7})

    # 4. Applications (temporal)
    print("Generating applications...")
    app_id = 1
    for c in eco.customers:
        label = eco.ground_truth[str(c["customer_id"])]
        # application count distribution overlapping
        if label=="normal":
            cnt = rng.randint(1,3) if rng.uniform(0,1)>0.6 else 1
        elif label=="suspicious":
            cnt = rng.randint(1,4)
        else:
            cnt = rng.randint(2,5)
        for _ in range(cnt):
            # temporal: fraud bursts within 3 days window for ecosystems
            if label=="fraud" and rng.uniform(0,1)>0.5:
                # find ecosystem burst time
                base = START + timedelta(days=rng.randint(30,150))
            else:
                base = rng.date_between(START, END)
            dealer = next((x["dealer_id"] for x in eco.d_c if x["customer_id"]==c["customer_id"]), rng.choice(eco.dealers)["dealer_id"])
            eco.apps.append({
                "application_id": uid(f"APP_{app_id:06d}"), "application_ref": f"APP{app_id:06d}",
                "customer_id": c["customer_id"], "dealer_id": dealer,
                "requested_amount": rng.randint(50000, 1500000), "tenure_months": rng.choice([12,24,36,60]),
                "application_timestamp": base + timedelta(hours=rng.randint(0,23)),
                "application_status": rng.choice(["APPROVED","REJECTED","SUBMITTED"]) if label!="fraud" else rng.choice(["APPROVED","SUBMITTED"]),
                "decision": "APPROVED" if rng.uniform(0,1)>0.4 else "REJECTED",
                "risk_score": rng.uniform(20,95) if label=="fraud" else rng.uniform(5,60),
                "fraud_score": rng.uniform(60,99) if label=="fraud" else rng.uniform(5,40),
            })
            app_id+=1
            if app_id > TARGETS["applications"]:
                break
        if app_id > TARGETS["applications"]:
            break

    # 5. Loans (for approved apps)
    print("Generating loans...")
    loan_id = 1
    for a in eco.apps:
        if a["application_status"]=="APPROVED" and rng.uniform(0,1)>0.2 and loan_id <= TARGETS["loans"]:
            eco.loans.append({
                "loan_id": uid(f"LOAN_{loan_id:06d}"), "application_id": a["application_id"], "loan_account_ref": f"LN{loan_id:06d}",
                "sanctioned_amount": a["requested_amount"], "disbursed_amount": a["requested_amount"],
                "interest_rate": rng.uniform(10,18), "tenure_months": a["tenure_months"],
                "disbursement_date": (a["application_timestamp"] + timedelta(days=3)).date(),
                "loan_status": rng.choice(["ACTIVE","CLOSED"]) if a["customer_id"] in [c["customer_id"] for c in normal_customers] else rng.choice(["ACTIVE","DEFAULTED"])
            })
            # loan_guarantor
            if rng.uniform(0,1)>0.5:
                eco.loan_guar.append({"application_id": a["application_id"], "guarantor_id": rng.choice(eco.guarantors)["guarantor_id"]})
            loan_id+=1

    # 6. Payments
    print("Generating payments...")
    for loan in eco.loans:
        n_pay = TARGETS["payments_per_loan"] + rng.randint(-1,2)
        for i in range(max(1,n_pay)):
            is_fraud = any(str(loan["loan_id"])==str(x) for x in []) # simplification: check customer label via app
            app = next((a for a in eco.apps if a["application_id"]==loan["application_id"]), None)
            label = eco.ground_truth.get(str(app["customer_id"]), "normal") if app else "normal"
            delay = rng.randint(0,2) if label=="normal" else rng.randint(0,15)
            eco.payments.append({
                "payment_id": uid(f"PAY_{len(eco.payments)+1:07d}"), "loan_id": loan["loan_id"],
                "payment_date": loan["disbursement_date"] + timedelta(days=30*(i+1)+delay),
                "amount": loan["sanctioned_amount"]/loan["tenure_months"] + rng.uniform(-500,500),
                "payment_method": rng.choice(["NACH","UPI","NEFT"]), "payment_status": "SUCCESS" if label=="normal" or rng.uniform(0,1)>0.2 else rng.choice(["FAILED","PARTIAL"]),
                "days_past_due": delay if delay>3 else 0, "transaction_ref": f"TXN{len(eco.payments)+1:08d}", "transaction_hash": h(f"txn_{len(eco.payments)+1}")
            })

    # 7. Entity relationships (50k)
    print("Generating relationships...")
    rel_count = 0
    def add_rel(s_type, s_id, t_type, t_id, rel_type):
        eco.relationships.append({
            "relationship_id": uid(f"REL_{len(eco.relationships):07d}"), "source_entity_type": s_type, "source_entity_id": s_id,
            "target_entity_type": t_type, "target_entity_id": t_id, "relationship_type": rel_type,
            "strength": round(rng.uniform(0.7,0.99),3), "confidence": round(rng.uniform(0.7,0.99),3), "evidence_count": rng.randint(1,5)
        })
    # For each fraud ecosystem, create dense relationships
    for eco_def in ecosystems:
        members = eco_def["members"]
        for m in members:
            add_rel("CUSTOMER", m["customer_id"], "DEVICE", eco_def["device"]["device_id"], "SHARED_DEVICE")
            add_rel("CUSTOMER", m["customer_id"], "BANK_ACCOUNT", eco_def["bank"]["bank_account_id"], "SHARED_BANK_ACCOUNT")
            add_rel("CUSTOMER", m["customer_id"], "DEALER", eco_def["dealer"]["dealer_id"], "SAME_DEALER")
            if eco_def["scenario"] in ("SHARED_GUARANTOR","MIXED"):
                add_rel("CUSTOMER", m["customer_id"], "GUARANTOR", eco_def["guarantor"]["guarantor_id"], "SHARED_GUARANTOR")
        # inter-customer suspicious links
        for i in range(len(members)):
            for j in range(i+1, min(i+3, len(members))):
                add_rel("CUSTOMER", members[i]["customer_id"], "CUSTOMER", members[j]["customer_id"], "SUSPICIOUS_LINK")
    # Fill remaining with random relationships to reach 60k
    while len(eco.relationships) < TARGETS["relationships"]:
        c = rng.choice(eco.customers)
        choice = rng.randint(1,4)
        if choice==1:
            add_rel("CUSTOMER", c["customer_id"], "DEVICE", rng.choice(eco.devices)["device_id"], rng.choice(["SHARED_DEVICE","SUSPICIOUS_LINK"]))
        elif choice==2:
            add_rel("CUSTOMER", c["customer_id"], "MOBILE", rng.choice(eco.mobiles)["mobile_id"], "SHARED_MOBILE")
        elif choice==3:
            add_rel("CUSTOMER", c["customer_id"], "BANK_ACCOUNT", rng.choice(eco.banks)["bank_account_id"], "SHARED_BANK_ACCOUNT")
        else:
            add_rel("CUSTOMER", c["customer_id"], "ADDRESS", rng.choice(eco.addresses)["address_id"], "SHARED_ADDRESS")
        if len(eco.relationships)>70000:
            break

    # Fraud clusters for demo
    print("Generating clusters...")
    for idx, demo_ref in enumerate(["F-9001","F-9002","F-9003","F-9004","F-9005"]):
        cid = uid(demo_ref)
        eco.clusters.append({"cluster_id": cid, "cluster_ref": demo_ref, "cluster_type": "MIXED_ENTITY_CLUSTER", "risk_score": 85+rng.randint(0,10), "member_count": len(eco.demo.get(demo_ref,[])), "cluster_status": "ACTIVE", "detected_at": END - timedelta(days=10)})
        for mem in eco.demo.get(demo_ref,[]):
            eco.cluster_members.append({"cluster_id": cid, "entity_type": "CUSTOMER", "entity_id": uuid.UUID(mem), "membership_score": 0.9})

    # Also add remaining ecosystems as clusters
    for eco_def in ecosystems[5:15]:
        cid = uid(eco_def["ref"])
        eco.clusters.append({"cluster_id": cid, "cluster_ref": eco_def["ref"], "cluster_type": "MIXED_ENTITY_CLUSTER", "risk_score": rng.uniform(60,95), "member_count": len(eco_def["members"]), "cluster_status": "ACTIVE", "detected_at": END - timedelta(days=rng.randint(1,30))})
        for m in eco_def["members"]:
            eco.cluster_members.append({"cluster_id": cid, "entity_type": "CUSTOMER", "entity_id": m["customer_id"], "membership_score": 0.8})

    print(f"Generated: customers {len(eco.customers)}, apps {len(eco.apps)}, loans {len(eco.loans)}, payments {len(eco.payments)}, rels {len(eco.relationships)}, clusters {len(eco.clusters)}")
    return eco

if __name__=="__main__":
    generate()
