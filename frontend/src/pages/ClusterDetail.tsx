import { useParams, Link } from "react-router-dom"
import { useEffect, useState } from "react"
import { api } from "../api/client"
import { Card, Badge, Empty, ErrorState } from "../components/ui"

export default function ClusterDetail() {
  const { id } = useParams()
  const [c, setC] = useState<any>(null)
  const [m, setM] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  const load = () => {
    if (!id) return
    setLoading(true)
    setError("")
    Promise.all([api.cluster(id), api.clusterMembers(id)])
      .then(([cc, mm]) => {
        setC(cc)
        setM(mm)
      })
      .catch((e) => setError(e.message || String(e)))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    load()
  }, [id])

  if (loading) return <Card>Loading cluster details...</Card>
  if (error) return <ErrorState msg={`Unable to load cluster. ${error}`} retry={load} />
  if (!c) return <Empty msg="Cluster not found." />

  return (
    <div style={{ display: "grid", gap: 18 }}>
      <Card style={{ borderLeftWidth: 4, borderLeftColor: c.risk_score > 80 ? "#ef4444" : "var(--accent)" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <div className="muted" style={{ fontSize: 11, fontWeight: 700, letterSpacing: "0.08em" }}>
              FRAUD CLUSTER DOSSIER
            </div>
            <b style={{ fontSize: 22 }}>{c.cluster_ref}</b>
          </div>
          <Badge level={c.risk_score > 80 ? "CRITICAL" : "HIGH"} />
        </div>
        <div className="muted" style={{ marginTop: 8, fontSize: 13 }}>
          {c.member_count} connected members • Collective Risk Score: <b>{c.risk_score}</b> • Pattern: <b>{c.detected_pattern || "SHARED_HARDWARE_RING"}</b>
        </div>
      </Card>

      <Card>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <b>Cluster Members & Collision Footprint</b>
          <span className="muted" style={{ fontSize: 12 }}>
            {m?.members?.length || 0} associated nodes
          </span>
        </div>
        {!m?.members?.length ? (
          <Empty msg="No members in this cluster." />
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>Entity Type</th>
                <th>Entity Identifier</th>
                <th>Membership Confidence</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {(m.members || []).map((x: any) => (
                <tr key={x.member_id}>
                  <td style={{ fontWeight: 700 }}>{x.entity_type}</td>
                  <td style={{ fontFamily: "monospace", fontSize: 12 }}>{x.entity_id}</td>
                  <td style={{ fontWeight: 800 }}>{x.membership_score}%</td>
                  <td>
                    <Link to="/analyze" className="btn ghost" style={{ padding: "4px 10px", fontSize: 11.5 }}>
                      Analyze Entity →
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Card>
    </div>
  )
}
