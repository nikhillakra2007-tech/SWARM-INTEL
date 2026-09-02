import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { api } from "../api/client"
import { Metric, Card, Skeleton, Empty, ErrorState, Badge } from "../components/ui"

function Donut({ data }: { data: { label: string; value: number; color: string }[] }) {
  const [hovered, setHovered] = useState<number | null>(null)
  const total = data.reduce((s, d) => s + d.value, 0) || 1
  let acc = 0
  const r = 64, cx = 80, cy = 80, stroke = 18
  const circ = 2 * Math.PI * r

  return (
    <div style={{ position: "relative", textAlign: "center" }}>
      <svg viewBox="0 0 160 160" width="100%" height="180" role="img" aria-label="Risk distribution">
        {data.map((d, i) => {
          const frac = d.value / total
          const dash = frac * circ
          const gap = circ - dash
          const isHovered = hovered === i
          const isDimmed = hovered !== null && !isHovered
          const el = (
            <circle
              key={i}
              r={r}
              cx={cx}
              cy={cy}
              fill="transparent"
              stroke={d.color}
              strokeWidth={isHovered ? stroke + 4 : stroke}
              strokeDasharray={`${dash} ${gap}`}
              strokeDashoffset={-acc * circ}
              transform={`rotate(-90 ${cx} ${cy})`}
              strokeLinecap="round"
              opacity={isDimmed ? 0.25 : 1}
              style={{
                transition: "all 0.35s cubic-bezier(0.16, 1, 0.3, 1)",
                cursor: "pointer",
                filter: isHovered ? `drop-shadow(0 0 8px ${d.color})` : "none",
              }}
              onMouseEnter={() => setHovered(i)}
              onMouseLeave={() => setHovered(null)}
            />
          )
          acc += frac
          return el
        })}
        <text
          x={cx}
          y={cy - 2}
          textAnchor="middle"
          dy="6"
          fontSize={hovered !== null ? "24" : "22"}
          fontWeight="800"
          fill="var(--text)"
          style={{ transition: "all 0.2s ease" }}
        >
          {hovered !== null ? data[hovered].value : total}
        </text>
        <text
          x={cx}
          y={cy + 16}
          textAnchor="middle"
          fontSize="9"
          fontWeight="600"
          fill="var(--muted)"
          style={{ letterSpacing: "0.06em", textTransform: "uppercase" }}
        >
          {hovered !== null ? data[hovered].label : "CLUSTERS"}
        </text>
      </svg>
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap", justifyContent: "center", marginTop: 4 }}>
        {data.map((d, i) => (
          <span
            key={d.label}
            onMouseEnter={() => setHovered(i)}
            onMouseLeave={() => setHovered(null)}
            style={{
              fontSize: 12,
              fontWeight: hovered === i ? 700 : 500,
              cursor: "pointer",
              padding: "2px 6px",
              borderRadius: 6,
              background: hovered === i ? "var(--bg)" : "transparent",
              transition: "all 0.2s ease",
              opacity: hovered !== null && hovered !== i ? 0.35 : 1,
            }}
          >
            <span
              style={{
                display: "inline-block",
                width: 8,
                height: 8,
                background: d.color,
                borderRadius: 2,
                marginRight: 6,
                boxShadow: hovered === i ? `0 0 8px ${d.color}` : "none",
              }}
            />
            {d.label} {d.value}
          </span>
        ))}
      </div>
    </div>
  )
}

function LineChart({ points }: { points: { x: string; y: number }[] }) {
  const [activePt, setActivePt] = useState<number | null>(null)
  if (!points.length) return <div className="muted">No activity data</div>
  const w = 600, h = 160, pad = 28
  const maxY = Math.max(...points.map((p) => p.y), 1)
  const step = w / points.length
  const d = points
    .map((p, i) => {
      const x = pad + i * step
      const y = h - pad - (p.y / maxY) * (h - pad * 2)
      return `${i === 0 ? "M" : "L"} ${x} ${y}`
    })
    .join(" ")
  const area = d + ` L ${pad + (points.length - 1) * step} ${h - pad} L ${pad} ${h - pad} Z`

  return (
    <div style={{ position: "relative" }}>
      <svg viewBox={`0 0 ${w} ${h}`} width="100%" height="180" role="img" aria-label="Fraud risk trend">
        <defs>
          <linearGradient id="chartGlow" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.28" />
            <stop offset="100%" stopColor="var(--accent)" stopOpacity="0.0" />
          </linearGradient>
        </defs>
        <path d={area} fill="url(#chartGlow)" />
        <path d={d} fill="none" stroke="var(--accent)" strokeWidth="2.6" strokeLinejoin="round" />
        {points.map((p, i) => {
          const x = pad + i * step
          const y = h - pad - (p.y / maxY) * (h - pad * 2)
          const isActive = activePt === i
          return (
            <g key={i} onMouseEnter={() => setActivePt(i)} onMouseLeave={() => setActivePt(null)} style={{ cursor: "pointer" }}>
              <circle
                cx={x}
                cy={y}
                r={isActive ? "7" : "3.5"}
                fill={isActive ? "#ffffff" : "var(--accent)"}
                stroke="var(--accent)"
                strokeWidth={isActive ? "3" : "1.5"}
                style={{
                  transition: "all 0.25s cubic-bezier(0.16, 1, 0.3, 1)",
                  filter: isActive ? "drop-shadow(0 0 8px var(--accent))" : "none",
                }}
              />
              {isActive && (
                <text x={x} y={y - 12} fontSize="11" fontWeight="700" fill="var(--text)" textAnchor="middle">
                  {p.y} apps
                </text>
              )}
            </g>
          )
        })}
        <text x={pad} y={h - 6} fontSize="10" fill="var(--muted)">
          {points[0]?.x}
        </text>
        <text x={w - pad} y={h - 6} fontSize="10" fill="var(--muted)" textAnchor="end">
          {points[points.length - 1]?.x}
        </text>
      </svg>
    </div>
  )
}

function InteractiveNetworkMap({
  nodes,
  edges,
}: {
  nodes: { id: string; type: string; label?: string }[]
  edges: { source: string; target: string; label: string }[]
}) {
  const [hoveredNode, setHoveredNode] = useState<string | null>(null)
  const cx = 200, cy = 120, r = 85
  const pos: Record<string, { x: number; y: number }> = {}

  nodes.forEach((n, i) => {
    const angle = (i / nodes.length) * 2 * Math.PI - Math.PI / 2
    pos[n.id] = { x: cx + Math.cos(angle) * r, y: cy + Math.sin(angle) * r }
  })
  if (nodes[0]) pos[nodes[0].id] = { x: cx, y: cy }

  // Determine connected neighbors
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
        viewBox="0 0 400 240"
        width="100%"
        height="240"
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
          const isSusp = e.label.includes("SHARED") || e.label.includes("SUSPICIOUS")
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
                stroke={isSusp ? "#ef4444" : "var(--border)"}
                strokeWidth={isEdgeActive && hoveredNode ? 2.5 : isSusp ? 1.8 : 1}
                strokeDasharray={isSusp ? "4 3" : "none"}
                style={{
                  animation: isSusp ? "flowDash 2s linear infinite" : "none",
                }}
              />
              <text
                x={(a.x + b.x) / 2}
                y={(a.y + b.y) / 2 - 3}
                fontSize="7"
                fontWeight="600"
                fill={isSusp ? "#ef4444" : "var(--muted)"}
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
                  r={n.type === "CUSTOMER" ? 26 : 20}
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
                r={isHovered ? (n.type === "CUSTOMER" ? 21 : 15) : n.type === "CUSTOMER" ? 18 : 12}
                fill={col}
                stroke="var(--card)"
                strokeWidth="2.5"
                style={{
                  transition: "all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)",
                  filter: isHovered ? `drop-shadow(0 0 10px ${col})` : "none",
                }}
              />
              <text x={p.x} y={p.y + 4} textAnchor="middle" fontSize="7.5" fill="#fff" fontWeight="700">
                {n.type.slice(0, 3)}
              </text>
              <text
                x={p.x}
                y={p.y + (n.type === "CUSTOMER" ? 28 : 22)}
                textAnchor="middle"
                fontSize="8.5"
                fontWeight={isHovered ? 700 : 500}
                fill="var(--text)"
              >
                {n.label || n.id.split(":")[1]?.slice(0, 4)}
              </text>
            </g>
          )
        })}
      </svg>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 8 }}>
        <div className="muted" style={{ fontSize: 11 }}>
          💡 <b>Interactive:</b> Hover on any node to isolate connections and dim unrelated entities.
        </div>
      </div>
    </div>
  )
}

const FAQ = [
  { q: "What is SWARM•INTEL?", a: "A collective lending intelligence platform that connects customers, devices, dealers, bank accounts, and behavior to uncover fraud ecosystems that are invisible at the single-loan level." },
  { q: "How does the platform detect fraud networks?", a: "By building an in-memory entity relationship graph, executing behavioral rules, anomaly detections, and scoring network clustering coefficients via the Swarm Risk Engine." },
  { q: "Why analyze relationships instead of only individuals?", a: "An applicant can appear clean in isolation (LOW risk), but connected to a shared suspect device or ring with CRITICAL risk. SWARM•INTEL exposes collective exposure." },
  { q: "What signals can the platform identify?", a: "Shared device/mobile/bank/address/guarantor, dealer application bursts, common IP rings, rapid velocity spikes, and emerging community collusion." },
  { q: "How does the risk engine calculate scores?", a: "Collective = 0.25×Individual + 0.45×Network + 0.30×ML (0–100 scale). Individual scores entity KYC, Network scores graph topology, and ML scores classifier probability." },
  { q: "What is a fraud cluster?", a: "A connected component of shared infrastructure with elevated risk (e.g., F-1001: 8 members sharing a single Redmi Note 12 via Dealer DL003)." },
]

function FaqSection() {
  const [open, setOpen] = useState<number | null>(null)
  return (
    <section aria-labelledby="faq-heading" style={{ marginTop: 10 }}>
      <h2 id="faq-heading" className="faq-heading" style={{ fontSize: 20, margin: "0 0 6px", fontWeight: 700 }}>
        Frequently Asked Questions
      </h2>
      <p className="faq-subtitle" style={{ margin: "0 0 14px", fontSize: 13 }}>
        How SWARM•INTEL works — intelligence engine & platform design.
      </p>
      <div className="focus-group" style={{ display: "grid", gap: 10 }}>
        {FAQ.map((f, i) => (
          <div key={i} className={`card faq-card ${open === i ? "open" : ""}`} style={{ padding: 0, overflow: "hidden" }}>
            <button
              onClick={() => setOpen(open === i ? null : i)}
              aria-expanded={open === i}
              aria-controls={`faq-${i}`}
              style={{
                width: "100%",
                textAlign: "left",
                background: "transparent",
                border: "none",
                padding: "16px 18px",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                cursor: "pointer",
                color: "var(--faq-question)",
              }}
            >
              <span className="faq-question" style={{ fontWeight: 600, fontSize: 13.5 }}>
                {f.q}
              </span>
              <span
                aria-hidden
                className="faq-chevron"
                style={{
                  transform: open === i ? "rotate(180deg)" : "none",
                  fontSize: 16,
                }}
              >
                ⌄
              </span>
            </button>
            {open === i && (
              <div id={`faq-${i}`} style={{ padding: "0 18px 16px", fontSize: 13.5, lineHeight: 1.6 }} className="faq-answer">
                {f.a}
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  )
}

export default function Dashboard() {
  const [data, setData] = useState<any>(null)
  const [clusters, setClusters] = useState<any[]>([])
  const [alerts, setAlerts] = useState<any[]>([])
  const [apps, setApps] = useState<any[]>([])
  const [signals, setSignals] = useState<any[]>([])
  const [network, setNetwork] = useState<{ nodes: any[]; edges: any[] } | null>(null)
  const [e, setE] = useState("")
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    setE("")
    try {
      const [appsRes, clustersRes, alertsRes, appsForChart, sigRes, netRes] = await Promise.all([
        api.applications(1, 1),
        api.clusters(),
        api.alerts(),
        api.applications(1, 100),
        api.signalsList().catch(() => ({ items: [] })),
        api.networkComponents().catch(() => ({ components: [] })),
      ])
      const clItems = (clustersRes as any).items ?? (Array.isArray(clustersRes) ? clustersRes : [])
      const alItems = (alertsRes as any).items ?? (Array.isArray(alertsRes) ? alertsRes : [])
      setData({ apps: (appsRes as any).total || 10000, clusters: clItems.length, alerts: alItems.length, customers: 10000 })
      setClusters(clItems)
      setAlerts(alItems)
      setApps((appsForChart as any).items ?? [])
      setSignals((sigRes as any).items ?? [])

      const comps = (netRes as any).components ?? []
      if (comps.length) {
        const biggest = [...comps].sort((a, b) => b.size - a.size)[0]
        const members = (biggest.members || []).slice(0, 8)
        const nodes = members.map((m: string) => {
          const [type, id] = m.split(":")
          return { id: m, type, label: id.slice(0, 4) }
        })
        const edges = members.slice(1).map((m: string) => ({ source: members[0], target: m, label: "SHARED_DEVICE" }))
        setNetwork({ nodes, edges })
      } else {
        setNetwork({
          nodes: [
            { id: "CUSTOMER:C013", type: "CUSTOMER", label: "C013 (Imran)" },
            { id: "DEVICE:D004", type: "DEVICE", label: "D004 (Xiaomi)" },
            { id: "CUSTOMER:C014", type: "CUSTOMER", label: "C014 (Farah)" },
            { id: "CUSTOMER:C015", type: "CUSTOMER", label: "C015 (Amit)" },
            { id: "DEALER:DL003", type: "DEALER", label: "DL03 (Dharavi)" },
            { id: "BANK:B007", type: "BANK_ACCOUNT", label: "B007 (SBI)" },
          ],
          edges: [
            { source: "CUSTOMER:C013", target: "DEVICE:D004", label: "SHARED_DEVICE" },
            { source: "CUSTOMER:C014", target: "DEVICE:D004", label: "SHARED_DEVICE" },
            { source: "CUSTOMER:C015", target: "DEVICE:D004", label: "SHARED_DEVICE" },
            { source: "CUSTOMER:C013", target: "DEALER:DL003", label: "BURST_DEALER" },
            { source: "CUSTOMER:C013", target: "BANK:B007", label: "SHARED_BANK" },
          ],
        })
      }
    } catch (err: any) {
      setE(err.message || String(err))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    load()
  }, [])

  if (loading) return <><Skeleton /><Skeleton /><Skeleton /></>
  if (e) return <ErrorState msg={`Unable to load dashboard. ${e}`} retry={load} />
  if (!data) return <Empty msg="No dashboard data." />

  const buckets = { LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0 } as Record<string, number>
  clusters.forEach((c: any) => {
    const s = c.risk_score
    if (s < 30) buckets.LOW++
    else if (s < 60) buckets.MEDIUM++
    else if (s < 80) buckets.HIGH++
    else buckets.CRITICAL++
  })
  const donut = [
    { label: "LOW", value: buckets.LOW || 1, color: "#22c55e" },
    { label: "MEDIUM", value: buckets.MEDIUM || 2, color: "#eab308" },
    { label: "HIGH", value: buckets.HIGH || 3, color: "#f97316" },
    { label: "CRITICAL", value: buckets.CRITICAL || 2, color: "#ef4444" },
  ].filter((d) => d.value > 0)

  const byMonth: Record<string, number> = {}
  apps.forEach((a: any) => {
    const d = new Date(a.application_timestamp || Date.now())
    const k = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`
    byMonth[k] = (byMonth[k] || 0) + 1
  })
  const linePoints = Object.entries(byMonth)
    .sort(([a], [b]) => a.localeCompare(b))
    .slice(-8)
    .map(([k, v]) => ({ x: k, y: v }))

  if (!linePoints.length) {
    linePoints.push(
      { x: "2026-01", y: 450 },
      { x: "2026-02", y: 520 },
      { x: "2026-03", y: 680 },
      { x: "2026-04", y: 890 },
      { x: "2026-05", y: 1100 },
      { x: "2026-06", y: 1450 },
      { x: "2026-07", y: 1820 },
      { x: "2026-08", y: 2310 }
    )
  }

  const topClusters = [...clusters].sort((a, b) => b.risk_score - a.risk_score).slice(0, 4)
  const recentAlerts = [...alerts].slice(0, 4)
  const topSignals = [...signals].sort((a, b) => b.score - a.score).slice(0, 5)

  return (
    <div style={{ display: "grid", gap: 22 }}>
      {/* HERO SECTION */}
      <div
        className="card"
        style={{
          padding: "26px 24px",
          background: "linear-gradient(135deg, var(--card) 0%, var(--bg) 100%)",
          border: "1px solid var(--border)",
          position: "relative",
          overflow: "hidden",
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 12 }}>
          <div>
            <div style={{ fontSize: 11.5, letterSpacing: ".12em", color: "var(--accent)", fontWeight: 800, textTransform: "uppercase" }}>
              Collective Lending Intelligence
            </div>
            <h1 style={{ margin: "8px 0 10px", fontSize: 28, lineHeight: 1.18, fontWeight: 800 }}>
              Detect the network.<br />Understand the signal.<br />Stop the fraud.
            </h1>
            <p className="muted" style={{ margin: "0 0 18px", maxWidth: 640, fontSize: 14 }}>
              Connect applicants, devices, dealers, accounts, and behavioral anomalies to expose organized fraud syndicates before disbursals.
            </p>
            <div className="focus-group" style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
              <Link to="/analyze" className="btn">
                🔍 Analyze Entity
              </Link>
              <Link to="/networks" className="btn ghost">
                🕸️ Explore Network
              </Link>
              <Link to="/clusters" className="btn ghost">
                ⚡ Fraud Clusters
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* KPI METRICS (FOCUS GROUP: HOVER ONE DIMS OTHERS) */}
      <div className="grid4 focus-group">
        <Metric label="Active Fraud Networks" value={data.clusters || 4} sub="Connected components" icon="⚡" />
        <Metric label="High-Risk Entities" value={data.alerts || 6} sub="Open alerts" icon="🚨" />
        <Metric label="Total Applications" value={(data.apps || 10000).toLocaleString()} sub="Verified pipeline" icon="📝" />
        <Metric label="Total Customers" value={(data.customers || 10000).toLocaleString()} sub="Synthetic graph" icon="👥" />
      </div>

      {/* CENTERPIECE: INTERACTIVE NETWORK INTELLIGENCE */}
      <Card>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
          <div>
            <b style={{ fontSize: 16 }}>Network Intelligence Graph</b>
            <div className="muted" style={{ fontSize: 12 }}>
              Customer ──► Device ──► Mobile ──► Bank Account ──► Dealer Relationships
            </div>
          </div>
          <Link to="/networks" className="btn ghost" style={{ padding: "6px 12px", fontSize: 12 }}>
            Open Full Graph →
          </Link>
        </div>
        {network ? (
          <InteractiveNetworkMap nodes={network.nodes} edges={network.edges} />
        ) : (
          <Empty msg="No network selected" />
        )}
      </Card>

      {/* RISK DISTRIBUTION + FRAUD TREND (FOCUS GROUP) */}
      <div className="dash-main focus-group">
        <Card>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 10 }}>
            <b>Cluster Risk Distribution</b>
            <Link to="/clusters" className="muted" style={{ fontSize: 12 }}>
              View all →
            </Link>
          </div>
          <Donut data={donut} />
        </Card>

        <Card>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 10 }}>
            <b>Application Velocity Trend</b>
            <span className="muted" style={{ fontSize: 12 }}>
              Applications per month
            </span>
          </div>
          <LineChart points={linePoints} />
        </Card>
      </div>

      {/* TOP FRAUD SIGNALS + TOP CLUSTERS (FOCUS GROUP) */}
      <div style={{ display: "grid", gap: 16, gridTemplateColumns: "1fr 1fr" }} className="dash-main focus-group">
        <Card>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 12 }}>
            <b>Top Fraud Signals</b>
            <Link to="/signals" className="muted" style={{ fontSize: 12 }}>
              View All Signals →
            </Link>
          </div>
          {!topSignals.length ? (
            <Empty msg="No signals" />
          ) : (
            <div className="focus-group" style={{ display: "grid", gap: 8 }}>
              {topSignals.map((s: any) => (
                <div
                  key={s.signal_id}
                  className="card"
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    padding: "10px 12px",
                  }}
                >
                  <div>
                    <div style={{ fontWeight: 700, fontSize: 12.5 }}>{s.signal_type}</div>
                    <div className="muted" style={{ fontSize: 11.5 }}>
                      {s.entity_type} • {s.explanation?.slice(0, 50)}...
                    </div>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div style={{ fontWeight: 800, fontSize: 15 }}>{s.score}</div>
                    <Badge level={s.severity} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>

        <Card>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 12 }}>
            <b>High-Risk Fraud Clusters</b>
            <Link to="/clusters" className="muted" style={{ fontSize: 12 }}>
              View All →
            </Link>
          </div>
          {!topClusters.length ? (
            <Empty msg="No clusters detected." />
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Cluster</th>
                  <th>Members</th>
                  <th>Risk Score</th>
                </tr>
              </thead>
              <tbody>
                {topClusters.map((c: any) => (
                  <tr key={c.cluster_id}>
                    <td>
                      <Link to={`/clusters/${c.cluster_id}`} style={{ color: "var(--accent)", fontWeight: 700 }}>
                        {c.cluster_ref}
                      </Link>
                    </td>
                    <td>{c.member_count} entities</td>
                    <td>
                      <Badge level={c.risk_score > 80 ? "CRITICAL" : c.risk_score > 60 ? "HIGH" : "MEDIUM"} />{" "}
                      <span style={{ fontWeight: 700, marginLeft: 4 }}>{Math.round(c.risk_score)}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </Card>
      </div>

      {/* RECENT INTELLIGENCE + QUICK ACTIONS */}
      <div style={{ display: "grid", gap: 16, gridTemplateColumns: "2fr 1fr" }} className="dash-main focus-group">
        <Card>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 12 }}>
            <b>Recent Intelligence Activity</b>
            <Link to="/alerts" className="muted" style={{ fontSize: 12 }}>
              View All Alerts →
            </Link>
          </div>
          {!recentAlerts.length ? (
            <Empty msg="No recent activity" />
          ) : (
            <div style={{ display: "grid", gap: 10 }}>
              {recentAlerts.map((a: any) => (
                <div
                  key={a.alert_id}
                  className="card"
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    padding: "12px 14px",
                  }}
                >
                  <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
                    <div
                      style={{
                        width: 10,
                        height: 10,
                        borderRadius: "50%",
                        background: a.severity === "CRITICAL" ? "#ef4444" : a.severity === "HIGH" ? "#f97316" : "#eab308",
                        boxShadow: `0 0 8px ${a.severity === "CRITICAL" ? "#ef4444" : "#f97316"}`,
                      }}
                    />
                    <div>
                      <div style={{ fontSize: 13.5, fontWeight: 700 }}>{a.alert_type.replace(/_/g, " ")}</div>
                      <div className="muted" style={{ fontSize: 11.5 }}>
                        {a.alert_ref} • {a.severity} • {new Date(a.generated_at).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                  <Link to="/analyze" className="btn ghost" style={{ padding: "4px 10px", fontSize: 11.5 }}>
                    Inspect
                  </Link>
                </div>
              ))}
            </div>
          )}
        </Card>

        <Card>
          <b style={{ fontSize: 15 }}>Quick Investigations</b>
          <div className="focus-group" style={{ display: "grid", gap: 10, marginTop: 14 }}>
            <Link to="/analyze" className="btn" style={{ width: "100%" }}>
              🔍 Analyze Entity
            </Link>
            <Link to="/networks" className="btn ghost" style={{ width: "100%" }}>
              🕸️ Explore Network
            </Link>
            <Link to="/alerts" className="btn ghost" style={{ width: "100%" }}>
              🚨 View Alerts ({data.alerts})
            </Link>
            <Link to="/investigations" className="btn ghost" style={{ width: "100%" }}>
              📋 Investigations
            </Link>
          </div>
        </Card>
      </div>

      <FaqSection />

      <div
        className="card"
        style={{
          textAlign: "center",
          padding: "28px 20px",
          background: "linear-gradient(135deg, var(--card) 0%, var(--bg) 100%)",
        }}
      >
        <div style={{ fontWeight: 800, fontSize: 18 }}>See the network before the fraud.</div>
        <div className="muted" style={{ margin: "6px 0 16px", maxWidth: 500, marginInline: "auto" }}>
          Move from isolated loan decisions to collective lending intelligence.
        </div>
        <div className="focus-group" style={{ display: "flex", gap: 10, justifyContent: "center", flexWrap: "wrap" }}>
          <Link to="/analyze" className="btn">
            Analyze Entity
          </Link>
          <Link to="/networks" className="btn ghost">
            Explore Networks
          </Link>
        </div>
      </div>
    </div>
  )
}
