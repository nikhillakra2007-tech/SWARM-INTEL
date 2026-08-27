-- =============================================================================
-- 004_relationship_network.sql — Entity relationships + fraud clusters/members
-- =============================================================================

-- Fraud clusters — F-1001 (HIGH) and F-1002 (MEDIUM)
INSERT INTO fraud_clusters (cluster_id, cluster_ref, cluster_type, risk_score, member_count, cluster_status, detected_at, last_updated_at, metadata) VALUES
  ('eb941871-6325-5ea3-99e6-ee117fe8ae14', 'F-1001', 'MIXED_ENTITY_CLUSTER', 91.5, 12, 'ACTIVE', '2026-08-12 10:00:00+00', '2026-08-21 10:00:00+00', '{"description":"Dharavi quick-loan ring: 4 customers share device+mobile+bank+address via DL003/G005","dealer":"DL003"}'),
  ('f5f3e5ea-6e89-50da-91aa-d850d88bf193', 'F-1002', 'MIXED_ENTITY_CLUSTER', 68.0, 8, 'UNDER_REVIEW', '2026-08-15 10:00:00+00', '2026-08-20 10:00:00+00', '{"description":"Secondary ring linked via B007/B009 bridge","dealer":"DL003/DL006"}');

-- Fraud cluster members — F-1001 (12) + F-1002 (8)
INSERT INTO fraud_cluster_members (member_id, cluster_id, entity_type, entity_id, membership_score, joined_at, left_at) VALUES
  ('0fa56dab-3a04-5685-8b30-eb815773899d', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'CUSTOMER', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 0.92, '2026-08-12 10:00:00+00', NULL),
  ('661412bb-1c12-5de6-95a7-003f646a6514', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'CUSTOMER', '262908a0-40a1-5e33-935b-16fb4610f7c3', 0.92, '2026-08-12 10:00:00+00', NULL),
  ('7d913bc2-fd32-5901-8862-cf308a6308f0', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'CUSTOMER', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', 0.92, '2026-08-12 10:00:00+00', NULL),
  ('c24e0a71-71d3-5e55-a805-9ada581b5579', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'CUSTOMER', '04d1f1de-7bd6-5c8a-9bb4-5ae5a29c6f1a', 0.92, '2026-08-12 10:00:00+00', NULL),
  ('27748323-2800-50bf-94e0-65fd21b360f8', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'DEVICE', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', 0.92, '2026-08-12 10:00:00+00', NULL),
  ('69eb5821-f623-5737-aa61-81ffd6877ba5', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'DEVICE', 'ffcd5963-2e92-5384-9ebb-8c725d356803', 0.92, '2026-08-12 10:00:00+00', NULL),
  ('3734a896-8617-5e1c-ae33-4cd063147962', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'MOBILE', 'b068243d-74b6-5686-a73c-ca9cda42a1c5', 0.92, '2026-08-12 10:00:00+00', NULL),
  ('1188aac6-f3fa-512c-9d43-8eb60763dcb2', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'BANK_ACCOUNT', 'f1a2e82c-29a8-5f8f-a9d5-2b3abadd5ed2', 0.92, '2026-08-12 10:00:00+00', NULL),
  ('b3340ae1-0939-5320-8ba8-5cd79bdf93ff', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'DEALER', '1530ac82-d0d9-5500-b75e-77dee064c607', 0.92, '2026-08-12 10:00:00+00', NULL),
  ('f88cc188-c981-5607-bc5c-1cf143a2da63', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'GUARANTOR', '8546212a-0d87-5f98-a87d-2c1214c93130', 0.92, '2026-08-12 10:00:00+00', NULL),
  ('e0a15db6-552b-52c1-8369-bab36231eb5c', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'ADDRESS', 'c1b9cd81-aa55-559a-bf95-862eccf2a80d', 0.92, '2026-08-12 10:00:00+00', NULL),
  ('ad8babe9-2be8-5bbc-b536-19631644e3cd', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'IP', '6ee5070f-c819-5487-a4bf-a130a9119f43', 0.92, '2026-08-12 10:00:00+00', NULL),
  ('8886a835-dfef-5006-92c4-e6dec8cca07c', 'f5f3e5ea-6e89-50da-91aa-d850d88bf193', 'CUSTOMER', '54a13a95-99cc-52d7-9e3a-772c7d681451', 0.75, '2026-08-15 10:00:00+00', NULL),
  ('bf2e2f92-eae9-5e68-93e5-e3b76973ee73', 'f5f3e5ea-6e89-50da-91aa-d850d88bf193', 'CUSTOMER', 'fbb13e1e-e118-53de-9d9e-e1f3144b462c', 0.75, '2026-08-15 10:00:00+00', NULL),
  ('013f641a-6ea9-5775-8374-3cea16cbf254', 'f5f3e5ea-6e89-50da-91aa-d850d88bf193', 'CUSTOMER', '268bceed-354a-5a1c-8a96-483fa6d706c7', 0.75, '2026-08-15 10:00:00+00', NULL),
  ('8042a923-b32f-5b1c-8478-7d8fb11149ec', 'f5f3e5ea-6e89-50da-91aa-d850d88bf193', 'CUSTOMER', '5988542c-1427-57fb-b248-d2737f6051b9', 0.75, '2026-08-15 10:00:00+00', NULL),
  ('65779c78-38a7-5488-8315-0d396e74b984', 'f5f3e5ea-6e89-50da-91aa-d850d88bf193', 'BANK_ACCOUNT', 'e7739ae7-d48a-5241-9032-0745af4fdf9f', 0.75, '2026-08-15 10:00:00+00', NULL),
  ('45044302-778a-5777-8df7-835d449158a6', 'f5f3e5ea-6e89-50da-91aa-d850d88bf193', 'DEVICE', 'ffcd5963-2e92-5384-9ebb-8c725d356803', 0.75, '2026-08-15 10:00:00+00', NULL),
  ('92189f4b-f7e0-5a36-87d5-3eb0bd34bed6', 'f5f3e5ea-6e89-50da-91aa-d850d88bf193', 'MOBILE', '99afca5e-e00b-557e-85d7-fb400028f93d', 0.75, '2026-08-15 10:00:00+00', NULL),
  ('f798970b-43c0-5934-8430-f05f66e686a7', 'f5f3e5ea-6e89-50da-91aa-d850d88bf193', 'DEALER', '1530ac82-d0d9-5500-b75e-77dee064c607', 0.75, '2026-08-15 10:00:00+00', NULL);

-- Entity relationships — bidirectional swarm graph (shared device/mobile/bank/address/guarantor/ip/dealer)
INSERT INTO entity_relationships (relationship_id, source_entity_type, source_entity_id, target_entity_type, target_entity_id, relationship_type, strength, confidence, evidence_count, first_seen, last_seen, metadata) VALUES
  ('8f7b4b3f-7fd9-5e9e-a61e-8a1865eb5754', 'CUSTOMER', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'DEVICE', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', 'SHARED_DEVICE', 0.98, 0.99, 4, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('a155a8a6-f955-5f33-8661-884184f450ec', 'CUSTOMER', '262908a0-40a1-5e33-935b-16fb4610f7c3', 'DEVICE', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', 'SHARED_DEVICE', 0.98, 0.99, 4, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('15485a54-b833-55a0-94ef-b4ffaf8bfdea', 'CUSTOMER', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', 'DEVICE', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', 'SHARED_DEVICE', 0.97, 0.98, 4, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('8daadfbb-137b-5739-b143-ce30a553d5b3', 'CUSTOMER', '268bceed-354a-5a1c-8a96-483fa6d706c7', 'DEVICE', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', 'SHARED_DEVICE', 0.85, 0.88, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('6070a76c-2e34-5ff6-9a92-0a9a0af32b1b', 'CUSTOMER', '04d1f1de-7bd6-5c8a-9bb4-5ae5a29c6f1a', 'DEVICE', 'ffcd5963-2e92-5384-9ebb-8c725d356803', 'SHARED_DEVICE', 0.96, 0.97, 3, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('604c3ed2-a77f-5817-b2da-a2a354bc135e', 'CUSTOMER', '54a13a95-99cc-52d7-9e3a-772c7d681451', 'DEVICE', 'ffcd5963-2e92-5384-9ebb-8c725d356803', 'SHARED_DEVICE', 0.95, 0.96, 3, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('4c5490aa-a702-5a80-b854-e2a1c6391f80', 'CUSTOMER', 'fbb13e1e-e118-53de-9d9e-e1f3144b462c', 'DEVICE', 'ffcd5963-2e92-5384-9ebb-8c725d356803', 'SHARED_DEVICE', 0.94, 0.95, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('730636f7-35a9-5765-bf58-849dca90b610', 'CUSTOMER', '5988542c-1427-57fb-b248-d2737f6051b9', 'DEVICE', 'ffcd5963-2e92-5384-9ebb-8c725d356803', 'SHARED_DEVICE', 0.9, 0.92, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('8d4e54c5-5b49-5c7a-8c5c-c16b325c7bff', 'CUSTOMER', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'MOBILE', 'b068243d-74b6-5686-a73c-ca9cda42a1c5', 'SHARED_MOBILE', 0.99, 0.99, 4, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('d9dcc1ab-6b46-5fc6-a01e-7c0b49a98881', 'CUSTOMER', '262908a0-40a1-5e33-935b-16fb4610f7c3', 'MOBILE', 'b068243d-74b6-5686-a73c-ca9cda42a1c5', 'SHARED_MOBILE', 0.99, 0.99, 4, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('c101466a-66a4-52b5-8628-3a8b24de0fbf', 'CUSTOMER', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', 'MOBILE', 'b068243d-74b6-5686-a73c-ca9cda42a1c5', 'SHARED_MOBILE', 0.85, 0.87, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('019d48e6-89f2-5527-a7b3-cfdc826d8a15', 'CUSTOMER', '54a13a95-99cc-52d7-9e3a-772c7d681451', 'MOBILE', '99afca5e-e00b-557e-85d7-fb400028f93d', 'SHARED_MOBILE', 0.92, 0.93, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('46588545-0769-528b-8d36-9b5a53a1a23c', 'CUSTOMER', 'fbb13e1e-e118-53de-9d9e-e1f3144b462c', 'MOBILE', '99afca5e-e00b-557e-85d7-fb400028f93d', 'SHARED_MOBILE', 0.92, 0.93, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('7c2fd963-11b3-5be2-8f5a-3ead64214743', 'CUSTOMER', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'BANK_ACCOUNT', 'f1a2e82c-29a8-5f8f-a9d5-2b3abadd5ed2', 'SHARED_BANK_ACCOUNT', 0.97, 0.98, 4, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('ca116538-69e6-5466-a587-683e5a07d836', 'CUSTOMER', '262908a0-40a1-5e33-935b-16fb4610f7c3', 'BANK_ACCOUNT', 'f1a2e82c-29a8-5f8f-a9d5-2b3abadd5ed2', 'SHARED_BANK_ACCOUNT', 0.97, 0.98, 4, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('bdd0876b-e752-5dd5-9f88-49043d206f9d', 'CUSTOMER', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', 'BANK_ACCOUNT', 'f1a2e82c-29a8-5f8f-a9d5-2b3abadd5ed2', 'SHARED_BANK_ACCOUNT', 0.96, 0.97, 4, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('a0c453f2-7264-5b81-9cd9-500218366d5f', 'CUSTOMER', '04d1f1de-7bd6-5c8a-9bb4-5ae5a29c6f1a', 'BANK_ACCOUNT', 'f1a2e82c-29a8-5f8f-a9d5-2b3abadd5ed2', 'SHARED_BANK_ACCOUNT', 0.9, 0.92, 1, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('fbfd08e2-0239-556a-b80c-2ff5dbb4f845', 'CUSTOMER', '268bceed-354a-5a1c-8a96-483fa6d706c7', 'BANK_ACCOUNT', 'f1a2e82c-29a8-5f8f-a9d5-2b3abadd5ed2', 'SHARED_BANK_ACCOUNT', 0.8, 0.82, 1, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('d2dfb390-0160-5689-83d6-e5e091576447', 'CUSTOMER', '54a13a95-99cc-52d7-9e3a-772c7d681451', 'BANK_ACCOUNT', 'e7739ae7-d48a-5241-9032-0745af4fdf9f', 'SHARED_BANK_ACCOUNT', 0.93, 0.94, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('e169e52f-0866-5d48-970c-e7246bd00d8a', 'CUSTOMER', 'fbb13e1e-e118-53de-9d9e-e1f3144b462c', 'BANK_ACCOUNT', 'e7739ae7-d48a-5241-9032-0745af4fdf9f', 'SHARED_BANK_ACCOUNT', 0.93, 0.94, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('358ea1f5-268a-5be3-bdf7-bf2f183e6f39', 'CUSTOMER', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'ADDRESS', 'c1b9cd81-aa55-559a-bf95-862eccf2a80d', 'SHARED_ADDRESS', 0.94, 0.95, 3, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('fdec11d7-0fbb-5bbb-95eb-b6bfe5cec675', 'CUSTOMER', '262908a0-40a1-5e33-935b-16fb4610f7c3', 'ADDRESS', 'c1b9cd81-aa55-559a-bf95-862eccf2a80d', 'SHARED_ADDRESS', 0.94, 0.95, 3, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('71c3433b-93f9-5a9e-934a-038a9f5add62', 'CUSTOMER', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', 'ADDRESS', 'c1b9cd81-aa55-559a-bf95-862eccf2a80d', 'SHARED_ADDRESS', 0.93, 0.94, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('a4299f0b-df81-5ceb-a1b3-8dea5180e0b2', 'CUSTOMER', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'GUARANTOR', '8546212a-0d87-5f98-a87d-2c1214c93130', 'SHARED_GUARANTOR', 0.96, 0.97, 3, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('c79386e5-0e17-5800-a17a-18bf56524dd0', 'CUSTOMER', '262908a0-40a1-5e33-935b-16fb4610f7c3', 'GUARANTOR', '8546212a-0d87-5f98-a87d-2c1214c93130', 'SHARED_GUARANTOR', 0.96, 0.97, 3, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('2c7569ad-1d9d-5e3e-b3c4-35be3130558f', 'CUSTOMER', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', 'GUARANTOR', '8546212a-0d87-5f98-a87d-2c1214c93130', 'SHARED_GUARANTOR', 0.95, 0.96, 3, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('a2a28a09-09b4-5f0d-b220-928c23476ce9', 'CUSTOMER', '04d1f1de-7bd6-5c8a-9bb4-5ae5a29c6f1a', 'GUARANTOR', '8546212a-0d87-5f98-a87d-2c1214c93130', 'SHARED_GUARANTOR', 0.9, 0.92, 1, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('57841b27-78e7-5d19-ab4c-0e81b0565ec3', 'CUSTOMER', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'DEALER', '1530ac82-d0d9-5500-b75e-77dee064c607', 'SAME_DEALER', 0.92, 0.94, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('316dacde-fbe8-56b0-9011-dc2fe0c6799e', 'CUSTOMER', '262908a0-40a1-5e33-935b-16fb4610f7c3', 'DEALER', '1530ac82-d0d9-5500-b75e-77dee064c607', 'SAME_DEALER', 0.92, 0.94, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('b33c695d-db62-5f50-ad73-08aa0a86d44d', 'CUSTOMER', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', 'DEALER', '1530ac82-d0d9-5500-b75e-77dee064c607', 'SAME_DEALER', 0.91, 0.93, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('705844a6-e3b5-59ef-9b36-15f0ab967aaf', 'CUSTOMER', '04d1f1de-7bd6-5c8a-9bb4-5ae5a29c6f1a', 'DEALER', '1530ac82-d0d9-5500-b75e-77dee064c607', 'SAME_DEALER', 0.9, 0.92, 1, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('50b180a6-da40-5c05-bb63-ed3f3887e3c8', 'CUSTOMER', '54a13a95-99cc-52d7-9e3a-772c7d681451', 'DEALER', '1530ac82-d0d9-5500-b75e-77dee064c607', 'SAME_DEALER', 0.88, 0.9, 1, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('2de8d5df-a717-5c95-a752-c91c81aba9e6', 'DEVICE', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', 'IP', '6ee5070f-c819-5487-a4bf-a130a9119f43', 'SAME_IP', 0.89, 0.9, 3, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('405767f4-83ed-5205-bdb7-6971471411ce', 'DEVICE', 'ffcd5963-2e92-5384-9ebb-8c725d356803', 'IP', '6ee5070f-c819-5487-a4bf-a130a9119f43', 'SAME_IP', 0.87, 0.88, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('5a4860f5-c1ef-5a70-b116-7318db06e41d', 'CUSTOMER', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'CUSTOMER', '262908a0-40a1-5e33-935b-16fb4610f7c3', 'SUSPICIOUS_LINK', 0.96, 0.97, 5, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('2b7cb7d3-b4db-5d86-946e-58495660b445', 'CUSTOMER', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'CUSTOMER', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', 'SUSPICIOUS_LINK', 0.94, 0.95, 4, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('688a54f7-6ff8-507f-ac81-6dd37b91915a', 'CUSTOMER', '262908a0-40a1-5e33-935b-16fb4610f7c3', 'CUSTOMER', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', 'SUSPICIOUS_LINK', 0.93, 0.94, 4, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('1a8b11de-a7c9-5c8a-b309-14c11a84b847', 'CUSTOMER', '54a13a95-99cc-52d7-9e3a-772c7d681451', 'CUSTOMER', 'fbb13e1e-e118-53de-9d9e-e1f3144b462c', 'SUSPICIOUS_LINK', 0.85, 0.87, 2, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}'),
  ('9ae9d79a-71cb-57b7-a6ed-96ce8dadfe44', 'DEALER', '1530ac82-d0d9-5500-b75e-77dee064c607', 'DEVICE', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', 'SHARED_DEALER_DEVICE', 0.88, 0.89, 3, '2026-08-10 09:00:00+00', '2026-08-20 10:00:00+00', '{"auto":true}');

-- Fix member_count (already set correctly above; no update needed)
SELECT '004_relationship_network loaded' AS status;
