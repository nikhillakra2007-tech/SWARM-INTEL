import { useEffect, useState } from "react"
import { api } from "../api/client"
import { Card, Empty, ErrorState, Badge } from "../components/ui"
import { Link } from "react-router-dom"

function useFetch<T>(fn: () => Promise<T>) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string>("")
  const load = () => {
    setLoading(true)
    setError("")
    fn()
      .then(setData)
      .catch((e) => setError(e.message || String(e)))
      .finally(() => setLoading(false))
  }
  useEffect(() => {
    load()
  }, [])
  return { data, loading, error, retry: load }
}

function InteractiveNetworkMap({
  nodes,
  edges,
}: {
  nodes: { id: string; type: string }[]
  edges: { source: string; target: string; label: string }[]
}) {
  const [hoveredNode, setHoveredNode] = useState<string | null>(null)
  const cx = 300, cy = 150, r = 110
  const pos: Record<string, { x: number; y: number }> = {}

  nodes.forEach((n, i) => {
    const angle = (i / nodes.length) * 2 * Math.PI - Math.PI / 2
    pos[n.id] = { x: cx + Math.cos(angle) * r, y: cy + Math.sin(angle) * r }
  })
  if (nodes[0]) pos[nodes[0].id] = { x: cx, y: cy }

  const connectedNodes = new Set<string>()
  if (hoveredNode) {
    connectedNodes.add(hoveredNode)
    edges.forEach((e) => {
      if (e.source === hoveredNode) connectedNodes.add(e.target)
      if (e.target === hoveredNode) connectedNodes.add(e.source)
    })
  }

  return (
    <div style={{ position: "relative" }}>
      <svg
        viewBox="0 0 600 300"
        width="100%"
        height="320"
        style={{
          background: "var(--bg)",
          borderRadius: 14,
          border: "1px solid var(--border)",
          transition: "var(--transition-smooth)",
        }}
      >
        {edges.map((e, i) => {
          const a = pos[e.source], b = pos[e.target]
          if (!a || !b) return null
          const susp = e.label.includes("SHARED") || e.label.includes("SUSPICIOUS")
          const isEdgeActive = hoveredNode
            ? e.source === hoveredNode || e.target === hoveredNode
            : true
          const isDimmed = hoveredNode && !isEdgeActive

          return (
            <g key={i} opacity={isDimmed ? 0.1 : 1} style={{ transition: "opacity 0.3s ease" }}>
              <line
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                stroke={susp ? "#ef4444" : "var(--border)"}
                strokeWidth={isEdgeActive && hoveredNode ? 2.5 : susp ? 1.8 : 1}
                strokeDasharray={susp ? "4 3" : "none"}
                style={{
                  animation: susp ? "flowDash 2s linear infinite" : "none",
                }}
              />
              <text
                x={(a.x + b.x) / 2}
                y={(a.y + b.y) / 2 - 4}
                fontSize="8"
                fontWeight="600"
                fill={susp ? "#ef4444" : "var(--muted)"}
                textAnchor="middle"
              >
                {e.label.replace("SHARED_", "")}
              </text>
            </g>
          )
        })}

        {nodes.map((n) => {
          const p = pos[n.id]
          const isHovered = hoveredNode === n.id
          const isConnected = hoveredNode ? connectedNodes.has(n.id) : true
          const isDimmed = hoveredNode && !isConnected
          const col =
            n.type === "CUSTOMER"
              ? "var(--accent)"
              : n.type === "DEVICE"
              ? "#06b6d4"
              : n.type === "DEALER"
              ? "#8b5cf6"
              : n.type === "BANK_ACCOUNT"
              ? "#f59e0b"
              : "#94a3b8"

          return (
            <g
              key={n.id}
              onMouseEnter={() => setHoveredNode(n.id)}
              onMouseLeave={() => setHoveredNode(null)}
              opacity={isDimmed ? 0.2 : 1}
              style={{
                cursor: "pointer",
                transition: "all 0.3s cubic-bezier(0.16, 1, 0.3, 1)",
              }}
            >
              {isHovered && (
                <circle
                  cx={p.x}
                  cy={p.y}
                  r={n.type === "CUSTOMER" ? 25 : 18}
                  fill="none"
                  stroke={col}
                  strokeWidth="2"
                  strokeDasharray="3 3"
                  style={{ animation: "pulseGlow 1.5s infinite" }}
                />
              )}
              <circle
                cx={p.x}
                cy={p.y}
                r={isHovered ? (n.type === "CUSTOMER" ? 20 : 14) : n.type === "CUSTOMER" ? 16 : 11}
                fill={col}
                stroke="var(--card)"
                strokeWidth="2"
                style={{
                  transition: "all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)",
                  filter: isHovered ? `drop-shadow(0 0 10px ${col})` : "none",
                }}
              />
              <text x={p.x} y={p.y + 3} textAnchor="middle" fontSize="7.5" fill="#fff" fontWeight="700">
                {n.type.slice(0, 3)}
              </text>
              <text
                x={p.x}
                y={p.y + 24}
                textAnchor="middle"
                fontSize="9"
                fontWeight={isHovered ? 700 : 500}
                fill="var(--text)"
              >
                {n.id.split(":")[1]?.slice(0, 8)}
              </text>
            </g>
          )
        })}
      </svg>
      <div className="muted" style={{ fontSize: 11, marginTop: 8 }}>
        💡 <b>Interactive:</b> Hover on any entity node to focus on its direct relationships and dim unlinked components.
      </div>
    </div>
  )
}

export function Customers() {
  const { data, loading, error, retry } = useFetch(() => api.customers(1, 20))
  if (loading) return <Card>Loading customers...</Card>
  if (error) return <ErrorState msg={`Unable to load customers. ${error}`} retry={retry} />
  if (!data?.items?.length) return <Empty msg="No customers found." />

  return (
    <Card>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <div>
          <b style={{ fontSize: 16 }}>Customers Registry</b>
          <div className="muted" style={{ fontSize: 12 }}>
            Applicant identities with KYC pan & device footprints
          </div>
        </div>
        <span className="muted" style={{ fontSize: 12, fontWeight: 600 }}>
          {data.total} total • Synthetic Seed Data
        </span>
      </div>
      <div style={{ overflowX: "auto" }}>
        <table className="table">
          <thead>
            <tr>
              <th>Ref</th>
              <th>Full Name</th>
              <th>Occupation</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((c: any) => (
              <tr key={c.customer_id}>
                <td style={{ fontWeight: 700, color: "var(--accent)" }}>{c.customer_ref}</td>
                <td style={{ fontWeight: 600 }}>{c.full_name}</td>
                <td className="muted">{c.occupation}</td>
                <td>
                  <Badge level={c.customer_status === "ACTIVE" ? "LOW" : c.customer_status === "SUSPECT" ? "HIGH" : "CRITICAL"} />
                </td>
                <td>
                  <Link to="/analyze" className="btn ghost" style={{ padding: "4px 10px", fontSize: 11.5 }}>
                    Analyze →
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}

export function Applications() {
  const { data, loading, error, retry } = useFetch(() => api.applications(1, 20))
  if (loading) return <Card>Loading applications...</Card>
  if (error) return <ErrorState msg={`Unable to load applications. ${error}`} retry={retry} />
  if (!data?.items?.length) return <Empty msg="No applications found." />

  return (
    <Card>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <div>
          <b style={{ fontSize: 16 }}>Loan Applications</b>
          <div className="muted" style={{ fontSize: 12 }}>
            Real-time pipeline with velocity burst flags
          </div>
        </div>
        <span className="muted" style={{ fontSize: 12, fontWeight: 600 }}>
          {data.total} total
        </span>
      </div>
      <div style={{ overflowX: "auto" }}>
        <table className="table">
          <thead>
            <tr>
              <th>App Ref</th>
              <th>Status</th>
              <th>Requested Amount</th>
              <th>Timestamp</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((a: any) => (
              <tr key={a.application_id}>
                <td style={{ fontFamily: "monospace", fontWeight: 700 }}>{a.application_ref}</td>
                <td>
                  <Badge level={a.application_status === "APPROVED" ? "LOW" : a.application_status === "REJECTED" ? "CRITICAL" : "MEDIUM"} />
                </td>
                <td style={{ fontWeight: 700 }}>₹{Number(a.requested_amount).toLocaleString()}</td>
                <td className="muted" style={{ fontSize: 11.5 }}>
                  {new Date(a.application_timestamp).toLocaleString()}
                </td>
                <td>
                  <Link to="/analyze" className="btn ghost" style={{ padding: "4px 10px", fontSize: 11.5 }}>
                    Inspect
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}

export function Loans() {
  const { data, loading, error, retry } = useFetch(() => api.loans(1, 20))
  if (loading) return <Card>Loading loans...</Card>
  if (error) return <ErrorState msg={`Unable to load loans. ${error}`} retry={retry} />
  if (!data?.items?.length) return <Empty msg="No loans found." />

  return (
    <Card>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <div>
          <b style={{ fontSize: 16 }}>Disbursed Loans</b>
          <div className="muted" style={{ fontSize: 12 }}>
            Active & Closed Loan Accounts with cross-collateral tracking
          </div>
        </div>
        <span className="muted" style={{ fontSize: 12, fontWeight: 600 }}>
          {data.total} total
        </span>
      </div>
      <div style={{ overflowX: "auto" }}>
        <table className="table">
          <thead>
            <tr>
              <th>Loan Ref</th>
              <th>Sanctioned Amount</th>
              <th>Status</th>
              <th>Customer</th>
            </tr>
          </thead>
          <tbody>
            {data.items.map((l: any) => (
              <tr key={l.loan_id}>
                <td style={{ fontFamily: "monospace", fontWeight: 700 }}>{l.loan_account_ref}</td>
                <td style={{ fontWeight: 700 }}>₹{Number(l.sanctioned_amount).toLocaleString()}</td>
                <td>
                  <Badge level={l.loan_status === "ACTIVE" ? "LOW" : l.loan_status === "CLOSED" ? "MEDIUM" : "HIGH"} />
                </td>
                <td className="muted" style={{ fontSize: 12 }}>
                  {l.customer_id?.slice(0, 8)}...
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}

export function Devices() {
  return (
    <div style={{ display: "grid", gap: 16 }}>
      <Card>
        <b style={{ fontSize: 16 }}>📱 Shared Device Intelligence</b>
        <div className="muted" style={{ marginTop: 6, fontSize: 13.5 }}>
          Shared hardware fingerprints and IMEI collisions form the strongest lending fraud signals.
          Cluster <b>F-1001</b> and <b>F-9001</b> share a single Xiaomi Redmi Note 12 across 8 unrelated applicants via Dealer DL003.
        </div>
        <div
          style={{
            marginTop: 14,
            padding: 14,
            background: "var(--bg)",
            borderRadius: 12,
            border: "1px solid var(--border)",
            fontSize: 13,
          }}
        >
          API Route: <code>GET /api/devices/{`{device_id}`}/customers</code> — inspect via Analyze → DEVICE.
        </div>
      </Card>
    </div>
  )
}

export function Dealers() {
  const { data, loading, error, retry } = useFetch(() => api.dealers(1, 20))
  if (loading) return <Card>Loading dealers...</Card>
  if (error) return <ErrorState msg={`Unable to load dealers. ${error}`} retry={retry} />
  if (!data?.items?.length) return <Empty msg="No dealers found." />

  return (
    <Card>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <div>
          <b style={{ fontSize: 16 }}>Dealers & DSAs</b>
          <div className="muted" style={{ fontSize: 12 }}>
            Sourcing partner channels & anomaly burst rates
          </div>
        </div>
        <span className="muted" style={{ fontSize: 12, fontWeight: 600 }}>
          {data.total} total
        </span>
      </div>
      <div style={{ overflowX: "auto" }}>
        <table className="table">
          <thead>
            <tr>
              <th>Dealer Code</th>
              <th>Channel Name</th>
              <th>Type</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {(data.items || []).map((x: any) => (
              <tr key={x.dealer_id}>
                <td style={{ fontWeight: 700, color: "var(--accent)" }}>{x.dealer_code}</td>
                <td style={{ fontWeight: 600 }}>{x.dealer_name}</td>
                <td>{x.dealer_type}</td>
                <td>
                  <Badge level={x.dealer_status === "ACTIVE" ? "LOW" : x.dealer_status === "SUSPENDED" ? "CRITICAL" : "HIGH"} />
                </td>
                <td>
                  <Link to="/analyze" className="btn ghost" style={{ padding: "4px 10px", fontSize: 11.5 }}>
                    Inspect
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}

export function Signals() {
  const { data, loading, error, retry } = useFetch(() => api.signalsList())
  if (loading) return <Card>Loading fraud signals...</Card>
  if (error) return <ErrorState msg={`Unable to load signals. ${error}`} retry={retry} />
  const items = (data as any)?.items ?? []
  if (!items.length) return <Empty msg="No fraud signals found." />

  const uniq = new Map<string, any>()
  items.forEach((s: any) => {
    if (!uniq.has(s.signal_type) || s.score > uniq.get(s.signal_type).score) uniq.set(s.signal_type, s)
  })
  const top = [...uniq.values()].sort((a, b) => b.score - a.score).slice(0, 12)

  return (
    <Card>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <div>
          <b style={{ fontSize: 16 }}>Detected Fraud Signals</b>
          <div className="muted" style={{ fontSize: 12 }}>
            Rule and graph-based heuristic anomalies
          </div>
        </div>
        <span className="muted" style={{ fontSize: 12, fontWeight: 600 }}>
          {uniq.size} distinct rules
        </span>
      </div>
      <div style={{ overflowX: "auto" }}>
        <table className="table">
          <thead>
            <tr>
              <th>Signal Type</th>
              <th>Severity</th>
              <th>Risk Score</th>
              <th>Entity</th>
              <th>Explanation</th>
            </tr>
          </thead>
          <tbody>
            {top.map((s: any) => (
              <tr key={s.signal_id}>
                <td style={{ fontWeight: 700 }}>{s.signal_type}</td>
                <td>
                  <Badge level={s.severity} />
                </td>
                <td style={{ fontWeight: 800 }}>{s.score}</td>
                <td className="muted" style={{ fontSize: 12 }}>
                  {s.entity_type}
                </td>
                <td className="muted" style={{ fontSize: 12 }}>
                  {s.explanation}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}

export function Alerts() {
  const { data, loading, error, retry } = useFetch(() => api.alerts())
  if (loading) return <Card>Loading alerts...</Card>
  if (error) return <ErrorState msg={`Unable to load alerts. ${error}`} retry={retry} />
  const items = (data as any)?.items ?? (Array.isArray(data) ? data : [])
  if (!items.length) return <Empty msg="No active fraud alerts" />

  return (
    <Card>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
        <div>
          <b style={{ fontSize: 16 }}>Active Fraud Alerts</b>
          <div className="muted" style={{ fontSize: 12 }}>
            High-risk syndicate alerts escalated for investigation
          </div>
        </div>
        <span className="muted" style={{ fontSize: 12, fontWeight: 600 }}>
          {items.length} total
        </span>
      </div>
      <div className="focus-group" style={{ display: "grid", gap: 10 }}>
        {items.slice(0, 10).map((a: any) => (
          <div
            key={a.alert_id}
            className="card"
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              padding: "14px 16px",
            }}
          >
            <div>
              <div style={{ fontWeight: 700, fontSize: 14 }}>{a.alert_type.replace(/_/g, " ")}</div>
              <div className="muted" style={{ fontSize: 12, marginTop: 2 }}>
                {a.alert_ref} • {new Date(a.generated_at).toLocaleDateString()} • Status: <b>{a.alert_status}</b>
              </div>
            </div>
            <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
              <Badge level={a.severity} />
              <Link to="/analyze" className="btn ghost" style={{ padding: "5px 12px", fontSize: 12 }}>
                Analyze
              </Link>
            </div>
          </div>
        ))}
      </div>
    </Card>
  )
}

export function Investigations() {
  const { data, loading, error, retry } = useFetch(() => api.investigations())
  if (loading) return <Card>Loading investigations...</Card>
  if (error) return <ErrorState msg={`Unable to load investigations. ${error}`} retry={retry} />
  const items = (data as any)?.items ?? []

  return (
    <Card>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <div>
          <b style={{ fontSize: 16 }}>Investigations Audit Trail</b>
          <div className="muted" style={{ fontSize: 12 }}>
            Active fraud case management & field visits
          </div>
        </div>
        <span className="muted" style={{ fontSize: 12, fontWeight: 600 }}>
          {items.length} cases
        </span>
      </div>
      <div style={{ overflowX: "auto" }}>
        <table className="table">
          <thead>
            <tr>
              <th>Case ID</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Investigator</th>
              <th>Notes / Action</th>
            </tr>
          </thead>
          <tbody>
            {items.slice(0, 10).map((x: any) => (
              <tr key={x.investigation_id}>
                <td style={{ fontFamily: "monospace", fontSize: 12, fontWeight: 700 }}>
                  {x.investigation_id.slice(0, 8)}…
                </td>
                <td>
                  <Badge level={x.investigation_status === "OPEN" ? "HIGH" : x.investigation_status === "CLOSED" ? "LOW" : "CRITICAL"} />
                </td>
                <td>
                  <Badge level={x.priority === "URGENT" ? "CRITICAL" : x.priority === "HIGH" ? "HIGH" : "MEDIUM"} />
                </td>
                <td style={{ fontWeight: 600 }}>{x.investigator_ref}</td>
                <td className="muted" style={{ fontSize: 12 }}>
                  {x.notes}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}

export function Networks() {
  const { data, loading, error, retry } = useFetch(() => api.networkComponents())
  if (loading) return <Card>Loading network...</Card>
  if (error) return <ErrorState msg={`Unable to load network. ${error}`} retry={retry} />
  const comps = (data as any)?.components ?? []
  if (!comps.length) return <Empty msg="No network components detected." />

  const biggest = [...comps].sort((a, b) => b.size - a.size)[0]
  const nodes = (biggest.members || []).slice(0, 9).map((m: string) => {
    const [t] = m.split(":")
    return { id: m, type: t }
  })
  const edges = nodes.slice(1).map((n) => ({ source: nodes[0].id, target: n.id, label: "SHARED_DEVICE" }))

  return (
    <div style={{ display: "grid", gap: 18 }}>
      <Card>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <div>
            <b style={{ fontSize: 16 }}>Network Intelligence Graph Explorer</b>
            <div className="muted" style={{ fontSize: 12 }}>
              Largest connected component • {biggest.size} entities
            </div>
          </div>
          <span className="muted" style={{ fontSize: 12, fontWeight: 600 }}>
            {comps.length} components total
          </span>
        </div>
        <InteractiveNetworkMap nodes={nodes} edges={edges} />
      </Card>

      <Card>
        <b style={{ fontSize: 15 }}>Connected Components Topology</b>
        <div className="muted" style={{ fontSize: 12, marginBottom: 10 }}>
          Ranked by cluster member volume
        </div>
        <div style={{ overflowX: "auto" }}>
          <table className="table">
            <thead>
              <tr>
                <th>Component</th>
                <th>Entity Count</th>
                <th>Sample Members</th>
              </tr>
            </thead>
            <tbody>
              {comps.slice(0, 8).map((c: any, i: number) => (
                <tr key={i}>
                  <td style={{ fontWeight: 700, color: "var(--accent)" }}>Component #{i + 1}</td>
                  <td>
                    <span style={{ fontWeight: 800 }}>{c.size}</span> entities
                  </td>
                  <td
                    className="muted"
                    style={{
                      fontSize: 11.5,
                      maxWidth: 360,
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                  >
                    {(c.members || []).slice(0, 4).join(" • ")}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}

export function RiskPage() {
  return (
    <div style={{ display: "grid", gap: 18 }}>
      <Card>
        <b style={{ fontSize: 16 }}>Swarm Collective Risk Engine</b>
        <div className="muted" style={{ fontSize: 13, marginTop: 4 }}>
          Collective risk combines individual applicant KYC, graph network exposure, and machine-learning fraud probability.
        </div>
        <div
          style={{
            marginTop: 14,
            padding: 16,
            background: "var(--bg)",
            borderRadius: 14,
            border: "1px solid var(--border)",
            fontFamily: "monospace",
            fontSize: 14,
            fontWeight: 700,
            textAlign: "center",
            color: "var(--accent)",
          }}
        >
          Collective Risk = 0.25 × Individual + 0.45 × Network + 0.30 × ML
        </div>
      </Card>

      <div className="grid3 focus-group">
        <Card>
          <div className="muted" style={{ fontWeight: 700, fontSize: 12 }}>
            INDIVIDUAL WEIGHT (25%)
          </div>
          <div className="kpi">0.25</div>
          <div className="muted" style={{ fontSize: 12 }}>
            Applicant-level attributes, income band, occupation risk, KYC validity.
          </div>
        </Card>
        <Card>
          <div className="muted" style={{ fontWeight: 700, fontSize: 12 }}>
            NETWORK WEIGHT (45%)
          </div>
          <div className="kpi">0.45</div>
          <div className="muted" style={{ fontSize: 12 }}>
            Shared hardware fingerprints, dealer bursts, common bank rings, community density.
          </div>
        </Card>
        <Card>
          <div className="muted" style={{ fontWeight: 700, fontSize: 12 }}>
            ML CLASSIFIER (30%)
          </div>
          <div className="kpi">0.30</div>
          <div className="muted" style={{ fontSize: 12 }}>
            GradientBoosting inference score on 7 normalized graph and behavioral features.
          </div>
        </Card>
      </div>

      <Card>
        <b style={{ fontSize: 15 }}>Risk Score Thresholds & SLA</b>
        <div className="focus-group" style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 12, marginTop: 12 }}>
          {[
            { l: "LOW", c: "#22c55e", r: "0–30", desc: "Automated instant approval" },
            { l: "MEDIUM", c: "#eab308", r: "30–60", desc: "Secondary KYC check" },
            { l: "HIGH", c: "#f97316", r: "60–80", desc: "Manual underwriting review" },
            { l: "CRITICAL", c: "#ef4444", r: "80–100", desc: "Immediate freeze & fraud alert" },
          ].map((x) => (
            <div key={x.l} className="card" style={{ textAlign: "center", padding: 14 }}>
              <div style={{ width: 14, height: 14, background: x.c, borderRadius: "50%", margin: "0 auto 8px", boxShadow: `0 0 10px ${x.c}` }} />
              <div style={{ fontWeight: 800, fontSize: 14 }}>{x.l}</div>
              <div className="muted" style={{ fontWeight: 700, fontSize: 12 }}>
                {x.r}
              </div>
              <div className="muted" style={{ fontSize: 11, marginTop: 4 }}>
                {x.desc}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  )
}
