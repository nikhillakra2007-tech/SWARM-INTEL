import { useEffect, useState } from "react"
import { api } from "../api/client"
import { Card, Badge, Empty, ErrorState } from "../components/ui"
import { Link } from "react-router-dom"

export default function Clusters() {
  const [data, setData] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  const load = () => {
    setLoading(true)
    setError("")
    api.clusters()
      .then(setData)
      .catch((e) => setError(e.message || String(e)))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    load()
  }, [])

  if (loading) return <Card>Loading fraud clusters...</Card>
  if (error) return <ErrorState msg={`Unable to load clusters. ${error}`} retry={load} />
  const items = (data as any)?.items ?? (Array.isArray(data) ? data : [])
  if (!items.length) return <Empty msg="No clusters detected." />

  return (
    <div style={{ display: "grid", gap: 16 }}>
      <Card>
        <b style={{ fontSize: 16 }}>⚡ Active Fraud Clusters & Rings</b>
        <div className="muted" style={{ fontSize: 13, marginTop: 4 }}>
          {items.length} connected fraud components identified across synthetic portfolio. Hover on a cluster to spotlight.
        </div>
      </Card>
      <div className="focus-group" style={{ display: "grid", gap: 12 }}>
        {items.map((c: any) => (
          <Link
            key={c.cluster_id}
            to={`/clusters/${c.cluster_id}`}
            className="card card-interactive"
            style={{ display: "block" }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <div>
                <b style={{ fontSize: 15, color: "var(--accent)" }}>{c.cluster_ref}</b>
                <span className="muted" style={{ marginLeft: 10, fontSize: 12.5 }}>
                  {c.detected_pattern || "COLLUSIVE_FRAUD_RING"}
                </span>
              </div>
              <Badge level={c.risk_score > 80 ? "CRITICAL" : c.risk_score > 60 ? "HIGH" : "MEDIUM"} />
            </div>
            <div className="muted" style={{ fontSize: 12.5, marginTop: 8 }}>
              <b>{c.member_count}</b> member entities • Risk Score: <b>{c.risk_score}</b> • Status: <b>{c.cluster_status}</b>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}
