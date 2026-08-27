import { useEffect, useState } from "react"
import { api } from "../api/client"
import { Card, Badge, Empty, ErrorState } from "../components/ui"
import { Link } from "react-router-dom"
export default function Clusters(){
  const [data,setData]=useState<any>(null)
  const [loading,setLoading]=useState(true)
  const [error,setError]=useState("")
  const load=()=>{ setLoading(true); setError(""); api.clusters().then(setData).catch(e=> setError(e.message||String(e))).finally(()=> setLoading(false))}
  useEffect(()=>{ load() },[])
  if(loading) return <Card>Loading clusters...</Card>
  if(error) return <ErrorState msg={`Unable to load clusters. ${error}`} retry={load}/>
  const items=(data as any)?.items ?? (Array.isArray(data)?data:[])
  if(!items.length) return <Empty msg="No clusters detected."/>
  return <>
    <Card><b>Clusters</b><div className="muted">{items.length} detected via connected components</div></Card>
    <div style={{display:"grid",gap:12}}>
      {items.map((c:any)=><Link key={c.cluster_id} to={`/clusters/${c.cluster_id}`} className="card">
        <div style={{display:"flex",justifyContent:"space-between"}}><b>{c.cluster_ref}</b> <Badge level={c.risk_score>80?"CRITICAL":c.risk_score>60?"HIGH":"MEDIUM"}/></div>
        <div className="muted">{c.member_count} members • Risk {c.risk_score} • {c.cluster_status}</div>
      </Link>)}
    </div>
  </>
}
