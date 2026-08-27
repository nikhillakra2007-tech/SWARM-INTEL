"""
Generate synthetic seed SQL for Swarm Intelligence Lending Network.
All identifiers are synthetic/hashed. No real PII.
Run: python database/scripts/generate_seeds.py
Outputs: database/seeds/001_*.sql .. 005_*.sql
"""
import uuid, hashlib, textwrap, os, random, datetime

SEED_DIR = os.path.join(os.path.dirname(__file__), '..', 'seeds')
def uid(name): return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))
def h(val): return hashlib.sha256(val.encode()).hexdigest()  # 64 hex chars

random.seed(42)

# --- Define entity maps ---
customers = {}  # ref -> {uuid, name, ...}
for i in range(1, 21):
    ref = f'C{i:03d}'
    customers[ref] = uid(ref)

addresses = {f'A{i:03d}': uid(f'A{i:03d}') for i in range(1, 21)}
mobiles   = {f'M{i:03d}': uid(f'M{i:03d}') for i in range(1, 16)}
devices   = {f'D{i:03d}': uid(f'D{i:03d}') for i in range(1, 13)}
banks     = {f'B{i:03d}': uid(f'B{i:03d}') for i in range(1, 13)}
dealers   = {f'DL{i:03d}': uid(f'DL{i:03d}') for i in range(1, 7)}
guarantors= {f'G{i:03d}': uid(f'G{i:03d}') for i in range(1, 7)}
ips       = {f'IP{i:03d}': uid(f'IP{i:03d}') for i in range(1, 9)}
locs      = {f'LOC{i:03d}': uid(f'LOC{i:03d}') for i in range(1, 9)}
apps      = {f'APP{i:04d}': uid(f'APP{i:04d}') for i in range(1, 26)}
loans     = {f'LN{i:04d}': uid(f'LN{i:04d}') for i in range(1, 19)}
clusters  = {'F-1001': uid('F-1001'), 'F-1002': uid('F-1002')}
models    = {f'MODEL{i}': uid(f'MODEL{i}') for i in range(1, 4)}
alerts    = {f'ALT-{1001+i}': uid(f'ALT-{1001+i}') for i in range(6)}
invs      = {f'INV{i:04d}': uid(f'INV{i:04d}') for i in range(1, 5)}

# Customer archetypes: 12 normal, 8 suspicious (including F-1001 cluster of 4)
normal_customers = [f'C{i:03d}' for i in range(1, 13)]
fraud_cluster_members_refs = ['C013','C014','C015','C016']  # F-1001 core (maps to spec C001 etc conceptually)
suspicious_extra = ['C017','C018','C019','C020']  # F-1002 / secondary ring

# Names synthetic
names = [
    "Aarav Mehta","Priya Sharma","Rohan Desai","Ananya Gupta","Vikram Singh","Sneha Reddy","Arjun Patel","Kavya Nair","Rahul Verma","Neha Kapoor",
    "Siddharth Rao","Pooja Joshi","Imran Khan","Farah Sheikh","Amit Yadav","Sunita Mishra","Karan Malhotra","Divya Pillai","Sameer Ali","Meera Krishnan"
]

def sql_str(s): return "'" + s.replace("'","''") + "'"

# Build SQL pieces
out = {}

# ============ 001_reference_data.sql ============
lines = []
lines.append("-- =============================================================================\n-- 001_reference_data.sql — Reference entities (addresses, dealers, guarantors, mobiles, devices, IPs, locations, bank accounts, models)\n-- All values synthetic / hashed. No real PII.\n-- =============================================================================\n")

# Addresses
lines.append("-- Addresses (20)")
addr_data = [
    ("A001","Bandra West","Mumbai","Maharashtra","400050",19.0596,72.8295),
    ("A002","Koramangala","Bengaluru","Karnataka","560034",12.9352,77.6245),
    ("A003","Connaught Place","New Delhi","Delhi","110001",28.6315,77.2167),
    ("A004","Salt Lake","Kolkata","West Bengal","700091",22.5804,88.4120),
    ("A005","Banjara Hills","Hyderabad","Telangana","500034",17.4156,78.4348),
    ("A006","Andheri East","Mumbai","Maharashtra","400069",19.1136,72.8697),
    ("A007","Whitefield","Bengaluru","Karnataka","560066",12.9698,77.7500),
    ("A008","Dwarka","New Delhi","Delhi","110075",28.5921,77.0460),
    ("A009","Park Street","Kolkata","West Bengal","700016",22.5532,88.3480),
    ("A010","Gachibowli","Hyderabad","Telangana","500032",17.4400,78.3480),
    ("A011","Powai","Mumbai","Maharashtra","400076",19.1176,72.9060),
    ("A012","Indiranagar","Bengaluru","Karnataka","560038",12.9784,77.6408),
    ("A013","Dharavi Shared Chawl Block 7","Mumbai","Maharashtra","400017",19.0420,72.8560),  # shared fraud address
    ("A014","Old City Shared Lane 4A","Hyderabad","Telangana","500002",17.3616,78.4747),  # shared
    ("A015","Laxmi Nagar","New Delhi","Delhi","110092",28.6349,77.2750),
    ("A016","Hinjewadi","Pune","Maharashtra","411057",18.5912,73.7380),
    ("A017","Adyar","Chennai","Tamil Nadu","600020",13.0012,80.2565),
    ("A018","Vastrapur","Ahmedabad","Gujarat","380015",23.0330,72.5240),
    ("A019","Shared Address - Fraud Cluster","Mumbai","Maharashtra","400017",19.0420,72.8565),  # near A013
    ("A020","Malad West","Mumbai","Maharashtra","400064",19.1876,72.8484),
]
# (dead loop removed) — clean addr_rows defined below
addr_rows = [
    ("A001","Flat 302, Sunshine Apts, Bandra West","Mumbai","Mumbai","Maharashtra","400050",19.0596,72.8295),
    ("A002","12/4 80 Feet Road, Koramangala","Bengaluru","Bengaluru","Karnataka","560034",12.9352,77.6245),
    ("A003","Block C, Inner Circle, CP","New Delhi","New Delhi","Delhi","110001",28.6315,77.2167),
    ("A004","AE-123 Sector 1, Salt Lake","Kolkata","Kolkata","West Bengal","700091",22.5804,88.4120),
    ("A005","Road No.12, House 44, Banjara Hills","Hyderabad","Hyderabad","Telangana","500034",17.4156,78.4348),
    ("A006","Marol Naka, 5th Lane, Andheri East","Mumbai","Mumbai","Maharashtra","400069",19.1136,72.8697),
    ("A007","ITPL Road, Bldg 7, Whitefield","Bengaluru","Bengaluru","Karnataka","560066",12.9698,77.7500),
    ("A008","Sector 10, Pocket 2, Dwarka","New Delhi","New Delhi","Delhi","110075",28.5921,77.0460),
    ("A009","12 Park Street, Floor 3","Kolkata","Kolkata","West Bengal","700016",22.5532,88.3480),
    ("A010","DLF Cyber City, Block A, Gachibowli","Hyderabad","Hyderabad","Telangana","500032",17.4400,78.3480),
    ("A011","Hiranandani, Bldg 9, Powai","Mumbai","Mumbai","Maharashtra","400076",19.1176,72.9060),
    ("A012","100 Feet Road, 4th Cross, Indiranagar","Bengaluru","Bengaluru","Karnataka","560038",12.9784,77.6408),
    ("A013","Dharavi Shared Chawl Block 7, Room 12","Mumbai","Mumbai","Maharashtra","400017",19.0420,72.8560),
    ("A014","Old City Shared Lane 4A, House 22","Hyderabad","Hyderabad","Telangana","500002",17.3616,78.4747),
    ("A015","Vikas Marg, A-44, Laxmi Nagar","New Delhi","New Delhi","Delhi","110092",28.6349,77.2750),
    ("A016","Phase 2, Building 11, Hinjewadi","Pune","Pune","Maharashtra","411057",18.5912,73.7380),
    ("A017","Lattice Bridge Road, Adyar","Chennai","Chennai","Tamil Nadu","600020",13.0012,80.2565),
    ("A018","Wide Angle, CG Road, Vastrapur","Ahmedabad","Ahmedabad","Gujarat","380015",23.0330,72.5240),
    ("A019","Dharavi Shared Chawl Block 7, Room 14","Mumbai","Mumbai","Maharashtra","400017",19.0420,72.8565),
    ("A020","Link Road, Evershine Nagar, Malad","Mumbai","Mumbai","Maharashtra","400064",19.1876,72.8484),
]
lines.append("INSERT INTO addresses (address_id, address_hash, address_text, city, district, state, pincode, latitude, longitude) VALUES")
vals = []
for ref, text, city, district, state, pin, lat, lon in addr_rows:
    ah = h(f"addr-{ref}-{text}")
    vals.append(f"  ('{addresses[ref]}', '{ah}', {sql_str(text)}, {sql_str(city)}, {sql_str(district)}, {sql_str(state)}, '{pin}', {lat}, {lon})")
lines.append(",\n".join(vals) + ";\n")

# Mobile numbers - M002 shared fraud, M005 shared fraud
lines.append("-- Mobile numbers (15) — M002 and M005 are shared across fraud cluster")
mob_vals = []
for i in range(1,16):
    ref = f'M{i:03d}'
    raw = f'90000000{i:02d}'
    mh = h(f'mob-{raw}')
    status = 'SUSPECT' if ref in ('M002','M005','M009') else 'ACTIVE'
    mob_vals.append(f"  ('{mobiles[ref]}', '{mh}', '+91', '{status}', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00')")
lines.append("INSERT INTO mobile_numbers (mobile_id, mobile_hash, country_code, mobile_status, first_seen, last_seen) VALUES")
lines.append(",\n".join(mob_vals) + ";\n")

# Devices - D004 shared, D009 shared
lines.append("-- Devices (12) — D004 and D009 shared across multiple fraud customers")
dev_rows = [
    ("D001","fp_iphone15_abc111","MOBILE","iOS 17","Safari","Apple","iPhone 15"),
    ("D002","fp_pixel8_xyz222","MOBILE","Android 14","Chrome","Google","Pixel 8"),
    ("D003","fp_samsung_s23_qrs333","MOBILE","Android 14","Chrome","Samsung","Galaxy S23"),
    ("D004","fp_shared_device_FRAUD_X1","MOBILE","Android 13","Chrome","Xiaomi","Redmi Note 12"),  # shared fraud
    ("D005","fp_oneplus_11_aaa444","MOBILE","Android 14","Chrome","OnePlus","11R"),
    ("D006","fp_iphone14_bbb555","MOBILE","iOS 16","Safari","Apple","iPhone 14"),
    ("D007","fp_desktop_win_chrome_ccc666","DESKTOP","Windows 11","Chrome","Dell","Inspiron 15"),
    ("D008","fp_ipad_ddd777","TABLET","iPadOS 17","Safari","Apple","iPad Air"),
    ("D009","fp_shared_device_FRAUD_X2","MOBILE","Android 13","Chrome","Realme","Narzo 60"),  # shared fraud
    ("D010","fp_samsung_a54_eee888","MOBILE","Android 14","Chrome","Samsung","Galaxy A54"),
    ("D011","fp_moto_g73_fff999","MOBILE","Android 13","Chrome","Motorola","Moto G73"),
    ("D012","fp_iphone13_ggg000","MOBILE","iOS 17","Safari","Apple","iPhone 13"),
]
dev_vals=[]
for ref, fp, dtype, os_, browser, manuf, model in dev_rows:
    status='SUSPECT' if ref in ('D004','D009') else 'ACTIVE'
    dev_vals.append(f"  ('{devices[ref]}', '{fp}', '{dtype}', {sql_str(os_)}, {sql_str(browser)}, {sql_str(manuf)}, {sql_str(model)}, '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', '{status}')")
lines.append("INSERT INTO devices (device_id, device_fingerprint, device_type, os, browser, manufacturer, model, first_seen, last_seen, device_status) VALUES")
lines.append(",\n".join(dev_vals) + ";\n")

# IP addresses
lines.append("-- IP addresses (8) — IP001 shared fraud IP")
ip_vals=[]
for i in range(1,9):
    ref=f'IP{i:03d}'
    raw=f'203.0.113.{10+i}'
    ih=h(f'ip-{raw}')
    ip_vals.append(f"  ('{ips[ref]}', '{ih}', 'V4', '2025-03-01 10:00:00+00', '2026-08-21 14:00:00+00')")
lines.append("INSERT INTO ip_addresses (ip_id, ip_hash, ip_version, first_seen, last_seen) VALUES")
lines.append(",\n".join(ip_vals) + ";\n")

# Locations
lines.append("-- Locations (8)")
loc_rows=[
    ("LOC001",19.0596,72.8295,"Mumbai","Mumbai","Maharashtra","400050"),
    ("LOC002",12.9352,77.6245,"Bengaluru","Bengaluru","Karnataka","560034"),
    ("LOC003",28.6315,77.2167,"New Delhi","New Delhi","Delhi","110001"),
    ("LOC004",17.4156,78.4348,"Hyderabad","Hyderabad","Telangana","500034"),
    ("LOC005",22.5804,88.4120,"Kolkata","Kolkata","West Bengal","700091"),
    ("LOC006",19.0420,72.8560,"Mumbai","Mumbai","Maharashtra","400017"),  # fraud hub
    ("LOC007",18.5912,73.7380,"Pune","Pune","Maharashtra","411057"),
    ("LOC008",13.0012,80.2565,"Chennai","Chennai","Tamil Nadu","600020"),
]
loc_vals=[]
for ref, lat, lon, city, district, state, pin in loc_rows:
    loc_vals.append(f"  ('{locs[ref]}', {lat}, {lon}, {sql_str(city)}, {sql_str(district)}, {sql_str(state)}, '{pin}')")
lines.append("INSERT INTO locations (location_id, latitude, longitude, city, district, state, pincode) VALUES")
lines.append(",\n".join(loc_vals) + ";\n")

# Bank accounts — B007 shared fraud, B009 shared
lines.append("-- Bank accounts (12) — B007 shared across fraud cluster")
bank_vals=[]
bank_meta=[
    ("B001","State Bank of India","SBIN0000001"),
    ("B002","HDFC Bank","HDFC0000002"),
    ("B003","ICICI Bank","ICIC0000003"),
    ("B004","Axis Bank","UTIB0000004"),
    ("B005","Kotak Mahindra","KKBK0000005"),
    ("B006","Punjab National Bank","PUNB0000006"),
    ("B007","State Bank of India","SBIN0000007"),  # fraud shared
    ("B008","HDFC Bank","HDFC0000008"),
    ("B009","ICICI Bank","ICIC0000009"),  # secondary fraud
    ("B010","Axis Bank","UTIB0000010"),
    ("B011","Bank of Baroda","BARB0000011"),
    ("B012","IndusInd Bank","INDB0000012"),
]
for ref, bank, ifsc in bank_meta:
    ah=h(f'bank-{ref}-{bank}')
    status='SUSPECT' if ref in ('B007','B009') else 'ACTIVE'
    bank_vals.append(f"  ('{banks[ref]}', '{ah}', {sql_str(bank)}, '{ifsc}', 'SAVINGS', '{status}', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00')")
lines.append("INSERT INTO bank_accounts (bank_account_id, account_hash, bank_name, ifsc, account_type, account_status, first_seen, last_seen) VALUES")
lines.append(",\n".join(bank_vals) + ";\n")

# Dealers — DL003 fraud cluster dealer
lines.append("-- Dealers (6) — DL003 is high-velocity fraud dealer")
dealer_rows=[
    ("DL001","Alpha Auto Finance","DSA",addresses["A001"],"ACTIVE","2024-06-01"),
    ("DL002","Bengaluru Wheels Corp","BRANCH",addresses["A002"],"ACTIVE","2024-07-15"),
    ("DL003","Metro Quick Loans - Dharavi","DSA",addresses["A013"],"ACTIVE","2025-01-10"),  # fraud
    ("DL004","Hyderabad Prime Motors","DSA",addresses["A005"],"ACTIVE","2024-08-20"),
    ("DL005","Delhi Capital Lending","BRANCH",addresses["A003"],"ACTIVE","2024-09-01"),
    ("DL006","Pune Express Finance","ONLINE",addresses["A016"],"SUSPENDED","2024-10-01"),  # suspended
]
d_vals=[]
for ref, name, dtype, addr_id, status, onboarding in dealer_rows:
    d_vals.append(f"  ('{dealers[ref]}', '{ref}', {sql_str(name)}, '{dtype}', '{addr_id}', '{status}', '{onboarding}')")
lines.append("INSERT INTO dealers (dealer_id, dealer_code, dealer_name, dealer_type, address_id, dealer_status, onboarding_date) VALUES")
lines.append(",\n".join(d_vals) + ";\n")

# Guarantors — G005 shared fraud
lines.append("-- Guarantors (6) — G005 shared across fraud applications")
guar_rows=[
    ("G001","Rajesh Kumar",None,addresses["A006"]),
    ("G002","Sunita Devi",mobiles["M010"],addresses["A007"]),
    ("G003","Amit Sharma",mobiles["M011"],addresses["A008"]),
    ("G004","Lakshmi Iyer",mobiles["M012"],addresses["A009"]),
    ("G005","FARID SHAIKH - FRAUD RING",mobiles["M002"],addresses["A013"]),  # shared
    ("G006","Vikash Tiwari",mobiles["M013"],addresses["A015"]),
]
g_vals=[]
for ref, name, mob_id, addr_id in guar_rows:
    ih=h(f'guar-{ref}-{name}')
    mob_sql = f"'{mob_id}'" if mob_id else "NULL"
    addr_sql= f"'{addr_id}'" if addr_id else "NULL"
    g_vals.append(f"  ('{guarantors[ref]}', '{ref}', {sql_str(name)}, '{ih}', {mob_sql}, {addr_sql})")
lines.append("INSERT INTO guarantors (guarantor_id, guarantor_ref, full_name, identity_hash, mobile_id, address_id) VALUES")
lines.append(",\n".join(g_vals) + ";\n")

# Model versions
lines.append("-- Model versions (3)")
lines.append("INSERT INTO model_versions (model_id, model_name, version, model_type, training_completed_at, performance_metrics, model_status) VALUES")
lines.append(f"  ('{models['MODEL1']}', 'swarm-fraud-v1', '1.0.0', 'FRAUD_CLASSIFIER', '2026-01-15 10:00:00+00', '{{\"auc\":0.82,\"precision\":0.78,\"recall\":0.71}}', 'RETIRED'),")
lines.append(f"  ('{models['MODEL2']}', 'swarm-fraud-v2', '2.1.0', 'FRAUD_CLASSIFIER', '2026-05-01 10:00:00+00', '{{\"auc\":0.89,\"precision\":0.84,\"recall\":0.80}}', 'ACTIVE'),")
lines.append(f"  ('{models['MODEL3']}', 'swarm-risk-v1', '1.2.0', 'RISK_SCORER', '2026-06-01 10:00:00+00', '{{\"mse\":0.04,\"mae\":0.12}}', 'ACTIVE');\n")

out['001_reference_data.sql'] = "\n".join(lines)

# ============ 002_customers.sql ============
lines=[]
lines.append("-- =============================================================================\n-- 002_customers.sql — Customers (20) + link tables\n-- 12 normal (C001-C012), 4 F-1001 fraud cluster (C013-C016), 4 F-1002 ring (C017-C020)\n-- =============================================================================\n")
cust_rows_info=[
    ("C001","Aarav Mehta","1992-04-12","MALE","ENGINEER","MIDDLE","ACTIVE"),
    ("C002","Priya Sharma","1990-07-23","FEMALE","TEACHER","MIDDLE","ACTIVE"),
    ("C003","Rohan Desai","1988-11-05","MALE","BUSINESS","UPPER_MIDDLE","ACTIVE"),
    ("C004","Ananya Gupta","1995-02-18","FEMALE","DOCTOR","HIGH","ACTIVE"),
    ("C005","Vikram Singh","1985-09-30","MALE","GOVERNMENT","MIDDLE","ACTIVE"),
    ("C006","Sneha Reddy","1993-06-14","FEMALE","IT","UPPER_MIDDLE","ACTIVE"),
    ("C007","Arjun Patel","1991-12-01","MALE","SALES","LOWER_MIDDLE","ACTIVE"),
    ("C008","Kavya Nair","1994-03-22","FEMALE","LAWYER","HIGH","ACTIVE"),
    ("C009","Rahul Verma","1987-08-09","MALE","CONTRACTOR","MIDDLE","ACTIVE"),
    ("C010","Neha Kapoor","1996-05-17","FEMALE","STUDENT","LOW","ACTIVE"),
    ("C011","Siddharth Rao","1989-10-11","MALE","ENGINEER","MIDDLE","ACTIVE"),
    ("C012","Pooja Joshi","1992-01-25","FEMALE","NURSE","LOWER_MIDDLE","ACTIVE"),
    # Fraud cluster F-1001
    ("C013","Imran Khan","1993-03-08","MALE","DRIVER","LOW","SUSPECT"),
    ("C014","Farah Sheikh","1994-09-19","FEMALE","SELF_EMPLOYED","LOW","SUSPECT"),
    ("C015","Amit Yadav","1990-12-30","MALE","UNEMPLOYED","LOW","SUSPECT"),
    ("C016","Sunita Mishra","1991-06-06","FEMALE","HOUSEWIFE","LOW","SUSPECT"),
    # Secondary suspicious ring F-1002
    ("C017","Karan Malhotra","1988-04-04","MALE","AGENT","LOWER_MIDDLE","SUSPECT"),
    ("C018","Divya Pillai","1995-08-12","FEMALE","CLERK","LOWER_MIDDLE","SUSPECT"),
    ("C019","Sameer Ali","1992-11-11","MALE","DRIVER","LOW","SUSPECT"),
    ("C020","Meera Krishnan","1993-07-07","FEMALE","TAILOR","LOW","SUSPECT"),
]
lines.append("INSERT INTO customers (customer_id, customer_ref, full_name, date_of_birth, gender, pan_hash, aadhaar_hash, occupation, income_band, customer_status) VALUES")
c_vals=[]
for ref, name, dob, gender, occ, inc, status in cust_rows_info:
    pan=h(f'pan-{ref}-{name}')
    aad=h(f'aadhaar-{ref}-{name}')
    c_vals.append(f"  ('{customers[ref]}', '{ref}', {sql_str(name)}, '{dob}', '{gender}', '{pan}', '{aad}', {sql_str(occ)}, '{inc}', '{status}')")
lines.append(",\n".join(c_vals) + ";\n")

# Customer-mobile links
lines.append("-- Customer ↔ Mobile links — fraud reuses M002, M005")
cm_links=[
    ("C001","M001","PRIMARY",True),("C002","M003","PRIMARY",True),("C003","M004","PRIMARY",True),
    ("C004","M006","PRIMARY",True),("C005","M007","PRIMARY",True),("C006","M008","PRIMARY",True),
    ("C007","M010","PRIMARY",True),("C008","M011","PRIMARY",True),("C009","M012","PRIMARY",True),
    ("C010","M013","PRIMARY",True),("C011","M014","PRIMARY",True),("C012","M015","PRIMARY",True),
    # Fraud cluster: 4 customers share M002
    ("C013","M002","PRIMARY",True),("C014","M002","PRIMARY",True),("C015","M002","SECONDARY",False),("C016","M002","SECONDARY",False),
    # Extra links for network density
    ("C015","M005","PRIMARY",True),("C016","M005","SECONDARY",False),
    # Secondary ring shares M009
    ("C017","M009","PRIMARY",True),("C018","M009","PRIMARY",True),("C019","M005","PRIMARY",True),("C020","M009","SECONDARY",False),
]
lines.append("INSERT INTO customer_mobile_links (customer_id, mobile_id, relationship_type, is_primary, first_seen, last_seen) VALUES")
cm_vals=[f"  ('{customers[c]}', '{mobiles[m]}', '{rt}', {str(primary).lower()}, '2025-06-01 09:00:00+00', '2026-08-20 10:00:00+00')" for c,m,rt,primary in cm_links]
lines.append(",\n".join(cm_vals) + ";\n")

# Customer-address links
lines.append("-- Customer ↔ Address links — fraud shares A013")
ca_links=[
    ("C001","A001","RESIDENTIAL",True),("C002","A002","RESIDENTIAL",True),("C003","A003","RESIDENTIAL",True),
    ("C004","A004","RESIDENTIAL",True),("C005","A005","RESIDENTIAL",True),("C006","A006","RESIDENTIAL",True),
    ("C007","A007","RESIDENTIAL",True),("C008","A008","RESIDENTIAL",True),("C009","A009","RESIDENTIAL",True),
    ("C010","A010","RESIDENTIAL",True),("C011","A011","RESIDENTIAL",True),("C012","A012","RESIDENTIAL",True),
    ("C013","A013","RESIDENTIAL",True),("C014","A013","RESIDENTIAL",True),("C015","A013","RESIDENTIAL",True),("C016","A019","RESIDENTIAL",True),
    ("C017","A014","RESIDENTIAL",True),("C018","A014","RESIDENTIAL",True),("C019","A015","RESIDENTIAL",True),("C020","A016","RESIDENTIAL",True),
]
lines.append("INSERT INTO customer_address_links (customer_id, address_id, relationship_type, is_primary, first_seen, last_seen) VALUES")
ca_vals=[f"  ('{customers[c]}', '{addresses[a]}', '{rt}', {str(p).lower()}, '2025-06-01 09:00:00+00', '2026-08-20 10:00:00+00')" for c,a,rt,p in ca_links]
lines.append(",\n".join(ca_vals) + ";\n")

# Customer-bank links — B007 shared fraud
lines.append("-- Customer ↔ Bank Account links — B007 shared across F-1001")
cb_links=[
    ("C001","B001","PRIMARY",True),("C002","B002","PRIMARY",True),("C003","B003","PRIMARY",True),
    ("C004","B004","PRIMARY",True),("C005","B005","PRIMARY",True),("C006","B006","PRIMARY",True),
    ("C007","B008","PRIMARY",True),("C008","B010","PRIMARY",True),("C009","B011","PRIMARY",True),
    ("C010","B012","PRIMARY",True),("C011","B001","SECONDARY",False),("C012","B002","SECONDARY",False),  # normal reuse low
    ("C013","B007","PRIMARY",True),("C014","B007","PRIMARY",True),("C015","B007","PRIMARY",True),("C016","B007","SECONDARY",False),
    ("C017","B009","PRIMARY",True),("C018","B009","PRIMARY",True),("C019","B007","SECONDARY",False),("C020","B009","SECONDARY",False),
]
lines.append("INSERT INTO customer_bank_links (customer_id, bank_account_id, relationship_type, is_primary, first_seen, last_seen) VALUES")
cb_vals=[f"  ('{customers[c]}', '{banks[b]}', '{rt}', {str(p).lower()}, '2025-06-15 09:00:00+00', '2026-08-20 11:00:00+00')" for c,b,rt,p in cb_links]
lines.append(",\n".join(cb_vals) + ";\n")

# Customer-device links — D004 shared
lines.append("-- Customer ↔ Device links — D004 and D009 shared")
cd_links=[
    ("C001","D001"),("C002","D002"),("C003","D003"),("C004","D005"),("C005","D006"),("C006","D007"),
    ("C007","D008"),("C008","D010"),("C009","D011"),("C010","D012"),("C011","D001"),("C012","D002"),
    ("C013","D004"),("C014","D004"),("C015","D004"),("C016","D009"),
    ("C017","D009"),("C018","D009"),("C019","D004"),("C020","D009"),
]
lines.append("INSERT INTO customer_device_links (customer_id, device_id, first_seen, last_seen) VALUES")
cd_vals=[f"  ('{customers[c]}', '{devices[d]}', '2025-07-01 09:00:00+00', '2026-08-21 12:00:00+00')" for c,d in cd_links]
lines.append(",\n".join(cd_vals) + ";\n")

# Dealer-customer links
lines.append("-- Dealer ↔ Customer links")
dc_links=[
    ("DL001","C001"),("DL001","C002"),("DL002","C003"),("DL002","C004"),("DL004","C005"),("DL004","C006"),
    ("DL005","C007"),("DL005","C008"),("DL001","C009"),("DL002","C010"),("DL004","C011"),("DL005","C012"),
    # Fraud dealer DL003 owns 8 fraud customers
    ("DL003","C013"),("DL003","C014"),("DL003","C015"),("DL003","C016"),("DL003","C017"),("DL003","C018"),("DL003","C019"),("DL003","C020"),
    ("DL006","C017"),  # also linked to suspended dealer
]
lines.append("INSERT INTO dealer_customer_links (dealer_id, customer_id, first_application_at, last_application_at, application_count) VALUES")
dc_vals=[]
for dl,c in dc_links:
    cnt= 2 if c in ("C013","C017") else 1
    dc_vals.append(f"  ('{dealers[dl]}', '{customers[c]}', '2026-07-01 10:00:00+00', '2026-08-18 10:00:00+00', {cnt})")
lines.append(",\n".join(dc_vals) + ";\n")

out['002_customers.sql'] = "\n".join(lines)

# ============ 003_lending_data.sql ============
lines=[]
lines.append("-- =============================================================================\n-- 003_lending_data.sql — Loan applications, loans, payments, repayment behaviour, risk scores, predictions, fraud signals\n-- =============================================================================\n")

# Loan applications 25
lines.append("-- Loan applications (25) — fraud burst 2026-08-10 to 2026-08-18 via DL003")
app_data=[]
# Normal apps
norm_apps=[
    ("APP0001","C001","DL001",500000,36,"2026-06-01 10:00:00+00","APPROVED","APPROVED",22.5,12.3),
    ("APP0002","C002","DL001",300000,24,"2026-06-05 11:00:00+00","APPROVED","APPROVED",18.0,10.1),
    ("APP0003","C003","DL002",800000,60,"2026-06-10 09:30:00+00","APPROVED","APPROVED",31.2,14.5),
    ("APP0004","C004","DL002",1200000,48,"2026-06-12 14:00:00+00","APPROVED","APPROVED",25.0,11.0),
    ("APP0005","C005","DL004",400000,36,"2026-06-15 10:00:00+00","REJECTED","REJECTED",55.0,42.0),
    ("APP0006","C006","DL004",600000,24,"2026-06-18 16:00:00+00","APPROVED","APPROVED",20.0,9.5),
    ("APP0007","C007","DL005",250000,18,"2026-06-20 09:00:00+00","APPROVED","APPROVED",28.0,15.2),
    ("APP0008","C008","DL005",900000,36,"2026-06-22 11:00:00+00","APPROVED","APPROVED",24.5,13.0),
    ("APP0009","C009","DL001",350000,24,"2026-06-25 13:00:00+00","APPROVED","APPROVED",19.5,8.8),
    ("APP0010","C010","DL002",200000,12,"2026-06-28 10:00:00+00","APPROVED","APPROVED",16.0,7.2),
    ("APP0011","C011","DL004",450000,36,"2026-07-01 10:00:00+00","APPROVED","APPROVED",21.0,10.5),
    ("APP0012","C012","DL005",300000,24,"2026-07-03 15:00:00+00","APPROVED","APPROVED",23.0,12.0),
    # Fraud burst — same dealer DL003, tight window
    ("APP0013","C013","DL003",750000,36,"2026-08-10 09:15:00+00","APPROVED","APPROVED",78.5,88.2),
    ("APP0014","C014","DL003",800000,36,"2026-08-10 09:45:00+00","APPROVED","APPROVED",81.0,90.1),
    ("APP0015","C015","DL003",700000,36,"2026-08-10 10:30:00+00","APPROVED","APPROVED",85.0,92.5),
    ("APP0016","C016","DL003",650000,36,"2026-08-11 09:00:00+00","APPROVED","APPROVED",79.2,87.0),
    ("APP0017","C017","DL003",600000,24,"2026-08-12 10:00:00+00","UNDER_REVIEW","PENDING",72.0,82.3),
    ("APP0018","C018","DL003",550000,24,"2026-08-12 11:00:00+00","UNDER_REVIEW","PENDING",70.5,80.1),
    ("APP0019","C019","DL003",700000,36,"2026-08-13 09:30:00+00","SUBMITTED","PENDING",68.0,78.5),
    ("APP0020","C020","DL003",500000,24,"2026-08-14 10:00:00+00","SUBMITTED","PENDING",65.0,75.0),
    # Extra fraud attempts second guarantor reuse
    ("APP0021","C013","DL003",400000,18,"2026-08-15 09:00:00+00","SUBMITTED","PENDING",88.0,94.0),
    ("APP0022","C015","DL006",300000,12,"2026-08-16 10:00:00+00","REJECTED","REJECTED",90.0,95.5),
    ("APP0023","C017","DL006",450000,24,"2026-08-17 11:00:00+00","SUBMITTED","PENDING",74.0,84.0),
    ("APP0024","C001","DL001",200000,12,"2026-08-18 09:00:00+00","APPROVED","APPROVED",20.5,11.0),  # normal second app
    ("APP0025","C019","DL003",300000,12,"2026-08-18 14:00:00+00","SUBMITTED","PENDING",69.0,79.0),
]
lines.append("INSERT INTO loan_applications (application_id, application_ref, customer_id, dealer_id, requested_amount, tenure_months, application_timestamp, application_status, decision, risk_score, fraud_score) VALUES")
app_vals=[]
for ref,cust,dealer,amt,tenure,ts,status,dec,risk,fraud in norm_apps:
    dealer_sql = f"'{dealers[dealer]}'" if dealer else "NULL"
    app_vals.append(f"  ('{apps[ref]}', '{ref}', '{customers[cust]}', {dealer_sql}, {amt}, {tenure}, '{ts}', '{status}', '{dec}', {risk}, {fraud})")
lines.append(",\n".join(app_vals) + ";\n")

# Loans 18 (only for approved apps)
lines.append("-- Loans (18)")
loan_map=[
    ("LN0001","APP0001",500000,500000,11.5,36,"2026-06-03","ACTIVE"),
    ("LN0002","APP0002",300000,300000,12.0,24,"2026-06-07","ACTIVE"),
    ("LN0003","APP0003",800000,800000,10.8,60,"2026-06-12","ACTIVE"),
    ("LN0004","APP0004",1200000,1200000,11.0,48,"2026-06-14","ACTIVE"),
    ("LN0005","APP0006",600000,600000,12.5,24,"2026-06-20","ACTIVE"),
    ("LN0006","APP0007",250000,250000,13.0,18,"2026-06-22","ACTIVE"),
    ("LN0007","APP0008",900000,900000,11.2,36,"2026-06-24","ACTIVE"),
    ("LN0008","APP0009",350000,350000,12.8,24,"2026-06-27","ACTIVE"),
    ("LN0009","APP0010",200000,200000,14.0,12,"2026-06-30","CLOSED"),
    ("LN0010","APP0011",450000,450000,11.8,36,"2026-07-03","ACTIVE"),
    ("LN0011","APP0012",300000,300000,12.2,24,"2026-07-05","ACTIVE"),
    ("LN0013","APP0013",750000,750000,13.5,36,"2026-08-11","ACTIVE"),  # fraud
    ("LN0014","APP0014",800000,800000,13.5,36,"2026-08-11","ACTIVE"),
    ("LN0015","APP0015",700000,700000,13.5,36,"2026-08-12","ACTIVE"),
    ("LN0016","APP0016",650000,650000,13.5,36,"2026-08-12","ACTIVE"),
    ("LN0017","APP0024",200000,200000,12.0,12,"2026-08-19","ACTIVE"),
    ("LN0018","APP0003",0,0,0,0,"2026-06-12","ACTIVE"),  # placeholder fix below
]
# Remove LN0018 placeholder - replace with correct
loan_map_corrected=[
    ("LN0001","APP0001",500000,500000,11.5,36,"2026-06-03","ACTIVE"),
    ("LN0002","APP0002",300000,300000,12.0,24,"2026-06-07","ACTIVE"),
    ("LN0003","APP0003",800000,800000,10.8,60,"2026-06-12","ACTIVE"),
    ("LN0004","APP0004",1200000,1200000,11.0,48,"2026-06-14","ACTIVE"),
    ("LN0005","APP0006",600000,600000,12.5,24,"2026-06-20","ACTIVE"),
    ("LN0006","APP0007",250000,250000,13.0,18,"2026-06-22","ACTIVE"),
    ("LN0007","APP0008",900000,900000,11.2,36,"2026-06-24","ACTIVE"),
    ("LN0008","APP0009",350000,350000,12.8,24,"2026-06-27","ACTIVE"),
    ("LN0009","APP0010",200000,200000,14.0,12,"2026-06-30","CLOSED"),
    ("LN0010","APP0011",450000,450000,11.8,36,"2026-07-03","ACTIVE"),
    ("LN0011","APP0012",300000,300000,12.2,24,"2026-07-05","ACTIVE"),
    ("LN0012","APP0013",750000,750000,13.5,36,"2026-08-11","ACTIVE"),
    ("LN0013","APP0014",800000,800000,13.5,36,"2026-08-11","ACTIVE"),
    ("LN0014","APP0015",700000,700000,13.5,36,"2026-08-12","ACTIVE"),
    ("LN0015","APP0016",650000,650000,13.5,36,"2026-08-12","ACTIVE"),
    ("LN0016","APP0024",200000,200000,12.0,12,"2026-08-19","ACTIVE"),
    ("LN0017","APP0001",400000,400000,11.5,24,"2026-06-03","CLOSED"),  # second loan for C001 not needed; remove
]
# Final: 16 loans (unique application_id constraint: one loan per application)
loan_final=[
    ("LN0001","APP0001",500000,500000,11.5,36,"2026-06-03","ACTIVE"),
    ("LN0002","APP0002",300000,300000,12.0,24,"2026-06-07","ACTIVE"),
    ("LN0003","APP0003",800000,800000,10.8,60,"2026-06-12","ACTIVE"),
    ("LN0004","APP0004",1200000,1200000,11.0,48,"2026-06-14","ACTIVE"),
    ("LN0005","APP0006",600000,600000,12.5,24,"2026-06-20","ACTIVE"),
    ("LN0006","APP0007",250000,250000,13.0,18,"2026-06-22","ACTIVE"),
    ("LN0007","APP0008",900000,900000,11.2,36,"2026-06-24","ACTIVE"),
    ("LN0008","APP0009",350000,350000,12.8,24,"2026-06-27","ACTIVE"),
    ("LN0009","APP0010",200000,200000,14.0,12,"2026-06-30","CLOSED"),
    ("LN0010","APP0011",450000,450000,11.8,36,"2026-07-03","ACTIVE"),
    ("LN0011","APP0012",300000,300000,12.2,24,"2026-07-05","ACTIVE"),
    ("LN0012","APP0013",750000,750000,13.5,36,"2026-08-11","ACTIVE"),
    ("LN0013","APP0014",800000,800000,13.5,36,"2026-08-11","ACTIVE"),
    ("LN0014","APP0015",700000,700000,13.5,36,"2026-08-12","ACTIVE"),
    ("LN0015","APP0016",650000,650000,13.5,36,"2026-08-12","ACTIVE"),
    ("LN0016","APP0024",200000,200000,12.0,12,"2026-08-19","ACTIVE"),
]
lines.append("INSERT INTO loans (loan_id, application_id, loan_account_ref, sanctioned_amount, disbursed_amount, interest_rate, tenure_months, disbursement_date, loan_status) VALUES")
loan_vals=[]
for ln, app_ref, sanc, disb, rate, tenure, disb_date, status in loan_final:
    loan_vals.append(f"  ('{loans[ln]}', '{apps[app_ref]}', '{ln}', {sanc}, {disb}, {rate}, {tenure}, '{disb_date}', '{status}')")
lines.append(",\n".join(loan_vals) + ";\n")

# Guarantor links
lines.append("-- Loan guarantors — G005 reused across fraud apps")
lg_links=[
    ("APP0001","G001"),("APP0003","G002"),("APP0008","G003"),("APP0009","G004"),
    ("APP0013","G005"),("APP0014","G005"),("APP0015","G005"),("APP0016","G005"),("APP0021","G005"),
    ("APP0017","G006"),("APP0018","G005"),
]
lines.append("INSERT INTO loan_guarantors (application_id, guarantor_id, relationship_type) VALUES")
lg_vals=[f"  ('{apps[app]}', '{guarantors[g]}', 'GUARANTOR')" for app,g in lg_links]
lines.append(",\n".join(lg_vals) + ";\n")

# Payments — normal on-time + fraud bounces
lines.append("-- Payments — normal on-time vs fraud bounces/delays")
pay_vals=[]
pid=1
def add_pay(loan_ref, date, amount, method, status, dpd):
    global pid
    p_id = uid(f'PAY{pid:04d}')
    pid+=1
    trh = h(f'txn-{p_id}')
    return f"  ('{p_id}', '{loans[loan_ref]}', '{date}', {amount}, '{method}', '{status}', {dpd}, 'TXN{pid:05d}', '{trh}')"
# Normal: 3 on-time payments per active loan (first 6 loans)
for ln in ["LN0001","LN0002","LN0003","LN0004","LN0005","LN0006"]:
    for m in [1,2,3]:
        amt = {"LN0001":15000,"LN0002":14000,"LN0003":18000,"LN0004":30000,"LN0005":27000,"LN0006":15000}[ln]
        pay_vals.append(add_pay(ln, f"2026-{7+m:02d}-05", amt, "NACH", "SUCCESS", 0))
# One missed for LN0010
pay_vals.append(add_pay("LN0010", "2026-08-05", 14500, "NACH", "FAILED", 12))
pay_vals.append(add_pay("LN0010", "2026-08-10", 14500, "UPI", "SUCCESS", 10))
# Fraud loans: bounces + delays
for ln in ["LN0012","LN0013","LN0014","LN0015"]:
    pay_vals.append(add_pay(ln, "2026-08-15", 22000, "NACH", "FAILED", 5))
    pay_vals.append(add_pay(ln, "2026-08-18", 22000, "NACH", "FAILED", 8))
    pay_vals.append(add_pay(ln, "2026-08-20", 11000, "UPI", "PARTIAL", 6))
lines.append("INSERT INTO payments (payment_id, loan_id, payment_date, amount, payment_method, payment_status, days_past_due, transaction_ref, transaction_hash) VALUES")
lines.append(",\n".join(pay_vals) + ";\n")

# Repayment behaviour
lines.append("-- Repayment behaviour (derived)")
rb_vals=[]
rb_data=[
    ("LN0001",0.5,0,2,0,0,1.02,88),
    ("LN0002",0.2,0,3,0,0,1.05,92),
    ("LN0003",1.1,0,1,0,0,0.98,85),
    ("LN0004",0.0,0,3,0,0,1.1,95),
    ("LN0010",8.5,1,0,0,1,0.65,42),
    ("LN0012",6.2,0,0,2,2,0.45,18),
    ("LN0013",7.0,0,0,3,2,0.40,12),
    ("LN0014",6.8,0,0,2,2,0.42,15),
    ("LN0015",5.9,0,0,2,2,0.48,20),
]
for ln, avg_delay, missed, early, partial, bounces, vel, score in rb_data:
    rb_id=uid(f'RB-{ln}')
    rb_vals.append(f"  ('{rb_id}', '{loans[ln]}', {avg_delay}, {missed}, {early}, {partial}, {bounces}, {vel}, {score}, '2026-08-21 10:00:00+00')")
lines.append("INSERT INTO repayment_behaviour (behaviour_id, loan_id, avg_payment_delay_days, missed_payment_count, early_payment_count, partial_payment_count, bounce_count, payment_velocity, behaviour_score, calculated_at) VALUES")
lines.append(",\n".join(rb_vals) + ";\n")

# Risk scores — history preserved
lines.append("-- Risk scores — historical (never overwritten)")
rs_vals=[]
# Normal customers stable low
for cust in ["C001","C002","C003","C004","C005","C006","C007","C008","C009","C010","C011","C012"]:
    base = random.uniform(12,28)
    for idx, d in enumerate(["2026-06-01","2026-07-01","2026-08-01","2026-08-15"]):
        score = round(base + random.uniform(-3,3) + idx*0.5, 2)
        score = max(5, min(35, score))
        level = "LOW" if score <30 else "MEDIUM"
        rs_vals.append(f"  ('{uid(f'RS-{cust}-{d}')}', 'CUSTOMER', '{customers[cust]}', {score}, {round(score/100,4)}, '{level}', 'v2.1.0', '{d} 10:00:00+00', '{{\"model\":\"v2.1.0\",\"features\":{{\"income_band\":\"MIDDLE\"}}}}')")
# Fraud customers escalating
fraud_scores={
    "C013": [31,46,67,89],
    "C014": [28,44,71,91],
    "C015": [35,52,74,93],
    "C016": [30,48,69,87],
    "C017": [25,38,58,72],
    "C018": [22,35,55,70],
    "C019": [20,32,50,68],
    "C020": [18,30,48,65],
}
for cust, scores in fraud_scores.items():
    for s, d in zip(scores, ["2026-06-01","2026-07-01","2026-08-01","2026-08-15"]):
        level = "LOW" if s<30 else "MEDIUM" if s<60 else "HIGH" if s<80 else "CRITICAL"
        rs_vals.append(f"  ('{uid(f'RS-{cust}-{d}')}', 'CUSTOMER', '{customers[cust]}', {s}, {round(s/100,4)}, '{level}', 'v2.1.0', '{d} 10:00:00+00', '{{\"model\":\"v2.1.0\",\"fraud_cluster\":\"F-1001\"}}')")
# Dealer risk
rs_vals.append(f"  ('{uid('RS-DL003-2026-08-15')}', 'DEALER', '{dealers['DL003']}', 88.5, 0.885, 'CRITICAL', 'v2.1.0', '2026-08-15 10:00:00+00', '{{\"dealer_apps\":8}}')")
# Device risk
rs_vals.append(f"  ('{uid('RS-D004-2026-08-15')}', 'DEVICE', '{devices['D004']}', 92.0, 0.92, 'CRITICAL', 'v2.1.0', '2026-08-15 10:00:00+00', '{{\"shared_customers\":4}}')")
lines.append("INSERT INTO risk_scores (risk_score_id, entity_type, entity_id, risk_score, fraud_probability, risk_level, model_version, calculated_at, feature_snapshot) VALUES")
lines.append(",\n".join(rs_vals) + ";\n")

# Fraud signals
lines.append("-- Fraud signals")
sig_vals=[]
sigs=[
    ("CUSTOMER", "C013", "SHARED_DEVICE", "CRITICAL", 92, 0.95, "Device D004 shared across 4 customers in 48h"),
    ("CUSTOMER", "C014", "SHARED_DEVICE", "CRITICAL", 91, 0.94, "Device D004 shared"),
    ("CUSTOMER", "C015", "SHARED_DEVICE", "HIGH", 88, 0.90, "Device D004 shared + bank reuse"),
    ("CUSTOMER", "C013", "SHARED_BANK_ACCOUNT", "CRITICAL", 90, 0.93, "Bank B007 reused across 4 customers"),
    ("CUSTOMER", "C017", "SHARED_BANK_ACCOUNT", "HIGH", 82, 0.85, "Bank B009 shared"),
    ("CUSTOMER", "C013", "SHARED_ADDRESS", "HIGH", 80, 0.82, "Address A013 shared"),
    ("CUSTOMER", "C013", "RAPID_APPLICATION_BURST", "CRITICAL", 89, 0.91, "4 applications via DL003 in 24h window"),
    ("DEALER", "DL003", "UNUSUAL_DEALER_CLUSTER", "CRITICAL", 94, 0.96, "8 applications in 5 days vs baseline 2/month"),
    ("DEVICE", "D004", "DEVICE_VELOCITY", "CRITICAL", 93, 0.95, "4 distinct customers on same device in 48h"),
    ("CUSTOMER", "C013", "MULTIPLE_BANK_ACCOUNT_LINK", "MEDIUM", 65, 0.70, "Secondary bank link via shared account"),
    ("CUSTOMER", "C012", "UNUSUAL_REPAYMENT_PATTERN", "LOW", 35, 0.40, "Single late payment - not cluster"),
    ("LOAN", "LN0012", "UNUSUAL_REPAYMENT_PATTERN", "HIGH", 85, 0.88, "2 bounces + partial payment"),
]
for idx,(etype, eref, stype, sev, score, conf, desc) in enumerate(sigs):
    eid = customers[eref] if etype=="CUSTOMER" else dealers[eref] if etype=="DEALER" else devices[eref] if etype=="DEVICE" else loans[eref] if etype=="LOAN" else customers[eref]
    sig_id=uid(f'SIG{idx:03d}')
    lines_fake = f"  ('{sig_id}', '{etype}', '{eid}', '{stype}', '{sev}', {score}, {conf}, {sql_str(desc)}, '2026-08-12 10:00:00+00', NULL, '{{\"evidence\":\"auto\"}}')"
    sig_vals.append(lines_fake)
lines.append("INSERT INTO fraud_signals (signal_id, entity_type, entity_id, signal_type, severity, score, confidence, description, detected_at, expires_at, evidence) VALUES")
lines.append(",\n".join(sig_vals) + ";\n")

# Predictions
lines.append("-- Predictions")
pred_vals=[]
for cust in ["C001","C002","C003","C013","C014","C015","C016","C017"]:
    score = 0.12 if cust in ("C001","C002","C003") else 0.91 if cust in ("C013","C014","C015") else 0.82
    label = "FRAUD" if score>0.5 else "LEGIT"
    etype="CUSTOMER"
    eid=customers[cust]
    mid=models["MODEL2"]
    pred_vals.append(f"  ('{uid(f'PRED-{cust}')}', '{mid}', '{etype}', '{eid}', 'FRAUD_CLASSIFICATION', {score}, '{label}', '{{\"model\":\"v2.1.0\"}}', '2026-08-15 11:00:00+00')")
lines.append("INSERT INTO predictions (prediction_id, model_id, entity_type, entity_id, prediction_type, prediction_score, prediction_label, feature_snapshot, predicted_at) VALUES")
lines.append(",\n".join(pred_vals) + ";\n")

out['003_lending_data.sql'] = "\n".join(lines)

# ============ 004_relationship_network.sql ============
lines=[]
lines.append("-- =============================================================================\n-- 004_relationship_network.sql — Entity relationships + fraud clusters/members\n-- =============================================================================\n")

# Fraud clusters
lines.append("-- Fraud clusters — F-1001 (HIGH) and F-1002 (MEDIUM)")
lines.append("INSERT INTO fraud_clusters (cluster_id, cluster_ref, cluster_type, risk_score, member_count, cluster_status, detected_at, last_updated_at, metadata) VALUES")
lines.append(f"  ('{clusters['F-1001']}', 'F-1001', 'MIXED_ENTITY_CLUSTER', 91.5, 12, 'ACTIVE', '2026-08-12 10:00:00+00', '2026-08-21 10:00:00+00', '{{\"description\":\"Dharavi quick-loan ring: 4 customers share device+mobile+bank+address via DL003/G005\",\"dealer\":\"DL003\"}}'),")
lines.append(f"  ('{clusters['F-1002']}', 'F-1002', 'MIXED_ENTITY_CLUSTER', 68.0, 8, 'UNDER_REVIEW', '2026-08-15 10:00:00+00', '2026-08-20 10:00:00+00', '{{\"description\":\"Secondary ring linked via B007/B009 bridge\",\"dealer\":\"DL003/DL006\"}}');\n")

# Fraud cluster members — F-1001: C013,C014,C015,C016 + D004,D009 + M002 + B007 + DL003 + G005 + A013 + IP001
lines.append("-- Fraud cluster members — F-1001 (12) + F-1002 (8)")
fcm_vals=[]
# F-1001
for eref, etype in [("C013","CUSTOMER"),("C014","CUSTOMER"),("C015","CUSTOMER"),("C016","CUSTOMER"),
                     ("D004","DEVICE"),("D009","DEVICE"),("M002","MOBILE"),("B007","BANK_ACCOUNT"),
                     ("DL003","DEALER"),("G005","GUARANTOR"),("A013","ADDRESS"),("IP001","IP")]:
    eid = customers[eref] if etype=="CUSTOMER" else devices[eref] if etype=="DEVICE" else mobiles[eref] if etype=="MOBILE" else banks[eref] if etype=="BANK_ACCOUNT" else dealers[eref] if etype=="DEALER" else guarantors[eref] if etype=="GUARANTOR" else addresses[eref] if etype=="ADDRESS" else ips[eref]
    fcm_vals.append(f"  ('{uid(f'FCM-F1001-{eref}')}', '{clusters['F-1001']}', '{etype}', '{eid}', 0.92, '2026-08-12 10:00:00+00', NULL)")
# F-1002
for eref, etype in [("C017","CUSTOMER"),("C018","CUSTOMER"),("C019","CUSTOMER"),("C020","CUSTOMER"),
                     ("B009","BANK_ACCOUNT"),("D009","DEVICE"),("M009","MOBILE"),("DL003","DEALER")]:
    eid = customers[eref] if etype=="CUSTOMER" else banks[eref] if etype=="BANK_ACCOUNT" else devices[eref] if etype=="DEVICE" else mobiles[eref] if etype=="MOBILE" else dealers[eref]
    fcm_vals.append(f"  ('{uid(f'FCM-F1002-{eref}')}', '{clusters['F-1002']}', '{etype}', '{eid}', 0.75, '2026-08-15 10:00:00+00', NULL)")
lines.append("INSERT INTO fraud_cluster_members (member_id, cluster_id, entity_type, entity_id, membership_score, joined_at, left_at) VALUES")
lines.append(",\n".join(fcm_vals) + ";\n")

# Entity relationships — core swarm graph
lines.append("-- Entity relationships — bidirectional swarm graph (shared device/mobile/bank/address/guarantor/ip/dealer)")
er_vals=[]
def add_er(src_type, src_ref, tgt_type, tgt_ref, rel_type, strength, conf, evc=2):
    s_id = customers[src_ref] if src_type=="CUSTOMER" else devices[src_ref] if src_type=="DEVICE" else mobiles[src_ref] if src_type=="MOBILE" else banks[src_ref] if src_type=="BANK_ACCOUNT" else dealers[src_ref] if src_type=="DEALER" else guarantors[src_ref] if src_type=="GUARANTOR" else ips[src_ref] if src_type=="IP" else addresses[src_ref] if src_type=="ADDRESS" else None
    t_id = customers[tgt_ref] if tgt_type=="CUSTOMER" else devices[tgt_ref] if tgt_type=="DEVICE" else mobiles[tgt_ref] if tgt_type=="MOBILE" else banks[tgt_ref] if tgt_type=="BANK_ACCOUNT" else dealers[tgt_ref] if tgt_type=="DEALER" else guarantors[tgt_ref] if tgt_type=="GUARANTOR" else ips[tgt_ref] if tgt_type=="IP" else addresses[tgt_ref] if tgt_type=="ADDRESS" else customers[tgt_ref]
    er_id=uid(f'ER-{src_ref}-{tgt_ref}-{rel_type}')
    return f"  ('{er_id}', '{src_type}', '{s_id}', '{tgt_type}', '{t_id}', '{rel_type}', {strength}, {conf}, {evc}, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{{\"auto\":true}}')"

# Customer->Device shared
er_vals.append(add_er("CUSTOMER","C013","DEVICE","D004","SHARED_DEVICE",0.98,0.99,4))
er_vals.append(add_er("CUSTOMER","C014","DEVICE","D004","SHARED_DEVICE",0.98,0.99,4))
er_vals.append(add_er("CUSTOMER","C015","DEVICE","D004","SHARED_DEVICE",0.97,0.98,4))
er_vals.append(add_er("CUSTOMER","C019","DEVICE","D004","SHARED_DEVICE",0.85,0.88,2))
er_vals.append(add_er("CUSTOMER","C016","DEVICE","D009","SHARED_DEVICE",0.96,0.97,3))
er_vals.append(add_er("CUSTOMER","C017","DEVICE","D009","SHARED_DEVICE",0.95,0.96,3))
er_vals.append(add_er("CUSTOMER","C018","DEVICE","D009","SHARED_DEVICE",0.94,0.95,2))
er_vals.append(add_er("CUSTOMER","C020","DEVICE","D009","SHARED_DEVICE",0.90,0.92,2))
# Customer->Mobile shared
er_vals.append(add_er("CUSTOMER","C013","MOBILE","M002","SHARED_MOBILE",0.99,0.99,4))
er_vals.append(add_er("CUSTOMER","C014","MOBILE","M002","SHARED_MOBILE",0.99,0.99,4))
er_vals.append(add_er("CUSTOMER","C015","MOBILE","M002","SHARED_MOBILE",0.85,0.87,2))
er_vals.append(add_er("CUSTOMER","C017","MOBILE","M009","SHARED_MOBILE",0.92,0.93,2))
er_vals.append(add_er("CUSTOMER","C018","MOBILE","M009","SHARED_MOBILE",0.92,0.93,2))
# Customer->Bank shared
er_vals.append(add_er("CUSTOMER","C013","BANK_ACCOUNT","B007","SHARED_BANK_ACCOUNT",0.97,0.98,4))
er_vals.append(add_er("CUSTOMER","C014","BANK_ACCOUNT","B007","SHARED_BANK_ACCOUNT",0.97,0.98,4))
er_vals.append(add_er("CUSTOMER","C015","BANK_ACCOUNT","B007","SHARED_BANK_ACCOUNT",0.96,0.97,4))
er_vals.append(add_er("CUSTOMER","C016","BANK_ACCOUNT","B007","SHARED_BANK_ACCOUNT",0.90,0.92,1))
er_vals.append(add_er("CUSTOMER","C019","BANK_ACCOUNT","B007","SHARED_BANK_ACCOUNT",0.80,0.82,1))
er_vals.append(add_er("CUSTOMER","C017","BANK_ACCOUNT","B009","SHARED_BANK_ACCOUNT",0.93,0.94,2))
er_vals.append(add_er("CUSTOMER","C018","BANK_ACCOUNT","B009","SHARED_BANK_ACCOUNT",0.93,0.94,2))
# Customer->Address shared
er_vals.append(add_er("CUSTOMER","C013","ADDRESS","A013","SHARED_ADDRESS",0.94,0.95,3))
er_vals.append(add_er("CUSTOMER","C014","ADDRESS","A013","SHARED_ADDRESS",0.94,0.95,3))
er_vals.append(add_er("CUSTOMER","C015","ADDRESS","A013","SHARED_ADDRESS",0.93,0.94,2))
# Customer->Guarantor shared
er_vals.append(add_er("CUSTOMER","C013","GUARANTOR","G005","SHARED_GUARANTOR",0.96,0.97,3))
er_vals.append(add_er("CUSTOMER","C014","GUARANTOR","G005","SHARED_GUARANTOR",0.96,0.97,3))
er_vals.append(add_er("CUSTOMER","C015","GUARANTOR","G005","SHARED_GUARANTOR",0.95,0.96,3))
er_vals.append(add_er("CUSTOMER","C016","GUARANTOR","G005","SHARED_GUARANTOR",0.90,0.92,1))
# Customer->Dealer
er_vals.append(add_er("CUSTOMER","C013","DEALER","DL003","SAME_DEALER",0.92,0.94,2))
er_vals.append(add_er("CUSTOMER","C014","DEALER","DL003","SAME_DEALER",0.92,0.94,2))
er_vals.append(add_er("CUSTOMER","C015","DEALER","DL003","SAME_DEALER",0.91,0.93,2))
er_vals.append(add_er("CUSTOMER","C016","DEALER","DL003","SAME_DEALER",0.90,0.92,1))
er_vals.append(add_er("CUSTOMER","C017","DEALER","DL003","SAME_DEALER",0.88,0.90,1))
# Device->IP
er_vals.append(add_er("DEVICE","D004","IP","IP001","SAME_IP",0.89,0.90,3))
er_vals.append(add_er("DEVICE","D009","IP","IP001","SAME_IP",0.87,0.88,2))
# Customer->Customer suspicious links
er_vals.append(add_er("CUSTOMER","C013","CUSTOMER","C014","SUSPICIOUS_LINK",0.96,0.97,5))
er_vals.append(add_er("CUSTOMER","C013","CUSTOMER","C015","SUSPICIOUS_LINK",0.94,0.95,4))
er_vals.append(add_er("CUSTOMER","C014","CUSTOMER","C015","SUSPICIOUS_LINK",0.93,0.94,4))
er_vals.append(add_er("CUSTOMER","C017","CUSTOMER","C018","SUSPICIOUS_LINK",0.85,0.87,2))
# Dealer->Device
er_vals.append(add_er("DEALER","DL003","DEVICE","D004","SHARED_DEALER_DEVICE",0.88,0.89,3))

lines.append("INSERT INTO entity_relationships (relationship_id, source_entity_type, source_entity_id, target_entity_type, target_entity_id, relationship_type, strength, confidence, evidence_count, first_seen, last_seen, metadata) VALUES")
lines.append(",\n".join(er_vals) + ";\n")

# Update fraud_clusters member_count to match actual (trigger not auto)
lines.append("-- Fix member_count (already set correctly above; no update needed)")
lines.append("SELECT '004_relationship_network loaded' AS status;\n")

out['004_relationship_network.sql'] = "\n".join(lines)

# ============ 005_fraud_scenarios.sql ============
lines=[]
lines.append("-- =============================================================================\n-- 005_fraud_scenarios.sql — Alerts, investigations, application events, audit logs\n-- =============================================================================\n")

# Fraud alerts
lines.append("-- Fraud alerts (6)")
alert_rows=[
    ("ALT-1001","CUSTOMER","C013","F-1001","EMERGING_FRAUD_NETWORK","CRITICAL",91,"OPEN","2026-08-12 11:00:00+00"),
    ("ALT-1002","CLUSTER","F-1001","F-1001","HIGH_RISK_DEVICE_CLUSTER","CRITICAL",93,"OPEN","2026-08-12 11:30:00+00"),
    ("ALT-1003","CUSTOMER","C017","F-1002","SHARED_BANK_ACCOUNT_NETWORK","HIGH",72,"OPEN","2026-08-15 09:00:00+00"),
    ("ALT-1004","DEALER","DL003","F-1001","DEALER_ANOMALY","CRITICAL",94,"IN_INVESTIGATION","2026-08-13 10:00:00+00"),
    ("ALT-1005","CUSTOMER","C015",None,"RAPID_APPLICATION_CLUSTER","HIGH",85,"OPEN","2026-08-16 10:00:00+00"),
    ("ALT-1006","DEVICE","D004","F-1001","BEHAVIOURAL_ANOMALY","HIGH",88,"OPEN","2026-08-14 09:00:00+00"),
]
alert_vals=[]
for ref, etype, eref, clus, atype, sev, score, status, gen_at in alert_rows:
    eid = None
    if etype=="CUSTOMER": eid=customers[eref]
    elif etype=="CLUSTER": eid=clusters[eref]
    elif etype=="DEALER": eid=dealers[eref]
    elif etype=="DEVICE": eid=devices[eref]
    else: eid=customers[eref]
    cid = clusters[clus] if clus else "NULL"
    cid_sql = f"'{cid}'" if clus else "NULL"
    alert_vals.append(f"  ('{uid(ref)}', '{ref}', '{etype}', '{eid}', {cid_sql}, '{atype}', '{sev}', {score}, '{status}', '{gen_at}', NULL, '{{\"auto\":true}}')")
lines.append("INSERT INTO fraud_alerts (alert_id, alert_ref, entity_type, entity_id, cluster_id, alert_type, severity, risk_score, alert_status, generated_at, resolved_at, evidence) VALUES")
lines.append(",\n".join(alert_vals) + ";\n")

# Investigations
lines.append("-- Investigations (4)")
lines.append("INSERT INTO investigations (investigation_id, alert_id, investigator_ref, investigation_status, priority, notes, opened_at, closed_at) VALUES")
lines.append(f"  ('{invs['INV0001']}', '{uid('ALT-1001')}', 'investigator_01', 'IN_PROGRESS', 'URGENT', 'Field visit scheduled to Dharavi address A013. Device D004 seized for review.', '2026-08-13 09:00:00+00', NULL),")
lines.append(f"  ('{invs['INV0002']}', '{uid('ALT-1004')}', 'investigator_02', 'IN_PROGRESS', 'URGENT', 'Dealer DL003 transaction audit — 8 apps in 5 days.', '2026-08-14 10:00:00+00', NULL),")
lines.append(f"  ('{invs['INV0003']}', '{uid('ALT-1003')}', 'investigator_01', 'OPEN', 'HIGH', 'Secondary ring review — possible bridge via B007.', '2026-08-16 09:00:00+00', NULL),")
lines.append(f"  ('{invs['INV0004']}', '{uid('ALT-1002')}', 'investigator_03', 'CLOSED', 'HIGH', 'Confirmed fraud cluster F-1001. Recommended block on D004/M002/B007.', '2026-08-12 12:00:00+00', '2026-08-20 16:00:00+00');\n")

# Investigation actions
lines.append("-- Investigation actions (audit trail)")
lines.append("INSERT INTO investigation_actions (investigation_id, action_type, performed_by, notes, performed_at) VALUES")
lines.append(f"  ('{invs['INV0001']}', 'ASSIGNED', 'manager_01', 'Assigned to investigator_01', '2026-08-13 09:05:00+00'),")
lines.append(f"  ('{invs['INV0001']}', 'EVIDENCE_ADDED', 'investigator_01', 'Added device fingerprint D004 evidence', '2026-08-13 14:00:00+00'),")
lines.append(f"  ('{invs['INV0001']}', 'FIELD_VISIT', 'investigator_01', 'Visited A013 — 4 customers at same chawl', '2026-08-15 11:00:00+00'),")
lines.append(f"  ('{invs['INV0002']}', 'ASSIGNED', 'manager_01', 'Dealer audit assigned', '2026-08-14 10:05:00+00'),")
lines.append(f"  ('{invs['INV0002']}', 'CONTACTED_DEALER', 'investigator_02', 'Dealer principal unavailable', '2026-08-16 09:00:00+00'),")
lines.append(f"  ('{invs['INV0004']}', 'CASE_CLOSED', 'investigator_03', 'Cluster confirmed fraud', '2026-08-20 16:00:00+00');\n")

# Application events — burst + normal
lines.append("-- Application events — rapid burst + normal activity")
evt_vals=[]
def evt(app_ref, cust_ref, dev_ref, ip_ref, loc_ref, etype, ts):
    eid=uid(f'EVT-{app_ref}-{etype}-{ts}')
    app_id=apps[app_ref] if app_ref else "NULL"
    app_sql=f"'{app_id}'" if app_ref else "NULL"
    cust_id=customers[cust_ref] if cust_ref else "NULL"
    cust_sql=f"'{cust_id}'" if cust_ref else "NULL"
    dev_id=devices[dev_ref] if dev_ref else "NULL"
    dev_sql=f"'{dev_id}'" if dev_ref else "NULL"
    ip_id=ips[ip_ref] if ip_ref else "NULL"
    ip_sql=f"'{ip_id}'" if ip_ref else "NULL"
    loc_id=locs[loc_ref] if loc_ref else "NULL"
    loc_sql=f"'{loc_id}'" if loc_ref else "NULL"
    return f"  ('{eid}', {app_sql}, {cust_sql}, {dev_sql}, {ip_sql}, {loc_sql}, '{etype}', '{ts}', '{{\"source\":\"seed\"}}')"
# Normal scattered
evt_vals.append(evt("APP0001","C001","D001","IP002","LOC001","APPLICATION_STARTED","2026-06-01 09:50:00+00"))
evt_vals.append(evt("APP0001","C001","D001","IP002","LOC001","APPLICATION_SUBMITTED","2026-06-01 10:00:00+00"))
evt_vals.append(evt("APP0002","C002","D002","IP003","LOC002","APPLICATION_SUBMITTED","2026-06-05 11:00:00+00"))
# Fraud burst tight window same device+IP
for app_ref,cust in [("APP0013","C013"),("APP0014","C014"),("APP0015","C015")]:
    evt_vals.append(evt(app_ref,cust,"D004","IP001","LOC006","APPLICATION_STARTED","2026-08-10 09:00:00+00"))
    evt_vals.append(evt(app_ref,cust,"D004","IP001","LOC006","APPLICATION_SUBMITTED","2026-08-10 09:15:00+00"))
    evt_vals.append(evt(app_ref,cust,"D004","IP001","LOC006","DEVICE_CHANGED","2026-08-10 09:20:00+00"))
evt_vals.append(evt("APP0016","C016","D009","IP001","LOC006","APPLICATION_SUBMITTED","2026-08-11 09:00:00+00"))
evt_vals.append(evt("APP0017","C017","D009","IP001","LOC006","BANK_ACCOUNT_CHANGED","2026-08-12 10:05:00+00"))
evt_vals.append(evt("APP0021","C013","D004","IP001","LOC006","APPLICATION_EDITED","2026-08-15 09:05:00+00"))
evt_vals.append(evt("APP0005","C005","D006","IP004","LOC004","LOCATION_CHANGED","2026-06-15 10:30:00+00"))
lines.append("INSERT INTO application_events (event_id, application_id, customer_id, device_id, ip_id, location_id, event_type, event_timestamp, metadata) VALUES")
lines.append(",\n".join(evt_vals) + ";\n")

# Audit logs
lines.append("-- Audit logs")
lines.append("INSERT INTO audit_logs (user_ref, action, entity_type, entity_id, old_value, new_value) VALUES")
lines.append(f"  ('system', 'CREATE', 'CLUSTER', '{clusters['F-1001']}', NULL, '{{\"cluster_ref\":\"F-1001\",\"risk_score\":91.5}}'),")
lines.append(f"  ('investigator_01', 'UPDATE', 'CUSTOMER', '{customers['C013']}', '{{\"status\":\"ACTIVE\"}}', '{{\"status\":\"SUSPECT\"}}'),")
lines.append(f"  ('system', 'CREATE', 'ALERT', '{uid('ALT-1001')}', NULL, '{{\"alert_ref\":\"ALT-1001\",\"severity\":\"CRITICAL\"}}'),")
lines.append(f"  ('manager_01', 'APPROVE', 'INVESTIGATION', '{invs['INV0004']}', '{{\"status\":\"IN_PROGRESS\"}}', '{{\"status\":\"CLOSED\"}}');\n")

out['005_fraud_scenarios.sql'] = "\n".join(lines)

# Write files
os.makedirs(SEED_DIR, exist_ok=True)
for fname, content in out.items():
    path=os.path.join(SEED_DIR, fname)
    with open(path,'w',encoding='utf-8',newline='\n') as f:
        f.write(content)
    print(f"Wrote {fname} ({len(content)} bytes)")
print("Done")

