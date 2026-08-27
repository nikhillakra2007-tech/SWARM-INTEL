import { useParams } from "react-router-dom"
import { useEffect, useState } from "react"
import { api } from "../api/client"
import { Card, Badge, Empty, ErrorState } from "../components/ui"
export default function ClusterDetail(){
  const {id}=useParams()
  const [c,setC]=useState<any>(null); const [m,setM]=useState<any>(null)
  const [loading,setLoading]=useState(true); const [error,setError]=useState("")
  const load=()=>{
    if(!id) return
    setLoading(true); setError("")
    Promise.all([api.cluster(id), api.clusterMembers(id)]).then(([cc,mm])=>{ setC(cc); setM(mm)}).catch(e=> setError(e.message||String(e))).finally(()=> setLoading(false))
  }
  useEffect(()=>{ load() },[id])
  if(loading) return <Card>Loading cluster...</Card>
  if(error) return <ErrorState msg={`Unable to load cluster. ${error}`} retry={load}/>
  if(!c) return <Empty msg="Cluster not found."/>
  return <>
    <Card><b>{c.cluster_ref}</b> <Badge level={c.risk_score>80?"CRITICAL":"HIGH"}/><div className="muted">{c.member_count} members • Risk {c.risk_score} • {c.cluster_status}</div></Card>
    <Card><b>Members</b>
      {!m?.members?.length ? <Empty msg="No members in this cluster."/> :
      <table className="table"><thead><tr><th>Type</th><th>Entity</th><th>Score</th></tr></thead><tbody>{(m.members||[]).map((x:any)=><tr key={x.member_id}><td>{x.entity_type}</td><td style={{fontFamily:"monospace",fontSize:12}}>{x.entity_id.slice(0,8)}…</td><td>{x.membership_score}</td></tr>)}</tbody></table>}
    </Card>
  </>
}
