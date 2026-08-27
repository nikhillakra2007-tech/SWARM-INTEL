const base = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

function toInt(v: number, fallback: number) {
  const n = Number(v)
  return Number.isInteger(n) && n > 0 ? n : fallback
}

async function req<T>(path:string, opts:RequestInit={}): Promise<T> {
  const r = await fetch(base + path, { headers: {"Content-Type":"application/json"}, ...opts, body: opts.body as any })
  if (!r.ok) {
    const text = await r.text()
    // try to extract human message, keep backend detail limited
    throw new Error(text.slice(0, 500) || `Request failed (${r.status})`)
  }
  return r.json() as T
}

export const api = {
  health: () => req<{status:string; database:string}>("/health"),
  customers: (p=1,s=20) => req<any>(`/api/customers?page=${toInt(p,1)}&size=${toInt(s,20)}`),
  customer: (id:string) => req<any>(`/api/customers/${id}`),
  applications: (p=1,s=20) => req<any>(`/api/applications?page=${toInt(p,1)}&size=${toInt(s,20)}`),
  loans: (p=1,s=20) => req<any>(`/api/loans?page=${toInt(p,1)}&size=${toInt(s,20)}`),
  devices: (id:string) => req<any>(`/api/devices/${id}`),
  dealers: (p=1,s=20) => req<any>(`/api/dealers?page=${toInt(p,1)}&size=${toInt(s,20)}`),
  clusters: () => req<any>("/api/clusters"),
  cluster: (id:string) => req<any>(`/api/clusters/${id}`),
  clusterMembers: (id:string) => req<any>(`/api/clusters/${id}/members`),
  alerts: () => req<any>("/api/alerts"),
  investigations: () => req<any>("/api/investigations"),
  signalsList: () => req<any>("/api/fraud/signals"),
  signals: (et:string,id:string) => req<any>(`/api/fraud/signals/${et}/${id}`),
  analyze: (et:string,id:string) => req<any>(`/api/intelligence/analyze/${et}/${id}`, {method:"POST"}),
  risk: (et:string,id:string) => req<any>(`/api/risk/${et}/${id}`),
  network: (et:string,id:string) => req<any>(`/api/network/${et}/${id}`),
  networkComponents: () => req<any>("/api/network/components"),
  networkGraph: () => req<any>("/api/network/graph"),
  predictions: (et:string,id:string) => req<any>(`/api/predictions/${et}/${id}`),
}
