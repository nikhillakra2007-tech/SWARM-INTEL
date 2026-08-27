-- =============================================================================
-- 001_reference_data.sql — Reference entities (addresses, dealers, guarantors, mobiles, devices, IPs, locations, bank accounts, models)
-- All values synthetic / hashed. No real PII.
-- =============================================================================

-- Addresses (20)
INSERT INTO addresses (address_id, address_hash, address_text, city, district, state, pincode, latitude, longitude) VALUES
  ('5f51108b-57bc-5f5f-8a13-48c7ebfa74f2', '526b04e189a75aedbeda943d248cd3c708a284c3091822ea273e7a38ed46dedb', 'Flat 302, Sunshine Apts, Bandra West', 'Mumbai', 'Mumbai', 'Maharashtra', '400050', 19.0596, 72.8295),
  ('3e6a348b-a1cb-550a-b3ab-40bfcc787571', '8ac1965640c389e590b4ddc5280238a72b2cff05cecffbdc7e637d980f69f206', '12/4 80 Feet Road, Koramangala', 'Bengaluru', 'Bengaluru', 'Karnataka', '560034', 12.9352, 77.6245),
  ('087921d8-4ae6-5185-8018-fade440bf91a', '1c9d08ea9732d434999e204f8e673fbb2b1284c1a2e0d2a9525d6affc8c9323b', 'Block C, Inner Circle, CP', 'New Delhi', 'New Delhi', 'Delhi', '110001', 28.6315, 77.2167),
  ('689b840c-21ba-58af-bd3f-559b7e655328', '25ad63527d3e79bcb26eb82feaefc258a062e17143fdae93c5a43a9a08d3821c', 'AE-123 Sector 1, Salt Lake', 'Kolkata', 'Kolkata', 'West Bengal', '700091', 22.5804, 88.412),
  ('aa9729f5-9310-5751-8a02-e6ef2216207c', 'a8e6986e3179f8ed062d8adba8bc7fc8164de570c818681947b125cc97f59ee8', 'Road No.12, House 44, Banjara Hills', 'Hyderabad', 'Hyderabad', 'Telangana', '500034', 17.4156, 78.4348),
  ('39c1b460-6d67-515f-9436-eb8290639e98', '030915ef9ef098aadb2f77938168d3fdef259750e8e9dde0ff062950f962ff2e', 'Marol Naka, 5th Lane, Andheri East', 'Mumbai', 'Mumbai', 'Maharashtra', '400069', 19.1136, 72.8697),
  ('5a46b5ef-5426-5db7-9033-7d4dcbfa5647', '760bedbee3a7e0aac021a2b88bc859e229eca9235626934c270e2e217d142da7', 'ITPL Road, Bldg 7, Whitefield', 'Bengaluru', 'Bengaluru', 'Karnataka', '560066', 12.9698, 77.75),
  ('64f5a5ab-f354-53e0-8b2e-6bcc43626f01', '9306e6d9b167a74695dd9174318343d3043aa9971d2adb074566e534b4202dd8', 'Sector 10, Pocket 2, Dwarka', 'New Delhi', 'New Delhi', 'Delhi', '110075', 28.5921, 77.046),
  ('524b47e7-684f-5135-a032-e53be5e05102', 'e473543f8134f1bd075752ff7813dfac94f0d405772bc057c86af01710919b8a', '12 Park Street, Floor 3', 'Kolkata', 'Kolkata', 'West Bengal', '700016', 22.5532, 88.348),
  ('b95b59e9-197f-56f6-ae5b-8b3b46854bc1', 'de9a03a500d1318d5250a3583ee826fcf660fc80996c4b37f1f65c8f02410be7', 'DLF Cyber City, Block A, Gachibowli', 'Hyderabad', 'Hyderabad', 'Telangana', '500032', 17.44, 78.348),
  ('949269df-5cb0-5f9b-9b65-b063e3af076d', '16a0eb9ca2776e683b253c2eb52416b2ef36e86c3d10a08a37316546ecf7f48d', 'Hiranandani, Bldg 9, Powai', 'Mumbai', 'Mumbai', 'Maharashtra', '400076', 19.1176, 72.906),
  ('e1d9d96c-ce72-5455-a509-1d12da8dbad9', '5b874123c3ec8ae4733eb519685f893e6e5555e4bcb069163903e89b01b2bce2', '100 Feet Road, 4th Cross, Indiranagar', 'Bengaluru', 'Bengaluru', 'Karnataka', '560038', 12.9784, 77.6408),
  ('c1b9cd81-aa55-559a-bf95-862eccf2a80d', 'bd2e1cabe109980b7021cc7c60d68c883743e61ed4f79249e3d7977cf056b41d', 'Dharavi Shared Chawl Block 7, Room 12', 'Mumbai', 'Mumbai', 'Maharashtra', '400017', 19.042, 72.856),
  ('16ce458b-46cf-5a15-a173-e4dea5169075', '244f402856078659293cab4018520dc3774ecede158ee86840a05400ba5b33fe', 'Old City Shared Lane 4A, House 22', 'Hyderabad', 'Hyderabad', 'Telangana', '500002', 17.3616, 78.4747),
  ('254b189e-e70d-507d-8996-c2a3fe81df62', '57c23c1fb493f5c329768093a75a41a26c6b534058e6100643252b2c74729fac', 'Vikas Marg, A-44, Laxmi Nagar', 'New Delhi', 'New Delhi', 'Delhi', '110092', 28.6349, 77.275),
  ('60d7175b-3bb5-574a-8b65-e526175de654', '7c2abc5d358bfc0010a8009604d66fb689a981cafa5156fc359e8dcc39896ae6', 'Phase 2, Building 11, Hinjewadi', 'Pune', 'Pune', 'Maharashtra', '411057', 18.5912, 73.738),
  ('246ef9d6-ade1-5d00-9224-f78af05d3368', 'cec8354561e6e3b2f42355380a2ce8610192a9cdc561432abf8f206ad3622691', 'Lattice Bridge Road, Adyar', 'Chennai', 'Chennai', 'Tamil Nadu', '600020', 13.0012, 80.2565),
  ('461832df-2840-5b64-a4c8-9123108a52dd', '1fbb2c5b9fd0d5848043bc2868a83898d77b98a8688f197eb4b6e18f4aeb6948', 'Wide Angle, CG Road, Vastrapur', 'Ahmedabad', 'Ahmedabad', 'Gujarat', '380015', 23.033, 72.524),
  ('0f1b2b47-6790-55c2-9190-f15e4992e051', '7d837bf8e4b3af3dbc59e7705b4b56674758f4c130dc1fdce448b98bb8cf726b', 'Dharavi Shared Chawl Block 7, Room 14', 'Mumbai', 'Mumbai', 'Maharashtra', '400017', 19.042, 72.8565),
  ('69cc5023-b5bc-5a31-ae4d-dcdf4dcf373f', '604a90bc2e4ff6f75d99735bc61d0798b08a6820cad88bd1b24e7aca4cdecb9a', 'Link Road, Evershine Nagar, Malad', 'Mumbai', 'Mumbai', 'Maharashtra', '400064', 19.1876, 72.8484);

-- Mobile numbers (15) — M002 and M005 are shared across fraud cluster
INSERT INTO mobile_numbers (mobile_id, mobile_hash, country_code, mobile_status, first_seen, last_seen) VALUES
  ('cbef0b1f-9ae3-56d1-b1d3-338d3ac7acf8', '10e8c2b7e7e76dbd994e7e7056a8cc3566a5edde06f136f798a0443576d5cb90', '+91', 'ACTIVE', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('b068243d-74b6-5686-a73c-ca9cda42a1c5', '1e569dce8a4704b6b663d9635b9e33443922f13d9cbd71b95e20dc1cdf189a7c', '+91', 'SUSPECT', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('c3147df6-8a3e-5c2b-8e33-d68bb804ec50', 'f4c1f9599d671a0a15d67cf04064ed86a8fc468459ebaac1d8cbd570efcdb532', '+91', 'ACTIVE', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('8c12cddc-2554-5695-a3b5-d04d28d00b41', 'bb737bb9d1b383ba8ab4954fc614f6a8a12ae13178742c3193820461dea5bfd0', '+91', 'ACTIVE', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('13f0f4cf-cdc8-5e54-aa44-ed5ee3113a2f', 'c014ef8fc34ba8cf0db179fa92c8b107ce552ee705435853adc096eb182f9dc1', '+91', 'SUSPECT', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('5b0e62f8-6afb-5d87-b7cf-630aebd87ba5', '370d6f296fb4aee83150b259fd9722c43f9057099f449726f871b2f8049c5c6d', '+91', 'ACTIVE', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('d2275ad5-cce0-5389-b509-c43f5044d20b', '8a030bfff0c823fff4945954c96b170ba1128fd83c26bccda24d9ea100f7d358', '+91', 'ACTIVE', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('9a8c7452-3e66-530b-ac0e-a43ebe7d517b', '033295272b6a65de3ae92a750647704e13d4071e7428bc8469c4234624852ecf', '+91', 'ACTIVE', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('99afca5e-e00b-557e-85d7-fb400028f93d', '3a9c5bc66f9a0796e0dad38e673f54681228c712931612c723c0b60dc0c4bb1f', '+91', 'SUSPECT', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('c1192ca5-bbe8-58dd-9cd9-bda73253b017', '29785c1f8d2c71c70360355babec73b6f8269b09b95003b5043df584ab09ee2a', '+91', 'ACTIVE', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('0287fbf2-90c2-5506-b57e-df8e69bba808', '9fe8a540284820cf154085a1262d9f9204784a0e4ce7f40493907cc93d254bcb', '+91', 'ACTIVE', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('14b9b3d0-013c-54e9-9577-b3ace360179e', 'c27af4d87bcaa423084cbc47d1d4ef131a19ea15081238c7f76fbdbfb227a27f', '+91', 'ACTIVE', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('1907095f-6005-528c-bbd8-5ebff6f9eaf2', '0e18c3e04b135b6c58a307e535b0d1c7a3d78e3c41ed15782e921cd035288a90', '+91', 'ACTIVE', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('f009dc67-5c05-5c9f-831f-f25eb6bd5569', 'a6a77ff73b346b7bb3e232a099c3348dd0f812b32207859c4cec03802e5ffa1f', '+91', 'ACTIVE', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00'),
  ('00b949fa-16b6-5668-827e-f743d27c5c9e', '7a5f28cb27aa0e18c8321b74b8d092055dffeb0f57ec62976264e76c2b67721f', '+91', 'ACTIVE', '2025-01-15 08:00:00+00', '2026-08-20 10:00:00+00');

-- Devices (12) — D004 and D009 shared across multiple fraud customers
INSERT INTO devices (device_id, device_fingerprint, device_type, os, browser, manufacturer, model, first_seen, last_seen, device_status) VALUES
  ('9b7e0e61-c5e7-5617-bc6c-c8143bbd26b8', 'fp_iphone15_abc111', 'MOBILE', 'iOS 17', 'Safari', 'Apple', 'iPhone 15', '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', 'ACTIVE'),
  ('dddd26bd-e3ea-5bf1-b669-35add63275f8', 'fp_pixel8_xyz222', 'MOBILE', 'Android 14', 'Chrome', 'Google', 'Pixel 8', '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', 'ACTIVE'),
  ('a1cc4120-c23c-5170-b4b3-61183ef94274', 'fp_samsung_s23_qrs333', 'MOBILE', 'Android 14', 'Chrome', 'Samsung', 'Galaxy S23', '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', 'ACTIVE'),
  ('d5485e33-ab2a-5d8c-be2b-8e829e89d3be', 'fp_shared_device_FRAUD_X1', 'MOBILE', 'Android 13', 'Chrome', 'Xiaomi', 'Redmi Note 12', '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', 'SUSPECT'),
  ('6781ea92-6766-506b-8185-9341eff0b087', 'fp_oneplus_11_aaa444', 'MOBILE', 'Android 14', 'Chrome', 'OnePlus', '11R', '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', 'ACTIVE'),
  ('a4cab643-22d2-5f60-81c0-2d5010100f57', 'fp_iphone14_bbb555', 'MOBILE', 'iOS 16', 'Safari', 'Apple', 'iPhone 14', '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', 'ACTIVE'),
  ('98813bc9-153a-5d6e-a8bb-888031a3c1db', 'fp_desktop_win_chrome_ccc666', 'DESKTOP', 'Windows 11', 'Chrome', 'Dell', 'Inspiron 15', '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', 'ACTIVE'),
  ('b4331867-fec0-5c94-aac9-3101b8bf1e1b', 'fp_ipad_ddd777', 'TABLET', 'iPadOS 17', 'Safari', 'Apple', 'iPad Air', '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', 'ACTIVE'),
  ('ffcd5963-2e92-5384-9ebb-8c725d356803', 'fp_shared_device_FRAUD_X2', 'MOBILE', 'Android 13', 'Chrome', 'Realme', 'Narzo 60', '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', 'SUSPECT'),
  ('238ededb-2f50-5240-96f4-6d339b2e8073', 'fp_samsung_a54_eee888', 'MOBILE', 'Android 14', 'Chrome', 'Samsung', 'Galaxy A54', '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', 'ACTIVE'),
  ('40a16352-53fb-5289-ab1c-c68001a85ab0', 'fp_moto_g73_fff999', 'MOBILE', 'Android 13', 'Chrome', 'Motorola', 'Moto G73', '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', 'ACTIVE'),
  ('064b396f-5edc-5549-87c1-33284222904e', 'fp_iphone13_ggg000', 'MOBILE', 'iOS 17', 'Safari', 'Apple', 'iPhone 13', '2025-02-01 09:00:00+00', '2026-08-21 12:00:00+00', 'ACTIVE');

-- IP addresses (8) — IP001 shared fraud IP
INSERT INTO ip_addresses (ip_id, ip_hash, ip_version, first_seen, last_seen) VALUES
  ('6ee5070f-c819-5487-a4bf-a130a9119f43', '175a422fc4001d1ac42202a68af6ae1416d53f0c494b25e14e3cd4a6c71c52f4', 'V4', '2025-03-01 10:00:00+00', '2026-08-21 14:00:00+00'),
  ('70f42d4c-bfec-50cb-8a42-1579fdd6b011', 'acf8c722c76217a87eef35814c21a74121b17b41d0c4f1c123d684f265f55e86', 'V4', '2025-03-01 10:00:00+00', '2026-08-21 14:00:00+00'),
  ('38aae128-6234-5e54-a285-aad143fe4eaa', '05501f7c59649c17e5a4f68193251f9833850df75b97de2a31353dcf3b568d5c', 'V4', '2025-03-01 10:00:00+00', '2026-08-21 14:00:00+00'),
  ('9004eced-2824-58ff-8ec9-e254d5153aaf', '0b9195eb86c95515156c11d4390711ea765e0dd03f278cf70970e886f1441522', 'V4', '2025-03-01 10:00:00+00', '2026-08-21 14:00:00+00'),
  ('da72600e-fb20-5493-bbb5-2784eae4570a', '3db0e227e92b1f4b657374c170c2f2a091c5fe641afd3c663a16a8c405dd77ae', 'V4', '2025-03-01 10:00:00+00', '2026-08-21 14:00:00+00'),
  ('af304d0b-fcaa-550b-8c5b-6c953d9ef105', 'bf59960733978afdb93eb24eca4d429306d83f49de3269248afb1315b4c0e8e8', 'V4', '2025-03-01 10:00:00+00', '2026-08-21 14:00:00+00'),
  ('62ccdb3b-fc0e-56fc-95dd-aa639a2daced', '12c34ff857e1ddde13af419d472f24c6d30e8b77eb6a29919c9e576407f612bb', 'V4', '2025-03-01 10:00:00+00', '2026-08-21 14:00:00+00'),
  ('1d7389c4-1326-5073-8e44-a38d3f003075', '25992df687ffcacc7272d164306498e4254adc9a5526d519b2ca8d470c647508', 'V4', '2025-03-01 10:00:00+00', '2026-08-21 14:00:00+00');

-- Locations (8)
INSERT INTO locations (location_id, latitude, longitude, city, district, state, pincode) VALUES
  ('4377ae25-d1ea-50a6-b6bd-54fa4afd0096', 19.0596, 72.8295, 'Mumbai', 'Mumbai', 'Maharashtra', '400050'),
  ('c024100a-1495-5a2b-92f0-8a6948459bb6', 12.9352, 77.6245, 'Bengaluru', 'Bengaluru', 'Karnataka', '560034'),
  ('efac3db3-5c01-5500-a1f1-46af850f5803', 28.6315, 77.2167, 'New Delhi', 'New Delhi', 'Delhi', '110001'),
  ('c8fa3185-451e-5542-a2b8-d2f367984a66', 17.4156, 78.4348, 'Hyderabad', 'Hyderabad', 'Telangana', '500034'),
  ('a1d77522-0285-5fd2-bf42-b8270132c171', 22.5804, 88.412, 'Kolkata', 'Kolkata', 'West Bengal', '700091'),
  ('5f32f5ae-9811-59c3-b469-63604c57343b', 19.042, 72.856, 'Mumbai', 'Mumbai', 'Maharashtra', '400017'),
  ('f159a2f0-d36a-5fe9-b0bb-23d5554588ca', 18.5912, 73.738, 'Pune', 'Pune', 'Maharashtra', '411057'),
  ('2695a04d-a747-5d2c-a330-d3fca9eb2de7', 13.0012, 80.2565, 'Chennai', 'Chennai', 'Tamil Nadu', '600020');

-- Bank accounts (12) — B007 shared across fraud cluster
INSERT INTO bank_accounts (bank_account_id, account_hash, bank_name, ifsc, account_type, account_status, first_seen, last_seen) VALUES
  ('cc04388f-5ecb-5201-a93d-847401d76621', 'f0ca042dabf88f652b35314bb8216d9c7298af4d8b711bca8b86cdf687ff9c17', 'State Bank of India', 'SBIN0000001', 'SAVINGS', 'ACTIVE', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00'),
  ('094622a8-42f8-532c-a913-c80d3afe1c82', 'a67fca132f1a3166d418276873e2165d3eae244944d15a95c9d8ede3bee4beb1', 'HDFC Bank', 'HDFC0000002', 'SAVINGS', 'ACTIVE', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00'),
  ('3b1845ab-6df8-53cc-8778-8f6bb83714c7', '1657b9268ab2710fec71f4075d5992ff163dd476f941e7bf5a50dfba9b5e04bb', 'ICICI Bank', 'ICIC0000003', 'SAVINGS', 'ACTIVE', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00'),
  ('a053f7e6-240c-50b8-8b74-4d3b1d0e97e5', '95f8581025a53fd3fa5f2bd424c4fad060c38893a31a9bb69816322bf579db04', 'Axis Bank', 'UTIB0000004', 'SAVINGS', 'ACTIVE', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00'),
  ('5f38138f-d085-56d0-8527-98d8e9ddef50', 'd288f365a5903db569443c11dce34b958bf1d59971d3d0a382ea19885905326f', 'Kotak Mahindra', 'KKBK0000005', 'SAVINGS', 'ACTIVE', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00'),
  ('098e3dd1-683d-5387-874f-63af33a0615c', '528fe5ceaac9619f511c8352f3297ea8ba5d2fbb6f1db5d14dedcc31b190e546', 'Punjab National Bank', 'PUNB0000006', 'SAVINGS', 'ACTIVE', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00'),
  ('f1a2e82c-29a8-5f8f-a9d5-2b3abadd5ed2', '2ce5660718492ae8c2d96538d0f7eddcbbf091e825500c85881e0327cd47cbfc', 'State Bank of India', 'SBIN0000007', 'SAVINGS', 'SUSPECT', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00'),
  ('a9549ac0-6be0-53ae-80d2-40c821d51772', '57d8cc9710aee805617e512d6f6890064a9e13c83b6f79cd2d7cc0b88b291cac', 'HDFC Bank', 'HDFC0000008', 'SAVINGS', 'ACTIVE', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00'),
  ('e7739ae7-d48a-5241-9032-0745af4fdf9f', '5627e9ed88416ffac80ba0f90b62a338889618cc838e4c2a2dffbb16ba0ea76f', 'ICICI Bank', 'ICIC0000009', 'SAVINGS', 'SUSPECT', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00'),
  ('8974cf45-1897-5c00-856b-05505843291c', '6a78f812c865f00563493d96d4c3c27f5daee3e4fb0f89960dc12de12048074a', 'Axis Bank', 'UTIB0000010', 'SAVINGS', 'ACTIVE', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00'),
  ('2c2ef444-9e68-5228-afbd-0d1d61313fd9', '05baadc3e411e80438823e7dc0bd05101dd21bacfed3d2ceb97fa90e52876bb8', 'Bank of Baroda', 'BARB0000011', 'SAVINGS', 'ACTIVE', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00'),
  ('02560b3b-dd3b-54a9-af5c-99205863d359', 'a537b77e188e8a303749f85408580d1752ed9674240b1eb4097aa75ec9b7f421', 'IndusInd Bank', 'INDB0000012', 'SAVINGS', 'ACTIVE', '2025-01-20 09:00:00+00', '2026-08-20 11:00:00+00');

-- Dealers (6) — DL003 is high-velocity fraud dealer
INSERT INTO dealers (dealer_id, dealer_code, dealer_name, dealer_type, address_id, dealer_status, onboarding_date) VALUES
  ('8d32e18c-6df1-519a-850f-8e38e4f20484', 'DL001', 'Alpha Auto Finance', 'DSA', '5f51108b-57bc-5f5f-8a13-48c7ebfa74f2', 'ACTIVE', '2024-06-01'),
  ('6a69f2ba-6132-5c50-b751-bdb7a3123d85', 'DL002', 'Bengaluru Wheels Corp', 'BRANCH', '3e6a348b-a1cb-550a-b3ab-40bfcc787571', 'ACTIVE', '2024-07-15'),
  ('1530ac82-d0d9-5500-b75e-77dee064c607', 'DL003', 'Metro Quick Loans - Dharavi', 'DSA', 'c1b9cd81-aa55-559a-bf95-862eccf2a80d', 'ACTIVE', '2025-01-10'),
  ('800cc771-f6e5-5934-a249-eb1de1fd22be', 'DL004', 'Hyderabad Prime Motors', 'DSA', 'aa9729f5-9310-5751-8a02-e6ef2216207c', 'ACTIVE', '2024-08-20'),
  ('b3612cae-d240-5fe5-87d2-9bc9f2ecedf5', 'DL005', 'Delhi Capital Lending', 'BRANCH', '087921d8-4ae6-5185-8018-fade440bf91a', 'ACTIVE', '2024-09-01'),
  ('8d2310c2-5b13-5db5-9a23-740d6f5591c6', 'DL006', 'Pune Express Finance', 'ONLINE', '60d7175b-3bb5-574a-8b65-e526175de654', 'SUSPENDED', '2024-10-01');

-- Guarantors (6) — G005 shared across fraud applications
INSERT INTO guarantors (guarantor_id, guarantor_ref, full_name, identity_hash, mobile_id, address_id) VALUES
  ('afd6a7a1-735b-5e0e-b916-e86221e3746b', 'G001', 'Rajesh Kumar', '27d0cb3dc3bcec8a2bef24c6ceacd51a72b54d33281ecfc3560b89cd20bd225c', NULL, '39c1b460-6d67-515f-9436-eb8290639e98'),
  ('7590b5a8-819d-5a86-aa0e-f753442537a6', 'G002', 'Sunita Devi', 'e98526355669747ff35d95f5a6b4dff91623d891e911f23743d18cba16aff497', 'c1192ca5-bbe8-58dd-9cd9-bda73253b017', '5a46b5ef-5426-5db7-9033-7d4dcbfa5647'),
  ('8a092c15-fbc4-5650-a3e3-cf213f0100a5', 'G003', 'Amit Sharma', '4366dbef314ff2e47cac98f0c6805405db2807687b1587dad626ad3a07d8fa79', '0287fbf2-90c2-5506-b57e-df8e69bba808', '64f5a5ab-f354-53e0-8b2e-6bcc43626f01'),
  ('31249d32-2322-5922-bb9b-134a1adddbd9', 'G004', 'Lakshmi Iyer', 'a94b4ea7f660100f0da406a57f2d66cd20f74b9221cad15db8646576b76d538f', '14b9b3d0-013c-54e9-9577-b3ace360179e', '524b47e7-684f-5135-a032-e53be5e05102'),
  ('8546212a-0d87-5f98-a87d-2c1214c93130', 'G005', 'FARID SHAIKH - FRAUD RING', 'ff87b0c7ba02256163c5f4fad12ec30136a5cd927e0386578ed9344530eae269', 'b068243d-74b6-5686-a73c-ca9cda42a1c5', 'c1b9cd81-aa55-559a-bf95-862eccf2a80d'),
  ('de0073a3-b6df-54b5-a326-250609c5db89', 'G006', 'Vikash Tiwari', '7663bd72a6507e3780bde428c0d0b3bfd16aac3e901df46892c2311faf2742b9', '1907095f-6005-528c-bbd8-5ebff6f9eaf2', '254b189e-e70d-507d-8996-c2a3fe81df62');

-- Model versions (3)
INSERT INTO model_versions (model_id, model_name, version, model_type, training_completed_at, performance_metrics, model_status) VALUES
  ('45616aa0-a2ff-58a8-867c-d962240535bf', 'swarm-fraud-v1', '1.0.0', 'FRAUD_CLASSIFIER', '2026-01-15 10:00:00+00', '{"auc":0.82,"precision":0.78,"recall":0.71}', 'RETIRED'),
  ('67d05cd6-8388-5712-a88f-4150bd873ce1', 'swarm-fraud-v2', '2.1.0', 'FRAUD_CLASSIFIER', '2026-05-01 10:00:00+00', '{"auc":0.89,"precision":0.84,"recall":0.80}', 'ACTIVE'),
  ('5fdc5ae8-4ad4-589c-b934-fb6d5c56f020', 'swarm-risk-v1', '1.2.0', 'RISK_SCORER', '2026-06-01 10:00:00+00', '{"mse":0.04,"mae":0.12}', 'ACTIVE');
