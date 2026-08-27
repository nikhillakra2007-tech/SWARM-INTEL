-- =============================================================================
-- 005_fraud_scenarios.sql — Alerts, investigations, application events, audit logs
-- =============================================================================

-- Fraud alerts (6)
INSERT INTO fraud_alerts (alert_id, alert_ref, entity_type, entity_id, cluster_id, alert_type, severity, risk_score, alert_status, generated_at, resolved_at, evidence) VALUES
  ('9b26443e-2c7a-598f-9ae6-a616b72c7d6e', 'ALT-1001', 'CUSTOMER', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'EMERGING_FRAUD_NETWORK', 'CRITICAL', 91, 'OPEN', '2026-08-12 11:00:00+00', NULL, '{"auto":true}'),
  ('4fa5e841-244b-5ac4-a03f-4c548b3f7ffc', 'ALT-1002', 'CLUSTER', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'HIGH_RISK_DEVICE_CLUSTER', 'CRITICAL', 93, 'OPEN', '2026-08-12 11:30:00+00', NULL, '{"auto":true}'),
  ('c874bf05-eee3-5c33-ba28-28773b4775db', 'ALT-1003', 'CUSTOMER', '54a13a95-99cc-52d7-9e3a-772c7d681451', 'f5f3e5ea-6e89-50da-91aa-d850d88bf193', 'SHARED_BANK_ACCOUNT_NETWORK', 'HIGH', 72, 'OPEN', '2026-08-15 09:00:00+00', NULL, '{"auto":true}'),
  ('3ac730c4-12ea-52d8-8791-b1d5dc4ee4fa', 'ALT-1004', 'DEALER', '1530ac82-d0d9-5500-b75e-77dee064c607', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'DEALER_ANOMALY', 'CRITICAL', 94, 'IN_INVESTIGATION', '2026-08-13 10:00:00+00', NULL, '{"auto":true}'),
  ('e743ad81-d871-5344-8afd-1a3698be76ab', 'ALT-1005', 'CUSTOMER', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', NULL, 'RAPID_APPLICATION_CLUSTER', 'HIGH', 85, 'OPEN', '2026-08-16 10:00:00+00', NULL, '{"auto":true}'),
  ('269ff2ed-b0f0-5632-b8cb-8cb16a57c27d', 'ALT-1006', 'DEVICE', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', 'BEHAVIOURAL_ANOMALY', 'HIGH', 88, 'OPEN', '2026-08-14 09:00:00+00', NULL, '{"auto":true}');

-- Investigations (4)
INSERT INTO investigations (investigation_id, alert_id, investigator_ref, investigation_status, priority, notes, opened_at, closed_at) VALUES
  ('0c73d8e4-0cc7-5454-a394-53039f174e61', '9b26443e-2c7a-598f-9ae6-a616b72c7d6e', 'investigator_01', 'IN_PROGRESS', 'URGENT', 'Field visit scheduled to Dharavi address A013. Device D004 seized for review.', '2026-08-13 09:00:00+00', NULL),
  ('5e0d3d23-8cba-5c72-9cfc-e2fb436199d0', '3ac730c4-12ea-52d8-8791-b1d5dc4ee4fa', 'investigator_02', 'IN_PROGRESS', 'URGENT', 'Dealer DL003 transaction audit — 8 apps in 5 days.', '2026-08-14 10:00:00+00', NULL),
  ('c58f9c36-766f-51ce-bcfa-5097520f0f69', 'c874bf05-eee3-5c33-ba28-28773b4775db', 'investigator_01', 'OPEN', 'HIGH', 'Secondary ring review — possible bridge via B007.', '2026-08-16 09:00:00+00', NULL),
  ('c3950049-c9af-507b-8e3d-29ab1545918b', '4fa5e841-244b-5ac4-a03f-4c548b3f7ffc', 'investigator_03', 'CLOSED', 'HIGH', 'Confirmed fraud cluster F-1001. Recommended block on D004/M002/B007.', '2026-08-12 12:00:00+00', '2026-08-20 16:00:00+00');

-- Investigation actions (audit trail)
INSERT INTO investigation_actions (investigation_id, action_type, performed_by, notes, performed_at) VALUES
  ('0c73d8e4-0cc7-5454-a394-53039f174e61', 'ASSIGNED', 'manager_01', 'Assigned to investigator_01', '2026-08-13 09:05:00+00'),
  ('0c73d8e4-0cc7-5454-a394-53039f174e61', 'EVIDENCE_ADDED', 'investigator_01', 'Added device fingerprint D004 evidence', '2026-08-13 14:00:00+00'),
  ('0c73d8e4-0cc7-5454-a394-53039f174e61', 'FIELD_VISIT', 'investigator_01', 'Visited A013 — 4 customers at same chawl', '2026-08-15 11:00:00+00'),
  ('5e0d3d23-8cba-5c72-9cfc-e2fb436199d0', 'ASSIGNED', 'manager_01', 'Dealer audit assigned', '2026-08-14 10:05:00+00'),
  ('5e0d3d23-8cba-5c72-9cfc-e2fb436199d0', 'CONTACTED_DEALER', 'investigator_02', 'Dealer principal unavailable', '2026-08-16 09:00:00+00'),
  ('c3950049-c9af-507b-8e3d-29ab1545918b', 'CASE_CLOSED', 'investigator_03', 'Cluster confirmed fraud', '2026-08-20 16:00:00+00');

-- Application events — rapid burst + normal activity
INSERT INTO application_events (event_id, application_id, customer_id, device_id, ip_id, location_id, event_type, event_timestamp, metadata) VALUES
  ('fb4d1b05-f417-5da0-af17-6bcb0b492efc', 'ee97b8d1-d0c3-5d84-93b6-ef9fbc97fa36', 'c26abb20-eeb1-5002-93e5-30d328d89645', '9b7e0e61-c5e7-5617-bc6c-c8143bbd26b8', '70f42d4c-bfec-50cb-8a42-1579fdd6b011', '4377ae25-d1ea-50a6-b6bd-54fa4afd0096', 'APPLICATION_STARTED', '2026-06-01 09:50:00+00', '{"source":"seed"}'),
  ('f87dc8e0-f76b-50ac-a3aa-a964fb028281', 'ee97b8d1-d0c3-5d84-93b6-ef9fbc97fa36', 'c26abb20-eeb1-5002-93e5-30d328d89645', '9b7e0e61-c5e7-5617-bc6c-c8143bbd26b8', '70f42d4c-bfec-50cb-8a42-1579fdd6b011', '4377ae25-d1ea-50a6-b6bd-54fa4afd0096', 'APPLICATION_SUBMITTED', '2026-06-01 10:00:00+00', '{"source":"seed"}'),
  ('437ef50b-3046-5c19-8d1c-8f2884005ec6', 'a74aa1c6-b223-5df5-bc89-910e032e884a', '4605ec86-8198-573c-9385-cceb968216d8', 'dddd26bd-e3ea-5bf1-b669-35add63275f8', '38aae128-6234-5e54-a285-aad143fe4eaa', 'c024100a-1495-5a2b-92f0-8a6948459bb6', 'APPLICATION_SUBMITTED', '2026-06-05 11:00:00+00', '{"source":"seed"}'),
  ('0e9acf6c-bfd5-5b94-bc93-25620b5e25c5', '60fb0905-fc66-520e-9aa6-983721f0fe23', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', '6ee5070f-c819-5487-a4bf-a130a9119f43', '5f32f5ae-9811-59c3-b469-63604c57343b', 'APPLICATION_STARTED', '2026-08-10 09:00:00+00', '{"source":"seed"}'),
  ('8f8c7fa2-b1eb-550f-8ce8-d5805f01abc0', '60fb0905-fc66-520e-9aa6-983721f0fe23', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', '6ee5070f-c819-5487-a4bf-a130a9119f43', '5f32f5ae-9811-59c3-b469-63604c57343b', 'APPLICATION_SUBMITTED', '2026-08-10 09:15:00+00', '{"source":"seed"}'),
  ('a7c95e0e-6693-5cd6-a0b4-fdeda82c9b3d', '60fb0905-fc66-520e-9aa6-983721f0fe23', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', '6ee5070f-c819-5487-a4bf-a130a9119f43', '5f32f5ae-9811-59c3-b469-63604c57343b', 'DEVICE_CHANGED', '2026-08-10 09:20:00+00', '{"source":"seed"}'),
  ('266eacc6-54cf-5b8f-9e8a-87f9e1f41daa', '7469a595-3ce0-5a91-a85a-ff2e93fb36f5', '262908a0-40a1-5e33-935b-16fb4610f7c3', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', '6ee5070f-c819-5487-a4bf-a130a9119f43', '5f32f5ae-9811-59c3-b469-63604c57343b', 'APPLICATION_STARTED', '2026-08-10 09:00:00+00', '{"source":"seed"}'),
  ('cadfb26d-bbab-5ee1-aae8-98106da0ccdf', '7469a595-3ce0-5a91-a85a-ff2e93fb36f5', '262908a0-40a1-5e33-935b-16fb4610f7c3', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', '6ee5070f-c819-5487-a4bf-a130a9119f43', '5f32f5ae-9811-59c3-b469-63604c57343b', 'APPLICATION_SUBMITTED', '2026-08-10 09:15:00+00', '{"source":"seed"}'),
  ('08b0c8ae-b4f8-523b-bb1e-3fca0d987def', '7469a595-3ce0-5a91-a85a-ff2e93fb36f5', '262908a0-40a1-5e33-935b-16fb4610f7c3', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', '6ee5070f-c819-5487-a4bf-a130a9119f43', '5f32f5ae-9811-59c3-b469-63604c57343b', 'DEVICE_CHANGED', '2026-08-10 09:20:00+00', '{"source":"seed"}'),
  ('da9cfc5e-9d38-5b58-b13f-7c4e2df89d3f', 'ade68d5b-1673-555f-974e-eb7e181a58bb', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', '6ee5070f-c819-5487-a4bf-a130a9119f43', '5f32f5ae-9811-59c3-b469-63604c57343b', 'APPLICATION_STARTED', '2026-08-10 09:00:00+00', '{"source":"seed"}'),
  ('0e888dc9-b230-5cb2-bf5c-a76352d47fba', 'ade68d5b-1673-555f-974e-eb7e181a58bb', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', '6ee5070f-c819-5487-a4bf-a130a9119f43', '5f32f5ae-9811-59c3-b469-63604c57343b', 'APPLICATION_SUBMITTED', '2026-08-10 09:15:00+00', '{"source":"seed"}'),
  ('755f3e77-925e-5ee5-8b6e-4603fd65cbaf', 'ade68d5b-1673-555f-974e-eb7e181a58bb', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', '6ee5070f-c819-5487-a4bf-a130a9119f43', '5f32f5ae-9811-59c3-b469-63604c57343b', 'DEVICE_CHANGED', '2026-08-10 09:20:00+00', '{"source":"seed"}'),
  ('55dc31ce-f01d-5e7b-a06e-d162ab55fa0e', '85a1470a-2632-57b7-91c2-89ed652609b6', '04d1f1de-7bd6-5c8a-9bb4-5ae5a29c6f1a', 'ffcd5963-2e92-5384-9ebb-8c725d356803', '6ee5070f-c819-5487-a4bf-a130a9119f43', '5f32f5ae-9811-59c3-b469-63604c57343b', 'APPLICATION_SUBMITTED', '2026-08-11 09:00:00+00', '{"source":"seed"}'),
  ('58a07506-b0af-5ba7-84d2-f3053de89aa2', '964dd3eb-19cd-53fd-a240-cf06dcff06ec', '54a13a95-99cc-52d7-9e3a-772c7d681451', 'ffcd5963-2e92-5384-9ebb-8c725d356803', '6ee5070f-c819-5487-a4bf-a130a9119f43', '5f32f5ae-9811-59c3-b469-63604c57343b', 'BANK_ACCOUNT_CHANGED', '2026-08-12 10:05:00+00', '{"source":"seed"}'),
  ('67805ec9-3a26-541e-ad22-ed1d15e4359c', '6663e860-dcdb-5409-8462-ecf11d19a2c3', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', '6ee5070f-c819-5487-a4bf-a130a9119f43', '5f32f5ae-9811-59c3-b469-63604c57343b', 'APPLICATION_EDITED', '2026-08-15 09:05:00+00', '{"source":"seed"}'),
  ('c6088f83-6a0f-5934-b705-14f31835469f', '777442bd-eb06-5f29-b308-21994b7d790f', '3994d407-9b41-54ad-897b-6de222550fc4', 'a4cab643-22d2-5f60-81c0-2d5010100f57', '9004eced-2824-58ff-8ec9-e254d5153aaf', 'c8fa3185-451e-5542-a2b8-d2f367984a66', 'LOCATION_CHANGED', '2026-06-15 10:30:00+00', '{"source":"seed"}');

-- Audit logs
INSERT INTO audit_logs (user_ref, action, entity_type, entity_id, old_value, new_value) VALUES
  ('system', 'CREATE', 'CLUSTER', 'eb941871-6325-5ea3-99e6-ee117fe8ae14', NULL, '{"cluster_ref":"F-1001","risk_score":91.5}'),
  ('investigator_01', 'UPDATE', 'CUSTOMER', '85ca95a2-a02a-55a7-919f-a2d6af795a6c', '{"status":"ACTIVE"}', '{"status":"SUSPECT"}'),
  ('system', 'CREATE', 'ALERT', '9b26443e-2c7a-598f-9ae6-a616b72c7d6e', NULL, '{"alert_ref":"ALT-1001","severity":"CRITICAL"}'),
  ('manager_01', 'APPROVE', 'INVESTIGATION', 'c3950049-c9af-507b-8e3d-29ab1545918b', '{"status":"IN_PROGRESS"}', '{"status":"CLOSED"}');
