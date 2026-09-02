import {
  MOCK_CUSTOMERS,
  MOCK_DEALERS,
  MOCK_APPLICATIONS,
  MOCK_LOANS,
  MOCK_CLUSTERS,
  MOCK_ALERTS,
  MOCK_INVESTIGATIONS,
  MOCK_SIGNALS,
  getMockAnalysis,
  getMockNetwork
} from "./mockData"

const base = import.meta.env.VITE_API_URL || ""

function toInt(v: number, fallback: number) {
  const n = Number(v)
  return Number.isInteger(n) && n > 0 ? n : fallback
}

async function req<T>(path: string, opts: RequestInit = {}): Promise<T> {
  if (!base) {
    throw new Error("No backend configured, using demo mode")
  }
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), 3500)
  try {
    const r = await fetch(base + path, {
      headers: { "Content-Type": "application/json" },
      signal: controller.signal,
      ...opts,
      body: opts.body as any,
    })
    clearTimeout(timeoutId)
    if (!r.ok) {
      const text = await r.text()
      throw new Error(text.slice(0, 500) || `Request failed (${r.status})`)
    }
    return r.json() as T
  } catch (err) {
    clearTimeout(timeoutId)
    throw err
  }
}

export const api = {
  health: async () => {
    try {
      return await req<{ status: string; database: string }>("/health")
    } catch {
      return { status: "active", database: "standalone (in-memory demo / vercel)" }
    }
  },

  customers: async (p = 1, s = 20) => {
    try {
      return await req<any>(`/api/customers?page=${toInt(p, 1)}&size=${toInt(s, 20)}`)
    } catch {
      const page = toInt(p, 1)
      const size = toInt(s, 20)
      const start = (page - 1) * size
      const items = MOCK_CUSTOMERS.slice(start, start + size)
      return { items, total: MOCK_CUSTOMERS.length, page, size }
    }
  },

  customer: async (id: string) => {
    try {
      return await req<any>(`/api/customers/${id}`)
    } catch {
      const c = MOCK_CUSTOMERS.find((x) => x.customer_id === id || x.customer_ref === id) || MOCK_CUSTOMERS[0]
      return c
    }
  },

  applications: async (p = 1, s = 20) => {
    try {
      return await req<any>(`/api/applications?page=${toInt(p, 1)}&size=${toInt(s, 20)}`)
    } catch {
      const page = toInt(p, 1)
      const size = toInt(s, 20)
      const start = (page - 1) * size
      const items = MOCK_APPLICATIONS.slice(start, start + size)
      return { items, total: 10000, page, size }
    }
  },

  loans: async (p = 1, s = 20) => {
    try {
      return await req<any>(`/api/loans?page=${toInt(p, 1)}&size=${toInt(s, 20)}`)
    } catch {
      const page = toInt(p, 1)
      const size = toInt(s, 20)
      const start = (page - 1) * size
      const items = MOCK_LOANS.slice(start, start + size)
      return { items, total: 7500, page, size }
    }
  },

  devices: async (id: string) => {
    try {
      return await req<any>(`/api/devices/${id}`)
    } catch {
      return {
        device_id: id,
        fingerprint: "fp_shared_device_FRAUD_X1",
        device_type: "MOBILE",
        os: "Android 13",
        browser: "Chrome",
        manufacturer: "Xiaomi",
        model: "Redmi Note 12",
        associated_customers: MOCK_CUSTOMERS.slice(12, 16),
      }
    }
  },

  dealers: async (p = 1, s = 20) => {
    try {
      return await req<any>(`/api/dealers?page=${toInt(p, 1)}&size=${toInt(s, 20)}`)
    } catch {
      const page = toInt(p, 1)
      const size = toInt(s, 20)
      const start = (page - 1) * size
      const items = MOCK_DEALERS.slice(start, start + size)
      return { items, total: MOCK_DEALERS.length, page, size }
    }
  },

  clusters: async () => {
    try {
      return await req<any>("/api/clusters")
    } catch {
      return { items: MOCK_CLUSTERS, total: MOCK_CLUSTERS.length }
    }
  },

  cluster: async (id: string) => {
    try {
      return await req<any>(`/api/clusters/${id}`)
    } catch {
      const cl = MOCK_CLUSTERS.find((x) => x.cluster_id === id || x.cluster_ref === id) || MOCK_CLUSTERS[0]
      return cl
    }
  },

  clusterMembers: async (id: string) => {
    try {
      return await req<any>(`/api/clusters/${id}/members`)
    } catch {
      return {
        cluster_id: id,
        members: [
          { member_id: 'm1', entity_type: 'CUSTOMER', entity_id: '85ca95a2-a02a-55a7-919f-a2d6af795a6c', membership_score: 95.0 },
          { member_id: 'm2', entity_type: 'CUSTOMER', entity_id: '262908a0-40a1-5e33-935b-16fb4610f7c3', membership_score: 92.5 },
          { member_id: 'm3', entity_type: 'CUSTOMER', entity_id: '3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', membership_score: 91.0 },
          { member_id: 'm4', entity_type: 'CUSTOMER', entity_id: '04d1f1de-7bd6-5c8a-9bb4-5ae5a29c6f1a', membership_score: 89.5 },
          { member_id: 'm5', entity_type: 'DEVICE', entity_id: 'd5485e33-ab2a-5d8c-be2b-8e829e89d3be', membership_score: 98.0 },
          { member_id: 'm6', entity_type: 'DEALER', entity_id: '1530ac82-d0d9-5500-b75e-77dee064c607', membership_score: 94.0 },
        ],
      }
    }
  },

  alerts: async () => {
    try {
      return await req<any>("/api/alerts")
    } catch {
      return { items: MOCK_ALERTS, total: MOCK_ALERTS.length }
    }
  },

  investigations: async () => {
    try {
      return await req<any>("/api/investigations")
    } catch {
      return { items: MOCK_INVESTIGATIONS, total: MOCK_INVESTIGATIONS.length }
    }
  },

  signalsList: async () => {
    try {
      return await req<any>("/api/fraud/signals")
    } catch {
      return { items: MOCK_SIGNALS, total: MOCK_SIGNALS.length }
    }
  },

  signals: async (et: string, id: string) => {
    try {
      return await req<any>(`/api/fraud/signals/${et}/${id}`)
    } catch {
      return { items: MOCK_SIGNALS, total: MOCK_SIGNALS.length }
    }
  },

  analyze: async (et: string, id: string) => {
    try {
      return await req<any>(`/api/intelligence/analyze/${et}/${id}`, { method: "POST" })
    } catch {
      return getMockAnalysis(et, id)
    }
  },

  risk: async (et: string, id: string) => {
    try {
      return await req<any>(`/api/risk/${et}/${id}`)
    } catch {
      return getMockAnalysis(et, id).collective
    }
  },

  network: async (et: string, id: string) => {
    try {
      return await req<any>(`/api/network/${et}/${id}`)
    } catch {
      return getMockNetwork(et, id)
    }
  },

  networkComponents: async () => {
    try {
      return await req<any>("/api/network/components")
    } catch {
      return {
        components: [
          {
            component_id: 'comp-1',
            size: 8,
            members: [
              'CUSTOMER:85ca95a2-a02a-55a7-919f-a2d6af795a6c',
              'DEVICE:d5485e33-ab2a-5d8c-be2b-8e829e89d3be',
              'CUSTOMER:262908a0-40a1-5e33-935b-16fb4610f7c3',
              'CUSTOMER:3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb',
              'CUSTOMER:04d1f1de-7bd6-5c8a-9bb4-5ae5a29c6f1a',
              'DEALER:1530ac82-d0d9-5500-b75e-77dee064c607',
              'BANK_ACCOUNT:f1a2e82c-29a8-5f8f-a9d5-2b3abadd5ed2',
              'MOBILE:b068243d-74b6-5686-a73c-ca9cda42a1c5',
            ],
          },
          {
            component_id: 'comp-2',
            size: 5,
            members: [
              'CUSTOMER:54a13a95-99cc-52d7-9e3a-772c7d681451',
              'BANK_ACCOUNT:e7739ae7-d48a-5241-9032-0745af4fdf9f',
              'CUSTOMER:fbb13e1e-e118-53de-9d9e-e1f3144b462c',
              'CUSTOMER:268bceed-354a-5a1c-8a96-483fa6d706c7',
              'CUSTOMER:5988542c-1427-57fb-b248-d2737f6051b9',
            ],
          },
        ],
      }
    }
  },

  networkGraph: async () => {
    try {
      return await req<any>("/api/network/graph")
    } catch {
      return {
        nodes: [
          { id: 'CUSTOMER:85ca95a2-a02a-55a7-919f-a2d6af795a6c', type: 'CUSTOMER', label: 'C013' },
          { id: 'DEVICE:d5485e33-ab2a-5d8c-be2b-8e829e89d3be', type: 'DEVICE', label: 'D004' },
          { id: 'CUSTOMER:262908a0-40a1-5e33-935b-16fb4610f7c3', type: 'CUSTOMER', label: 'C014' },
          { id: 'CUSTOMER:3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', type: 'CUSTOMER', label: 'C015' },
          { id: 'DEALER:1530ac82-d0d9-5500-b75e-77dee064c607', type: 'DEALER', label: 'DL03' },
          { id: 'BANK_ACCOUNT:f1a2e82c-29a8-5f8f-a9d5-2b3abadd5ed2', type: 'BANK_ACCOUNT', label: 'B007' },
        ],
        edges: [
          { source: 'CUSTOMER:85ca95a2-a02a-55a7-919f-a2d6af795a6c', target: 'DEVICE:d5485e33-ab2a-5d8c-be2b-8e829e89d3be', label: 'SHARED_DEVICE' },
          { source: 'CUSTOMER:262908a0-40a1-5e33-935b-16fb4610f7c3', target: 'DEVICE:d5485e33-ab2a-5d8c-be2b-8e829e89d3be', label: 'SHARED_DEVICE' },
          { source: 'CUSTOMER:3ec3dd27-5de7-5ad3-bc0e-c0a95d5371fb', target: 'DEVICE:d5485e33-ab2a-5d8c-be2b-8e829e89d3be', label: 'SHARED_DEVICE' },
          { source: 'CUSTOMER:85ca95a2-a02a-55a7-919f-a2d6af795a6c', target: 'DEALER:1530ac82-d0d9-5500-b75e-77dee064c607', label: 'APPLICATION_DEALER' },
        ],
      }
    }
  },

  predictions: async (et: string, id: string) => {
    try {
      return await req<any>(`/api/predictions/${et}/${id}`)
    } catch {
      return {
        entity_type: et,
        entity_id: id,
        model_name: "swarm-fraud-v2",
        fraud_probability: 0.88,
        predicted_label: "FRAUD_SUSPECT",
        confidence: 0.92,
      }
    }
  },
}
