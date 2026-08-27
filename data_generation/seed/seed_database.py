"""
Bulk seed via SQLAlchemy. Safe: requires explicit --reset flag to wipe.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parents[2]))
sys.path.insert(0, str(pathlib.Path(__file__).parents[2] / "backend"))
from sqlalchemy import text
from app.database import SessionLocal
from sqlalchemy.dialects.postgresql import insert

def seed(eco, reset=False):
    db=SessionLocal()
    try:
        if reset:
            print("RESET: truncating core tables...")
            # truncate in FK order reverse
            for tbl in ["fraud_cluster_members","fraud_clusters","entity_relationships","application_events","payments","repayment_behaviour","loans","loan_guarantors","loan_applications","dealer_customer_links","customer_device_links","customer_bank_links","customer_address_links","customer_mobile_links","customers","devices","mobile_numbers","bank_accounts","addresses","dealers","guarantors","ip_addresses","locations"]:
                try: db.execute(text(f"TRUNCATE {tbl} CASCADE"))
                except: pass
            db.commit()
        # Bulk insert via executemany
        def bulk(table, rows, batch=2000):
            if not rows: return
            cols=list(rows[0].keys())
            placeholders=",".join([f":{c}" for c in cols])
            sql=text(f"INSERT INTO {table} ({','.join(cols)}) VALUES ({placeholders}) ON CONFLICT DO NOTHING")
            for i in range(0, len(rows), batch):
                db.execute(sql, rows[i:i+batch])
                db.commit()
        print("Seeding customers...")
        bulk("customers", eco.customers)
        bulk("mobile_numbers", eco.mobiles)
        bulk("addresses", eco.addresses)
        bulk("bank_accounts", eco.banks)
        bulk("devices", eco.devices)
        bulk("ip_addresses", eco.ips)
        bulk("locations", eco.locations)
        bulk("dealers", eco.dealers)
        bulk("guarantors", eco.guarantors)
        bulk("customer_device_links", [{"link_id": __import__("uuid").uuid4(), "customer_id": r["customer_id"], "device_id": r["device_id"]} for r in eco.c_device])
        bulk("customer_mobile_links", [{"link_id": __import__("uuid").uuid4(), "customer_id": r["customer_id"], "mobile_id": r["mobile_id"], "relationship_type": r["relationship_type"], "is_primary": r["is_primary"]} for r in eco.c_mobile])
        bulk("customer_bank_links", [{"link_id": __import__("uuid").uuid4(), "customer_id": r["customer_id"], "bank_account_id": r["bank_account_id"], "relationship_type": r["relationship_type"], "is_primary": r["is_primary"]} for r in eco.c_bank])
        bulk("customer_address_links", [{"link_id": __import__("uuid").uuid4(), "customer_id": r["customer_id"], "address_id": r["address_id"], "relationship_type": r["relationship_type"], "is_primary": r["is_primary"]} for r in eco.c_address])
        bulk("dealer_customer_links", [{"link_id": __import__("uuid").uuid4(), "dealer_id": r["dealer_id"], "customer_id": r["customer_id"], "application_count": r["application_count"]} for r in eco.d_c])
        bulk("loan_applications", eco.apps)
        bulk("loans", eco.loans)
        bulk("loan_guarantors", [{"link_id": __import__("uuid").uuid4(), "application_id": r["application_id"], "guarantor_id": r["guarantor_id"]} for r in eco.loan_guar])
        bulk("payments", eco.payments)
        bulk("entity_relationships", [{**r, "first_seen": r.get("first_seen") or __import__("datetime").datetime.now(__import__("datetime").timezone.utc), "last_seen": r.get("last_seen") or __import__("datetime").datetime.now(__import__("datetime").timezone.utc)} for r in eco.relationships])
        bulk("fraud_clusters", eco.clusters)
        bulk("fraud_cluster_members", [{"member_id": __import__("uuid").uuid4(), "cluster_id": r["cluster_id"], "entity_type": r["entity_type"], "entity_id": r["entity_id"], "membership_score": r["membership_score"]} for r in eco.cluster_members])
        db.commit()
        print(f"Seed done: {len(eco.customers)} customers, {len(eco.apps)} apps, {len(eco.relationships)} rels")
    finally:
        db.close()

if __name__=="__main__":
    from data_generation.generator import generate
    from data_generation.validation.validator import validate, report
    eco=generate()
    errs=validate(eco)
    print("Validation:", errs or "OK")
    print(report(eco))
    import argparse
    p=__import__("argparse").ArgumentParser(); p.add_argument("--reset", action="store_true")
    args=p.parse_args()
    seed(eco, reset=args.reset)
