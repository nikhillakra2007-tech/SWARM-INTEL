import { useState, useEffect } from "react"
import { api } from "../api/client"
import { Card, Badge, Empty } from "../components/ui"

const ENTITY_TYPES = ["CUSTOMER", "DEVICE", "DEALER", "APPLICATION", "LOAN"] as const
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i
const LABELS: Record<string, string> = {
  CUSTOMER: "Customer ID",
  DEVICE: "Device ID",
  DEALER: "Dealer ID",
  APPLICATION: "Application ID",
  LOAN: "Loan ID",
}

export default function Analyze() {
  const [et, setEt] = useState<string>("CUSTOMER")
  const [id, setId] = useState("")
  const [customers, setCustomers] = useState<any[]>([])
  const [apps, setApps] = useState<any[]>([])
  const [dealers, setDealers] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [res, setRes] = useState<any>(null)
  const [err, setErr] = useState("")
  const [fieldErr, setFieldErr] = useState("")

  useEffect(() => {
    api.customers(1, 20)
      .then((r) => setCustomers(r.items || []))
      .catch(() => {})
  }, [])

  useEffect(() => {
    if (et === "DEALER")
      api.dealers(1, 20)
        .then((r) => setDealers(r.items || []))
        .catch(() => {})
    if (et === "APPLICATION")
      api.applications(1, 20)
        .then((r) => setApps(r.items || []))
        .catch(() => {})
  }, [et])

  const validate = (v: string) => {
    if (!v.trim()) return `Please enter a valid ${LABELS[et]}.`
    if (!UUID_RE.test(v.trim())) return `Please enter a valid UUID for ${LABELS[et]}.`
    return ""
  }

  const run = async (targetId?: string) => {
    const checkId = targetId || id
    const fe = validate(checkId)
    if (fe) {
      setFieldErr(fe)
      return
    }
    setFieldErr("")
    setLoading(true)
    setErr("")
    setRes(null)
    try {
      const r = await api.analyze(et, checkId.trim())
      setRes(r)
    } catch (e: any) {
      setErr(e.message ? e.message.slice(0, 500) : String(e))
    } finally {
      setLoading(false)
    }
  }

  const selectOptions = () => {
    if (et === "CUSTOMER")
      return customers.map((c) => (
        <option key={c.customer_id} value={c.customer_id}>
          {c.customer_ref} — {c.full_name} ({c.customer_status})
        </option>
      ))
    if (et === "DEALER")
      return dealers.map((d) => (
        <option key={d.dealer_id} value={d.dealer_id}>
          {d.dealer_code} — {d.dealer_name}
        </option>
      ))
    if (et === "APPLICATION")
      return apps.map((a) => (
        <option key={a.application_id} value={a.application_id}>
          {a.application_ref} — {a.application_status}
        </option>
      ))
    return null
  }
  const showSelect = et === "CUSTOMER" || et === "DEALER" || et === "APPLICATION"

  return (
    <div style={{ display: "grid", gap: 20 }}>
      <Card>
        <b style={{ fontSize: 16 }}>🔍 Deep Entity Fraud & Network Analyzer</b>
        <div className="muted" style={{ margin: "4px 0 16px", fontSize: 13 }}>
          Calculate collective risk decomposition (Individual + Graph Topology + ML Model) for any entity.
        </div>

        <div style={{ display: "grid", gap: 12, maxWidth: 640 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 2fr", gap: 10 }}>
            <div>
              <label className="muted" style={{ display: "block", marginBottom: 4, fontWeight: 600 }}>
                Entity Type
              </label>
              <select
                value={et}
                onChange={(e) => {
                  setEt(e.target.value)
                  setId("")
                  setRes(null)
                  setErr("")
                  setFieldErr("")
                }}
              >
                {ENTITY_TYPES.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>

            {showSelect && (
              <div>
                <label className="muted" style={{ display: "block", marginBottom: 4, fontWeight: 600 }}>
                  Quick Preset
                </label>
                <select
                  value={id}
                  onChange={(e) => {
                    setId(e.target.value)
                    setFieldErr("")
                    if (e.target.value) run(e.target.value)
                  }}
                >
                  <option value="">Select {et.toLowerCase()} from database...</option>
                  {selectOptions()}
                </select>
              </div>
            )}
          </div>

          <div>
            <label className="muted" style={{ display: "block", marginBottom: 4, fontWeight: 600 }}>
              {LABELS[et]} (UUID)
            </label>
            <input
              className="input"
              placeholder={`Paste ${LABELS[et]} UUID...`}
              value={id}
              onChange={(e) => {
                setId(e.target.value)
                if (fieldErr) setFieldErr(validate(e.target.value))
              }}
              aria-label={LABELS[et]}
              aria-invalid={!!fieldErr}
            />
          </div>

          {fieldErr && <div style={{ color: "#dc2626", fontSize: 13, fontWeight: 500 }}>{fieldErr}</div>}

          <button className="btn" onClick={() => run()} disabled={loading} style={{ width: "fit-content" }}>
            {loading ? "Analyzing Network & Signals..." : "⚡ RUN COLLECTIVE ANALYSIS"}
          </button>

          {loading && (
            <div className="muted" style={{ fontSize: 12, lineHeight: 1.6, animation: "pulseGlow 1.5s infinite" }}>
              ⏳ Traversing graph neighbors • Checking cross-entity device links • Querying fraud rules • Running ML classifier inference • Calculating collective risk...
            </div>
          )}

          {err && <div style={{ color: "#dc2626", whiteSpace: "pre-wrap" }}>{err}</div>}
        </div>
      </Card>

      {res && (
        <div style={{ display: "grid", gap: 18 }}>
          {/* RISK DECOMPOSITION METRICS (FOCUS GROUP: HOVER ONE DIMS SIBLINGS) */}
          <div className="grid3 focus-group">
            <Card>
              <div className="muted" style={{ fontWeight: 600 }}>
                Individual Risk (25%)
              </div>
              <div className="kpi">
                {res.collective.individual_risk_score} <Badge level={res.collective.individual_level} />
              </div>
              <div className="muted" style={{ fontSize: 11.5 }}>
                Entity KYC, loan history, credit profile
              </div>
            </Card>

            <Card>
              <div className="muted" style={{ fontWeight: 600 }}>
                Network Graph Risk (45%)
              </div>
              <div className="kpi">
                {res.collective.network_risk_score} <Badge level={res.collective.network_level} />
              </div>
              <div className="muted" style={{ fontSize: 11.5 }}>
                Shared devices, accounts, dealer burst ring
              </div>
            </Card>

            <Card>
              <div className="muted" style={{ fontWeight: 600 }}>
                ML Classifier (30%)
              </div>
              <div className="kpi">{res.ml ? Math.round(res.ml.probability * 100) + "%" : "—"}</div>
              <div className="muted" style={{ fontSize: 11.5 }}>
                {res.ml?.label || "GradientBoosting Model prediction"}
              </div>
            </Card>
          </div>

          {/* COLLECTIVE SCORE HIGHLIGHT */}
          <Card
            style={{
              borderWidth: 2,
              borderColor:
                res.collective.risk_level === "CRITICAL"
                  ? "#ef4444"
                  : res.collective.risk_level === "HIGH"
                  ? "#f97316"
                  : "var(--accent)",
              background: "linear-gradient(135deg, var(--card) 0%, var(--bg) 100%)",
            }}
          >
            <div className="muted" style={{ fontSize: 12, fontWeight: 700, letterSpacing: "0.08em" }}>
              TOTAL COLLECTIVE SWARM RISK
            </div>
            <div style={{ fontSize: 38, fontWeight: 800, margin: "6px 0", display: "flex", alignItems: "center", gap: 12 }}>
              <span>{res.collective.collective_risk_score}</span>
              <Badge level={res.collective.risk_level} />
              <span className="muted" style={{ fontSize: 13, fontWeight: 500 }}>
                Confidence: {Math.round(res.collective.confidence * 100)}%
              </span>
            </div>
            <div className="muted" style={{ fontSize: 12 }}>
              Weights: 0.25×Individual ({res.collective.individual_risk_score}) + 0.45×Network ({res.collective.network_risk_score}) + 0.30×ML ({Math.round(res.ml.probability * 100)})
            </div>
          </Card>

          {/* EXPLANATION & WHY IS THIS RISKY */}
          <div className="dash-main focus-group">
            <Card>
              <b style={{ fontSize: 15 }}>🚨 Why is this Risky?</b>
              <ul style={{ paddingLeft: 18, margin: "10px 0 0" }}>
                {res.explanation.reasons.map((r: string, i: number) => (
                  <li key={i} style={{ margin: "8px 0", fontSize: 13, lineHeight: 1.5 }}>
                    {r}
                  </li>
                ))}
              </ul>
            </Card>

            <Card>
              <b style={{ fontSize: 15 }}>🕸️ Network Topology Features</b>
              <div className="net" style={{ marginTop: 10 }}>
                {res.features.network_degree === 0 ? (
                  <Empty msg="Isolated — no relationships" />
                ) : (
                  <>
                    <div className="muted" style={{ marginBottom: 8, fontSize: 12, fontWeight: 600 }}>
                      Degree: {res.features.network_degree} • Density: {res.features.network_density} • High-Risk Neighbors: {res.features.high_risk_neighbor_count}
                    </div>
                    <div>
                      {Object.entries(res.features)
                        .slice(0, 18)
                        .map(([k, v]: any) => (
                          <span key={k} className="node">
                            <b>{k}:</b> {String(v)}
                          </span>
                        ))}
                    </div>
                  </>
                )}
              </div>
            </Card>
          </div>

          {/* FRAUD SIGNALS TABLE (FOCUS GROUP) */}
          <Card>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
              <b>Triggered Fraud Signals ({res.rules.length})</b>
            </div>
            <table className="table">
              <thead>
                <tr>
                  <th>Signal Type</th>
                  <th>Severity</th>
                  <th>Score</th>
                  <th>Explanation</th>
                </tr>
              </thead>
              <tbody>
                {res.rules.map((s: any) => (
                  <tr key={s.signal_type}>
                    <td style={{ fontWeight: 700 }}>{s.signal_type}</td>
                    <td>
                      <Badge level={s.severity} />
                    </td>
                    <td style={{ fontWeight: 700 }}>{s.score}</td>
                    <td className="muted">{s.explanation}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        </div>
      )}
    </div>
  )
}
