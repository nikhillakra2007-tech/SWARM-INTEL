// Mock dataset generated from synthetic database seed data for standalone Vercel demo

export interface MockCustomer {
  customer_id: string;
  customer_ref: string;
  full_name: string;
  date_of_birth: string;
  gender: string;
  occupation: string;
  income_band: string;
  customer_status: "ACTIVE" | "SUSPECT" | "BLOCKED";
}

export const MOCK_CUSTOMERS: MockCustomer[] = [
  { customer_id: 'c26abb20-eeb1-5002-93e5-30d328d89645', customer_ref: 'C001', full_name: 'Aarav Mehta', date_of_birth: '1992-04-12', gender: 'MALE', occupation: 'ENGINEER', income_band: 'MIDDLE', customer_status: 'ACTIVE' },
  { customer_id: '4605ec86-8198-573c-9385-cceb968216d8', customer_ref: 'C002', full_name: 'Priya Sharma', date_of_birth: '1990-07-23', gender: 'FEMALE', occupation: 'TEACHER', income_band: 'MIDDLE', customer_status: 'ACTIVE' },
  { customer_id: 'd3bcd573-6a47-508d-bf6f-b8eae300f218', customer_ref: 'C003', full_name: 'Rohan Desai', date_of_birth: '1988-11-05', gender: 'MALE', occupation: 'BUSINESS', income_band: 'UPPER_MIDDLE', customer_status: 'ACTIVE' },
  { customer_id: '7088b870-b7d2-548e-8f1f-76f8280655fe', customer_ref: 'C004', full_name: 'Ananya Gupta', date_of_birth: '1995-02-18', gender: 'FEMALE', occupation: 'DOCTOR', income_band: 'HIGH', customer_status: 'ACTIVE' },
  { customer_id: '3994d407-9b41-54ad-897b-6de222550fc4', customer_ref: 'C005', full_name: 'Vikram Singh', date_of_birth: '1985-09-30', gender: 'MALE', occupation: 'GOVERNMENT', income_band: 'MIDDLE', customer_status: 'ACTIVE' },
  { customer_id: '72f62dd6-7af9-5b5e-9592-e663104feaff', customer_ref: 'C006', full_name: 'Sneha Reddy', date_of_birth: '1993-06-14', gender: 'FEMALE', occupation: 'IT', income_band: 'UPPER_MIDDLE', customer_status: 'ACTIVE' },
  { customer_id: '99a4fc0c-ff8d-5bdb-9169-705231808acf', customer_ref: 'C007', full_name: 'Arjun Patel', date_of_birth: '1991-12-01', gender: 'MALE', occupation: 'SALES', income_band: 'LOWER_MIDDLE', customer_status: 'ACTIVE' },
  { customer_id: '85b1e8d0-a8b6-5ce2-aa7b-0624477a2bde', customer_ref: 'C008', full_name: 'Kavya Nair', date_of_birth: '1994-03-22', gender: 'FEMALE', occupation: 'LAWYER', income_band: 'HIGH', customer_status: 'ACTIVE' },
  { customer_id: 'b31c2c88-cc38-582b-a5cb-befeafd16ba5', customer_ref: 'C009', full_name: 'Rahul Verma', date_of_birth: '1987-08-09', gender: 'MALE', occupation: 'CONTRACTOR', income_band: 'MIDDLE', customer_status: 'ACTIVE' },
  { customer_id: '31bed5d7-488b-5457-8e24-6e529ff4f116', customer_ref: 'C010', full_name: 'Neha Kapoor', date_of_birth: '1996-05-17', gender: 'FEMALE', occupation: 'STUDENT', income_band: 'LOW', customer_status: 'ACTIVE' },
  { customer_id: '83ab1dd7-477d-525f-8f9d-1b27eb7fabe6', customer_ref: 'C011', full_name: 'Siddharth Rao', date_of_birth: '1989-10-11', gender: 'MALE', occupation: 'ENGINEER', income_band: 'MIDDLE', customer_status: 'ACTIVE' },
  { customer_id: '1e5537dd-4629-57e0-a1da-3a0b28dad68d', customer_ref: 'C012', full_name: 'Pooja Joshi', date_of_birth: '1992-01-25', gender: 'FEMALE', occupation: 'NURSE', income_band: 'LOWER_MIDDLE', customer_status: 'ACTIVE' },
  { customer_id: '85ca95a2-a02a-55a7-919f-a2d6af795a6c', customer_ref: 'C013', full_name: 'Imran Khan', date_of_birth: '1993-03-08', gender: 'MALE', occupation: 'DRIVER', income_band: 'LOW', customer_status: 'SUSPECT' },
  { customer_id: '262908a0-40a1-5e33-935b-16fb4610f7c3', customer_ref: 'C014', full_name: 'Farah Sheikh', date_of_birth: '1994-09-19', gender: 'FEMALE', occupation: 'SELF_EMPLOYED', income_band: 'LOW', customer_status: 'SUSPECT' },
  { customer_id: '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', customer_ref: 'C015', full_name: 'Amit Yadav', date_of_birth: '1990-12-30', gender: 'MALE', occupation: 'UNEMPLOYED', income_band: 'LOW', customer_status: 'SUSPECT' },
  { customer_id: '04d1f1de-7bd6-5c8a-9bb4-5ae5a29c6f1a', customer_ref: 'C016', full_name: 'Sunita Mishra', date_of_birth: '1991-06-06', gender: 'FEMALE', occupation: 'HOUSEWIFE', income_band: 'LOW', customer_status: 'SUSPECT' },
  { customer_id: '54a13a95-99cc-52d7-9e3a-772c7d681451', customer_ref: 'C017', full_name: 'Karan Malhotra', date_of_birth: '1988-04-04', gender: 'MALE', occupation: 'AGENT', income_band: 'LOWER_MIDDLE', customer_status: 'SUSPECT' },
  { customer_id: 'fbb13e1e-e118-53de-9d9e-e1f3144b462c', customer_ref: 'C018', full_name: 'Divya Pillai', date_of_birth: '1995-08-12', gender: 'FEMALE', occupation: 'CLERK', income_band: 'LOWER_MIDDLE', customer_status: 'SUSPECT' },
  { customer_id: '268bceed-354a-5a1c-8a96-483fa6d706c7', customer_ref: 'C019', full_name: 'Sameer Ali', date_of_birth: '1992-11-11', gender: 'MALE', occupation: 'DRIVER', income_band: 'LOW', customer_status: 'SUSPECT' },
  { customer_id: '5988542c-1427-57fb-b248-d2737f6051b9', customer_ref: 'C020', full_name: 'Meera Krishnan', date_of_birth: '1993-07-07', gender: 'FEMALE', occupation: 'TAILOR', income_band: 'LOW', customer_status: 'SUSPECT' },
];

export const MOCK_DEALERS = [
  { dealer_id: '8d32e18c-6df1-519a-850f-8e38e4f20484', dealer_code: 'DL001', dealer_name: 'Alpha Auto Finance', dealer_type: 'DSA', dealer_status: 'ACTIVE', onboarding_date: '2024-06-01' },
  { dealer_id: '6a69f2ba-6132-5c50-b751-bdb7a3123d85', dealer_code: 'DL002', dealer_name: 'Bengaluru Wheels Corp', dealer_type: 'BRANCH', dealer_status: 'ACTIVE', onboarding_date: '2024-07-15' },
  { dealer_id: '1530ac82-d0d9-5500-b75e-77dee064c607', dealer_code: 'DL003', dealer_name: 'Metro Quick Loans - Dharavi', dealer_type: 'DSA', dealer_status: 'ACTIVE', onboarding_date: '2025-01-10' },
  { dealer_id: '800cc771-f6e5-5934-a249-eb1de1fd22be', dealer_code: 'DL004', dealer_name: 'Hyderabad Prime Motors', dealer_type: 'DSA', dealer_status: 'ACTIVE', onboarding_date: '2024-08-20' },
  { dealer_id: 'b3612cae-d240-5fe5-87d2-9bc9f2ecedf5', dealer_code: 'DL005', dealer_name: 'Delhi Capital Lending', dealer_type: 'BRANCH', dealer_status: 'ACTIVE', onboarding_date: '2024-09-01' },
  { dealer_id: '8d2310c2-5b13-5db5-9a23-740d6f5591c6', dealer_code: 'DL006', dealer_name: 'Pune Express Finance', dealer_type: 'ONLINE', dealer_status: 'SUSPENDED', onboarding_date: '2024-10-01' },
];

export const MOCK_APPLICATIONS = [
  { application_id: '60fb0905-fc66-520e-9aa6-983721f0fe23', application_ref: 'APP-1001', customer_id: '85ca95a2-a02a-55a7-919f-a2d6af795a6c', requested_amount: 150000, application_status: 'REJECTED', application_timestamp: '2026-08-10T09:15:00Z' },
  { application_id: '7469a595-3ce0-5a91-a85a-ff2e93fb36f5', application_ref: 'APP-1002', customer_id: '262908a0-40a1-5e33-935b-16fb4610f7c3', requested_amount: 175000, application_status: 'REJECTED', application_timestamp: '2026-08-10T09:15:00Z' },
  { application_id: 'ade68d5b-1673-555f-974e-eb7e181a58bb', application_ref: 'APP-1003', customer_id: '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', requested_amount: 160000, application_status: 'REJECTED', application_timestamp: '2026-08-10T09:15:00Z' },
  { application_id: '85a1470a-2632-57b7-91c2-89ed652609b6', application_ref: 'APP-1004', customer_id: '04d1f1de-7bd6-5c8a-9bb4-5ae5a29c6f1a', requested_amount: 140000, application_status: 'REJECTED', application_timestamp: '2026-08-11T09:00:00Z' },
  { application_id: 'ee97b8d1-d0c3-5d84-93b6-ef9fbc97fa36', application_ref: 'APP-0001', customer_id: 'c26abb20-eeb1-5002-93e5-30d328d89645', requested_amount: 500000, application_status: 'APPROVED', application_timestamp: '2026-06-01T10:00:00Z' },
  { application_id: 'a74aa1c6-b223-5df5-bc89-910e032e884a', application_ref: 'APP-0002', customer_id: '4605ec86-8198-573c-9385-cceb968216d8', requested_amount: 350000, application_status: 'APPROVED', application_timestamp: '2026-06-05T11:00:00Z' },
  { application_id: 'b561fa91-c113-5a44-88d2-ca49d88fe102', application_ref: 'APP-0003', customer_id: 'd3bcd573-6a47-508d-bf6f-b8eae300f218', requested_amount: 800000, application_status: 'APPROVED', application_timestamp: '2026-06-10T14:30:00Z' },
  { application_id: 'c992aa84-d992-5b91-a128-bb2233445566', application_ref: 'APP-0004', customer_id: '7088b870-b7d2-548e-8f1f-76f8280655fe', requested_amount: 1200000, application_status: 'APPROVED', application_timestamp: '2026-06-18T16:00:00Z' },
  { application_id: 'd8821bc3-e883-5c02-b239-cc3344556677', application_ref: 'APP-0005', customer_id: '3994d407-9b41-54ad-897b-6de222550fc4', requested_amount: 450000, application_status: 'APPROVED', application_timestamp: '2026-06-25T11:20:00Z' },
];

export const MOCK_LOANS = [
  { loan_id: '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d', loan_account_ref: 'LN-2026-0001', sanctioned_amount: 500000, loan_status: 'ACTIVE', customer_id: 'c26abb20-eeb1-5002-93e5-30d328d89645' },
  { loan_id: '2b3c4d5e-6f7a-8b9c-0d1e-2f3a4b5c6d7e', loan_account_ref: 'LN-2026-0002', sanctioned_amount: 350000, loan_status: 'ACTIVE', customer_id: '4605ec86-8198-573c-9385-cceb968216d8' },
  { loan_id: '3c4d5e6f-7a8b-9c0d-1e2f-3a4b5c6d7e8f', loan_account_ref: 'LN-2026-0003', sanctioned_amount: 800000, loan_status: 'ACTIVE', customer_id: 'd3bcd573-6a47-508d-bf6f-b8eae300f218' },
  { loan_id: '4d5e6f7a-8b9c-0d1e-2f3a-4b5c6d7e8f9a', loan_account_ref: 'LN-2026-0004', sanctioned_amount: 1200000, loan_status: 'CLOSED', customer_id: '7088b870-b7d2-548e-8f1f-76f8280655fe' },
  { loan_id: '5e6f7a8b-9c0d-1e2f-3a4b-5c6d7e8f9a0b', loan_account_ref: 'LN-2026-0005', sanctioned_amount: 450000, loan_status: 'ACTIVE', customer_id: '3994d407-9b41-54ad-897b-6de222550fc4' },
];

export const MOCK_CLUSTERS = [
  { cluster_id: 'eb941871-6325-5ea3-99e6-ee117fe8ae14', cluster_ref: 'F-1001', member_count: 8, risk_score: 91.5, cluster_status: 'CRITICAL', detected_pattern: 'SHARED_DEVICE_AND_DEALER_BURST' },
  { cluster_id: 'f5f3e5ea-6e89-50da-91aa-d850d88bf193', cluster_ref: 'F-1002', member_count: 6, risk_score: 76.8, cluster_status: 'HIGH', detected_pattern: 'SHARED_BANK_ACCOUNT_RING' },
  { cluster_id: 'a1b2c3d4-e5f6-7a8b-9c0d-e1f2a3b4c5d6', cluster_ref: 'F-9001', member_count: 12, risk_score: 94.2, cluster_status: 'CRITICAL', detected_pattern: 'MULTI_COMMUNITY_COLLUSION' },
  { cluster_id: 'b2c3d4e5-f6a7-8b9c-0d1e-f2a3b4c5d6e7', cluster_ref: 'F-3004', member_count: 4, risk_score: 62.0, cluster_status: 'HIGH', detected_pattern: 'SUSPICIOUS_GUARANTOR_NETWORK' },
];

export const MOCK_ALERTS = [
  { alert_id: '9b26443e-2c7a-598f-9ae6-a616b72c7d6e', alert_ref: 'ALT-1001', entity_type: 'CUSTOMER', entity_id: '85ca95a2-a02a-55a7-919f-a2d6af795a6c', cluster_id: 'eb941871-6325-5ea3-99e6-ee117fe8ae14', alert_type: 'EMERGING_FRAUD_NETWORK', severity: 'CRITICAL', risk_score: 91.5, alert_status: 'OPEN', generated_at: '2026-08-12T11:00:00Z' },
  { alert_id: '4fa5e841-244b-5ac4-a03f-4c548b3f7ffc', alert_ref: 'ALT-1002', entity_type: 'CLUSTER', entity_id: 'eb941871-6325-5ea3-99e6-ee117fe8ae14', cluster_id: 'eb941871-6325-5ea3-99e6-ee117fe8ae14', alert_type: 'HIGH_RISK_DEVICE_CLUSTER', severity: 'CRITICAL', risk_score: 93.0, alert_status: 'OPEN', generated_at: '2026-08-12T11:30:00Z' },
  { alert_id: 'c874bf05-eee3-5c33-ba28-28773b4775db', alert_ref: 'ALT-1003', entity_type: 'CUSTOMER', entity_id: '54a13a95-99cc-52d7-9e3a-772c7d681451', cluster_id: 'f5f3e5ea-6e89-50da-91aa-d850d88bf193', alert_type: 'SHARED_BANK_ACCOUNT_NETWORK', severity: 'HIGH', risk_score: 72.0, alert_status: 'OPEN', generated_at: '2026-08-15T09:00:00Z' },
  { alert_id: '3ac730c4-12ea-52d8-8791-b1d5dc4ee4fa', alert_ref: 'ALT-1004', entity_type: 'DEALER', entity_id: '1530ac82-d0d9-5500-b75e-77dee064c607', cluster_id: 'eb941871-6325-5ea3-99e6-ee117fe8ae14', alert_type: 'DEALER_ANOMALY', severity: 'CRITICAL', risk_score: 94.0, alert_status: 'IN_INVESTIGATION', generated_at: '2026-08-13T10:00:00Z' },
  { alert_id: 'e743ad81-d871-5344-8afd-1a3698be76ab', alert_ref: 'ALT-1005', entity_type: 'CUSTOMER', entity_id: '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', cluster_id: 'eb941871-6325-5ea3-99e6-ee117fe8ae14', alert_type: 'RAPID_APPLICATION_CLUSTER', severity: 'HIGH', risk_score: 85.0, alert_status: 'OPEN', generated_at: '2026-08-16T10:00:00Z' },
  { alert_id: '269ff2ed-b0f0-5632-b8cb-8cb16a57c27d', alert_ref: 'ALT-1006', entity_type: 'DEVICE', entity_id: 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', cluster_id: 'eb941871-6325-5ea3-99e6-ee117fe8ae14', alert_type: 'BEHAVIOURAL_ANOMALY', severity: 'HIGH', risk_score: 88.0, alert_status: 'OPEN', generated_at: '2026-08-14T09:00:00Z' },
];

export const MOCK_INVESTIGATIONS = [
  { investigation_id: '0c73d8e4-0cc7-5454-a394-53039f174e61', alert_id: '9b26443e-2c7a-598f-9ae6-a616b72c7d6e', investigator_ref: 'investigator_01', investigation_status: 'IN_PROGRESS', priority: 'URGENT', notes: 'Field visit scheduled to Dharavi address A013. Device D004 seized for review.', opened_at: '2026-08-13T09:00:00Z', closed_at: null },
  { investigation_id: '5e0d3d23-8cba-5c72-9cfc-e2fb436199d0', alert_id: '3ac730c4-12ea-52d8-8791-b1d5dc4ee4fa', investigator_ref: 'investigator_02', investigation_status: 'IN_PROGRESS', priority: 'URGENT', notes: 'Dealer DL003 transaction audit — 8 apps in 5 days.', opened_at: '2026-08-14T10:00:00Z', closed_at: null },
  { investigation_id: 'c58f9c36-766f-51ce-bcfa-5097520f0f69', alert_id: 'c874bf05-eee3-5c33-ba28-28773b4775db', investigator_ref: 'investigator_01', investigation_status: 'OPEN', priority: 'HIGH', notes: 'Secondary ring review — possible bridge via B007.', opened_at: '2026-08-16T09:00:00Z', closed_at: null },
  { investigation_id: 'c3950049-c9af-507b-8e3d-29ab1545918b', alert_id: '4fa5e841-244b-5ac4-a03f-4c548b3f7ffc', investigator_ref: 'investigator_03', investigation_status: 'CLOSED', priority: 'HIGH', notes: 'Confirmed fraud cluster F-1001. Recommended block on D004/M002/B007.', opened_at: '2026-08-12T12:00:00Z', closed_at: '2026-08-20T16:00:00Z' },
];

export const MOCK_SIGNALS = [
  { signal_id: 'sig-1', entity_type: 'CUSTOMER', entity_id: '85ca95a2-a02a-55a7-919f-a2d6af795a6c', signal_type: 'SHARED_DEVICE_HIGH_FREQUENCY', severity: 'CRITICAL', score: 95.0, explanation: 'Device D004 shared with 4 distinct applicants in under 48 hours.' },
  { signal_id: 'sig-2', entity_type: 'DEALER', entity_id: '1530ac82-d0d9-5500-b75e-77dee064c607', signal_type: 'DEALER_APPLICATION_BURST', severity: 'CRITICAL', score: 92.5, explanation: 'Dealer DL003 submitted 8 loan applications in 5 days with 100% suspect customer cluster links.' },
  { signal_id: 'sig-3', entity_type: 'CUSTOMER', entity_id: '262908a0-40a1-5e33-935b-16fb4610f7c3', signal_type: 'SHARED_BANK_ACCOUNT', severity: 'HIGH', score: 88.0, explanation: 'Bank Account B007 linked to 3 separate PAN hashes.' },
  { signal_id: 'sig-4', entity_type: 'CUSTOMER', entity_id: '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', signal_type: 'SUSPICIOUS_COMMON_GUARANTOR', severity: 'HIGH', score: 84.0, explanation: 'Guarantor G005 guarantees 5 concurrent high-risk micro-loans.' },
  { signal_id: 'sig-5', entity_type: 'DEVICE', entity_id: 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', signal_type: 'DEVICE_FINGERPRINT_REUSE', severity: 'HIGH', score: 81.0, explanation: 'Redmi Note 12 used across multiple unrelated Aadhaar identifiers.' },
];

export function getMockAnalysis(entityType: string, entityId: string) {
  const isClusterMember = ['85ca95a2-a02a-55a7-919f-a2d6af795a6c', '262908a0-40a1-5e33-935b-16fb4610f7c3', '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', '04d1f1de-7bd6-5c8a-9bb4-5ae5a29c6f1a', '1530ac82-d0d9-5500-b75e-77dee064c607'].includes(entityId);
  const isDealer = entityType === 'DEALER';

  const individualScore = isClusterMember ? 35.0 : 18.0;
  const networkScore = isClusterMember ? 96.5 : (isDealer ? 88.0 : 15.0);
  const mlProb = isClusterMember ? 0.88 : (isDealer ? 0.74 : 0.08);
  const collectiveScore = Math.round(0.25 * individualScore + 0.45 * networkScore + 0.30 * (mlProb * 100));

  const riskLevel = collectiveScore >= 80 ? 'CRITICAL' : collectiveScore >= 60 ? 'HIGH' : collectiveScore >= 30 ? 'MEDIUM' : 'LOW';
  const individualLevel = individualScore >= 60 ? 'HIGH' : individualScore >= 30 ? 'MEDIUM' : 'LOW';
  const networkLevel = networkScore >= 80 ? 'CRITICAL' : networkScore >= 60 ? 'HIGH' : 'LOW';

  const reasons = isClusterMember
    ? [
        'Shared Device (D004) identified across 4 concurrent loan applications in Dharavi cluster.',
        'Common Dealer DL003 flagged for abnormal application spike pattern.',
        'Guarantor G005 linked to known suspect ring F-1001 with 8 connected entities.',
        'Shared Mobile M002 and Bank Account B007 reuse across unrelated customer identities.',
        'Network density and clustering coefficient indicate synthetic fraud syndicate collusion.',
      ]
    : [
        'Entity exhibits normal verification metrics with standard credit profile.',
        'Isolated relationship graph with no shared suspect hardware fingerprints.',
        'Single active bank account and registered mobile number verified with KYC.',
      ];

  const rules = isClusterMember
    ? [
        { signal_type: 'SHARED_DEVICE_HIGH_FREQUENCY', severity: 'CRITICAL', score: 95.0, explanation: 'Device D004 shared with 4 distinct applicants in under 48 hours.' },
        { signal_type: 'DEALER_ANOMALY_BURST', severity: 'CRITICAL', score: 92.5, explanation: 'Dealer DL003 submitted 8 loan applications in 5 days.' },
        { signal_type: 'SHARED_BANK_ACCOUNT', severity: 'HIGH', score: 88.0, explanation: 'Bank Account B007 linked to multiple PAN records.' },
        { signal_type: 'SUSPICIOUS_GUARANTOR_OVERLAP', severity: 'HIGH', score: 84.0, explanation: 'Guarantor G005 guarantees 5 concurrent high-risk applications.' },
      ]
    : [
        { signal_type: 'CLEAN_KYC_VERIFICATION', severity: 'LOW', score: 10.0, explanation: 'Aadhaar and PAN matched successfully with single device footprint.' },
      ];

  return {
    collective: {
      collective_risk_score: collectiveScore,
      risk_level: riskLevel,
      individual_risk_score: individualScore,
      individual_level: individualLevel,
      network_risk_score: networkScore,
      network_level: networkLevel,
      confidence: 0.94,
      weights: { individual: 0.25, network: 0.45, ml: 0.30 },
    },
    explanation: { reasons },
    features: {
      network_degree: isClusterMember ? 7 : 1,
      network_density: isClusterMember ? 0.68 : 0.05,
      high_risk_neighbor_count: isClusterMember ? 4 : 0,
      shared_device_count: isClusterMember ? 3 : 0,
      shared_bank_account_count: isClusterMember ? 2 : 0,
      dealer_concentration_score: isClusterMember ? 0.92 : 0.15,
      temporal_burst_frequency: isClusterMember ? 4.8 : 0.2,
    },
    ml: {
      probability: mlProb,
      label: mlProb > 0.5 ? 'FRAUD_PREDICTED' : 'NORMAL_PREDICTED',
    },
    rules,
    alert: isClusterMember ? { alert_ref: 'ALT-1001', severity: 'CRITICAL' } : null,
  };
}

export function getMockNetwork(entityType: string, entityId: string) {
  return {
    nodes: [
      { id: `${entityType}:${entityId}`, type: entityType, label: entityId.slice(0, 4) },
      { id: 'DEVICE:d5485e33-ab2a-5d8c-be2b-8e829e89d3be', type: 'DEVICE', label: 'D004' },
      { id: 'CUSTOMER:262908a0-40a1-5e33-935b-16fb4610f7c3', type: 'CUSTOMER', label: 'C014' },
      { id: 'CUSTOMER:3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', type: 'CUSTOMER', label: 'C015' },
      { id: 'DEALER:1530ac82-d0d9-5500-b75e-77dee064c607', type: 'DEALER', label: 'DL03' },
      { id: 'BANK_ACCOUNT:f1a2e82c-29a8-5f8f-a9d5-2b3abadd5ed2', type: 'BANK_ACCOUNT', label: 'B007' },
    ],
    edges: [
      { source: `${entityType}:${entityId}`, target: 'DEVICE:d5485e33-ab2a-5d8c-be2b-8e829e89d3be', label: 'SHARED_DEVICE' },
      { source: 'CUSTOMER:262908a0-40a1-5e33-935b-16fb4610f7c3', target: 'DEVICE:d5485e33-ab2a-5d8c-be2b-8e829e89d3be', label: 'SHARED_DEVICE' },
      { source: 'CUSTOMER:3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', target: 'DEVICE:d5485e33-ab2a-5d8c-be2b-8e829e89d3be', label: 'SHARED_DEVICE' },
      { source: `${entityType}:${entityId}`, target: 'DEALER:1530ac82-d0d9-5500-b75e-77dee064c607', label: 'APPLICATION_DEALER' },
      { source: `${entityType}:${entityId}`, target: 'BANK_ACCOUNT:f1a2e82c-29a8-5f8f-a9d5-2b3abadd5ed2', label: 'SHARED_BANK_ACCOUNT' },
    ],
  };
}
