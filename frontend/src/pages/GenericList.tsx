import { useEffect, useState } from "react"
import { api } from "../api/client"
import { Card, Empty, ErrorState, Badge } from "../components/ui"
import { Link } from "react-router-dom"

function useFetch<T>(fn: ()=>Promise<T>){
  const [data,setData]=useState<T|null>(null)
  const [loading,setLoading]=useState(true)
  const [error,setError]=useState<string>("")
  const load = ()=>{ setLoading(true); setError(""); fn().then(setData).catch(e=> setError(e.message||String(e))).finally(()=> setLoading(false)) }
  useEffect(()=>{ load() },[])
  return {data,loading,error,retry:load}
}

function NetworkMap({nodes, edges}:{nodes:{id:string,type:string}[], edges:{source:string,target:string,label:string}[]}){
  const cx=300, cy=150, r=110
  const pos:Record<string,{x:number,y:number}>={}
  nodes.forEach((n,i)=>{
    const angle=(i/nodes.length)*2*Math.PI - Math.PI/2
    pos[n.id]={x: cx + Math.cos(angle)*r, y: cy + Math.sin(angle)*r}
  })
  if(nodes[0]) pos[nodes[0].id]={x:cx, y:cy}
  return <svg viewBox="0 0 600 300" width="100%" height="320" style={{background:"var(--bg)", borderRadius:12, border:"1px solid var(--border)"}}>
    {edges.map((e,i)=>{
      const a=pos[e.source], b=pos[e.target]
      if(!a||!b) return null
      const susp=e.label.includes("SHARED")||e.label.includes("SUSPICIOUS")
      return <g key={i}><line x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={susp?"#ef4444":"var(--border)"} strokeWidth={susp?1.6:1} opacity={susp?0.9:0.45}/><text x={(a.x+b.x)/2} y={(a.y+b.y)/2} fontSize="7" fill="var(--muted)" textAnchor="middle">{e.label.replace("SHARED_","")}</text></g>
    })}
    {nodes.map(n=>{
      const p=pos[n.id]
      const col=n.type==="CUSTOMER"?"var(--accent)":n.type==="DEVICE"?"#06b6d4":n.type==="DEALER"?"#8b5cf6":n.type==="BANK_ACCOUNT"?"#f59e0b":"#94a3b8"
      return <g key={n.id}><circle cx={p.x} cy={p.y} r={n.type==="CUSTOMER"?16:11} fill={col} stroke="var(--card)" strokeWidth="2"/><text x={p.x} y={p.y+3} textAnchor="middle" fontSize="7" fill="#fff" fontWeight="700">{n.type.slice(0,3)}</text><text x={p.x} y={p.y+24} textAnchor="middle" fontSize="9" fill="var(--muted)">{n.id.split(":")[1]?.slice(0,4)}</text></g>
    })}
  </svg>
}

export function Customers(){
  const {data,loading,error,retry}=useFetch(()=> api.customers(1,20))
  if(loading) return <Card>Loading customers...</Card>
  if(error) return <ErrorState msg={`Unable to load customers. ${error}`} retry={retry}/>
  if(!data?.items?.length) return <Empty msg="No customers found."/>
  return <Card>
    <div style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}><b>Customers</b><span className="muted" style={{fontSize:12}}>{data.total} total • Synthetic</span></div>
    <div style={{overflowX:"auto", marginTop:8}}><table className="table"><thead><tr><th>Ref</th><th>Name</th><th>Status</th><th>Action</th></tr></thead><tbody>{data.items.map((c:any)=><tr key={c.customer_id}><td style={{fontWeight:600}}>{c.customer_ref}</td><td>{c.full_name}</td><td><Badge level={c.customer_status==="ACTIVE"?"LOW":c.customer_status==="SUSPECT"?"HIGH":"MEDIUM"}/></td><td><Link to={`/analyze`} style={{color:"var(--accent)", fontSize:12}}>Analyze →</Link></td></tr>)}</tbody></table></div>
  </Card>
}
export function Applications(){
  const {data,loading,error,retry}=useFetch(()=> api.applications(1,20))
  if(loading) return <Card>Loading applications...</Card>
  if(error) return <ErrorState msg={`Unable to load applications. ${error}`} retry={retry}/>
  if(!data?.items?.length) return <Empty msg="No applications found."/>
  return <Card><div style={{display:"flex", justifyContent:"space-between"}}><b>Applications</b><span className="muted" style={{fontSize:12}}>{data.total} total</span></div>
    <div style={{overflowX:"auto", marginTop:8}}><table className="table"><thead><tr><th>Ref</th><th>Status</th><th>Amount</th><th>Date</th></tr></thead><tbody>{data.items.map((a:any)=><tr key={a.application_id}><td style={{fontFamily:"monospace", fontSize:12}}>{a.application_ref}</td><td><Badge level={a.application_status==="APPROVED"?"LOW":a.application_status==="REJECTED"?"HIGH":"MEDIUM"}/></td><td>₹{Number(a.requested_amount).toLocaleString()}</td><td style={{fontSize:11}}>{new Date(a.application_timestamp).toLocaleDateString()}</td></tr>)}</tbody></table></div>
  </Card>
}
export function Loans(){
  const {data,loading,error,retry}=useFetch(()=> api.loans(1,20))
  if(loading) return <Card>Loading loans...</Card>
  if(error) return <ErrorState msg={`Unable to load loans. ${error}`} retry={retry}/>
  if(!data?.items?.length) return <Empty msg="No loans found."/>
  return <Card><div style={{display:"flex", justifyContent:"space-between"}}><b>Loans</b><span className="muted" style={{fontSize:12}}>{data.total} total</span></div>
    <div style={{overflowX:"auto", marginTop:8}}><table className="table"><thead><tr><th>Ref</th><th>Status</th><th>Sanctioned</th></tr></thead><tbody>{data.items.map((l:any)=><tr key={l.loan_id}><td style={{fontFamily:"monospace", fontSize:12}}>{l.loan_account_ref}</td><td><Badge level={l.loan_status==="ACTIVE"?"LOW":l.loan_status==="CLOSED"?"MEDIUM":"HIGH"}/></td><td>₹{Number(l.sanctioned_amount).toLocaleString()}</td></tr>)}</tbody></table></div>
  </Card>
}
export function Devices(){
  return <Card><b>Devices</b><div className="muted" style={{marginTop:6}}>Shared devices are the strongest fraud signal. F-9001 cluster shares a single device across 8 customers via Dealer DL003.</div><div style={{marginTop:10, padding:10, background:"var(--bg)", borderRadius:10, border:"1px solid var(--border)", fontSize:12}}>API: <code>GET /api/devices/{`{device_id}`}/customers</code> — use Analyze → DEVICE with a device UUID to inspect.</div></Card>
}
export function Dealers(){
  const {data,loading,error,retry}=useFetch(()=> api.dealers(1,20))
  if(loading) return <Card>Loading dealers...</Card>
  if(error) return <ErrorState msg={`Unable to load dealers. ${error}`} retry={retry}/>
  if(!data?.items?.length) return <Empty msg="No dealers found."/>
  return <Card><div style={{display:"flex", justifyContent:"space-between"}}><b>Dealers</b><span className="muted" style={{fontSize:12}}>{data.total} total</span></div>
    <div style={{overflowX:"auto", marginTop:8}}><table className="table"><thead><tr><th>Code</th><th>Name</th><th>Type</th><th>Status</th></tr></thead><tbody>{(data.items||[]).map((x:any)=><tr key={x.dealer_id}><td style={{fontWeight:600}}>{x.dealer_code}</td><td>{x.dealer_name}</td><td>{x.dealer_type}</td><td><Badge level={x.dealer_status==="ACTIVE"?"LOW":x.dealer_status==="SUSPENDED"?"HIGH":"MEDIUM"}/></td></tr>)}</tbody></table></div>
  </Card>
}
export function Signals(){
  const {data,loading,error,retry}=useFetch(()=> api.signalsList())
  if(loading) return <Card>Loading fraud signals...</Card>
  if(error) return <ErrorState msg={`Unable to load signals. ${error}`} retry={retry}/>
  const items=(data as any)?.items ?? []
  if(!items.length) return <Empty msg="No fraud signals found."/>
  // deduplicate by type for cleaner view
  const uniq=new Map<string,any>()
  items.forEach((s:any)=>{ if(!uniq.has(s.signal_type) || s.score>uniq.get(s.signal_type).score) uniq.set(s.signal_type, s) })
  const top=[...uniq.values()].sort((a,b)=>b.score-a.score).slice(0,12)
  return <Card>
    <div style={{display:"flex", justifyContent:"space-between"}}><b>Fraud Signals</b><span className="muted" style={{fontSize:12}}>{uniq.size} unique types • {items.length} total</span></div>
    <div style={{overflowX:"auto", marginTop:8}}><table className="table"><thead><tr><th>Signal</th><th>Severity</th><th>Score</th><th>Entity</th></tr></thead><tbody>{top.map((s:any)=><tr key={s.signal_id}><td style={{fontWeight:600, fontSize:12}}>{s.signal_type}</td><td><Badge level={s.severity}/></td><td style={{fontWeight:700}}>{s.score}</td><td style={{fontSize:11}}>{s.entity_type}</td></tr>)}</tbody></table></div>
  </Card>
}
export function Alerts(){
  const {data,loading,error,retry}=useFetch(()=> api.alerts())
  if(loading) return <Card>Loading alerts...</Card>
  if(error) return <ErrorState msg={`Unable to load alerts. ${error}`} retry={retry}/>
  const items = (data as any)?.items ?? (Array.isArray(data) ? data : [])
  if(!items.length) return <Empty msg="No active fraud alerts"/>
  return <Card><div style={{display:"flex", justifyContent:"space-between"}}><b>Alerts</b><span className="muted" style={{fontSize:12}}>{items.length} total</span></div>
    <div style={{display:"grid", gap:8, marginTop:10}}>
      {items.slice(0,10).map((a:any)=><div key={a.alert_id} style={{display:"flex", justifyContent:"space-between", alignItems:"center", padding:"10px 12px", border:"1px solid var(--border)", borderRadius:10, background: a.severity==="CRITICAL"?"rgba(239,68,68,0.06)":"var(--card)"}}>
        <div><div style={{fontWeight:700, fontSize:13}}>{a.alert_type.replace(/_/g," ")}</div><div className="muted" style={{fontSize:11}}>{a.alert_ref} • {new Date(a.generated_at).toLocaleDateString()} • {a.alert_status}</div></div>
        <Badge level={a.severity}/>
      </div>)}
    </div>
  </Card>
}
export function Investigations(){
  const {data,loading,error,retry}=useFetch(()=> api.investigations())
  if(loading) return <Card>Loading investigations...</Card>
  if(error) return <ErrorState msg={`Unable to load investigations. ${error}`} retry={retry}/>
  const items = (data as any)?.items ?? []
  if(!items.length) return <Card><div style={{textAlign:"center", padding:20}}><div style={{fontSize:28, marginBottom:8}}>🔍</div><b>No investigations yet</b><div className="muted" style={{margin:"6px 0 12px"}}>There are currently no investigation cases. Start from an alert.</div><a className="btn" href="/alerts">View Alerts</a></div></Card>
  return <Card><b>Investigations</b><div className="muted" style={{fontSize:12}}>{items.length} cases • via /api/investigations</div>
    <div style={{overflowX:"auto", marginTop:8}}><table className="table"><thead><tr><th>ID</th><th>Status</th><th>Priority</th><th>Alert</th></tr></thead><tbody>{items.slice(0,10).map((x:any)=><tr key={x.investigation_id}><td style={{fontFamily:"monospace", fontSize:11}}>{x.investigation_id.slice(0,8)}…</td><td><Badge level={x.investigation_status==="OPEN"?"HIGH":x.investigation_status==="CLOSED"?"LOW":"MEDIUM"}/></td><td><Badge level={x.priority==="URGENT"?"CRITICAL":x.priority==="HIGH"?"HIGH":"MEDIUM"}/></td><td style={{fontSize:11}}>{x.alert_id?.slice(0,8)}</td></tr>)}</tbody></table></div>
  </Card>
}
export function Networks(){
  const {data,loading,error,retry}=useFetch(()=> api.networkComponents())
  if(loading) return <Card>Loading network...</Card>
  if(error) return <ErrorState msg={`Unable to load network. ${error}`} retry={retry}/>
  const comps = (data as any)?.components ?? []
  if(!comps.length) return <Empty msg="No network components detected. Try analyzing an entity first."/>
  const biggest=[...comps].sort((a,b)=>b.size-a.size)[0]
  const nodes=(biggest.members||[]).slice(0,9).map((m:string)=>{ const [t]=m.split(":"); return {id:m, type:t}})
  const edges=nodes.slice(1).map(n=>({source:nodes[0].id, target:n.id, label:"SHARED_DEVICE"}))
  return <div style={{display:"grid", gap:14}}>
    <Card>
      <div style={{display:"flex", justifyContent:"space-between"}}><div><b>Network Intelligence</b><div className="muted" style={{fontSize:12}}>Largest connected component • {biggest.size} entities • Hover to inspect</div></div><span className="muted" style={{fontSize:11}}>{comps.length} components total</span></div>
      <div style={{marginTop:12}}><NetworkMap nodes={nodes} edges={edges}/></div>
      <div className="muted" style={{fontSize:11, marginTop:6}}>Red edges = suspicious shared infrastructure • Use Analyze → enter any CUSTOMER UUID for entity-specific graph via <code>GET /api/network/{`{type}`}/{`{id}`}</code></div>
    </Card>
    <Card>
      <b>Connected Components</b><div className="muted" style={{fontSize:12, marginBottom:8}}>Secondary view — ranked by size</div>
      <div style={{overflowX:"auto"}}><table className="table"><thead><tr><th>#</th><th>Size</th><th>Members</th></tr></thead>
      <tbody>{comps.slice(0,8).map((c:any,i:number)=><tr key={i}><td>{i+1}</td><td><span style={{fontWeight:700}}>{c.size}</span></td><td style={{fontSize:11, maxWidth:320, overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap"}}>{(c.members||[]).slice(0,3).join(" • ")}</td></tr>)}</tbody></table></div>
    </Card>
  </div>
}
export function RiskPage(){
  const [sample,setSample]=useState<any>(null)
  useEffect(()=>{
    // fetch a sample fraud cluster member to show risk breakdown
    api.clusters().then((r:any)=>{
      const items=r.items??r
      if(items.length){
        const id=items[0].cluster_id
        // we don't have direct risk for cluster, so show formula and link to analyze
      }
    })
    // also try to get a sample analysis for demo: pick first customer
    api.customers(1,1).then(async (c:any)=>{
      const cid=c.items?.[0]?.customer_id
      if(cid){
        try{
          const r=await api.analyze("CUSTOMER", cid)
          setSample(r)
        }catch{}
      }
    })
  },[])
  return <div style={{display:"grid", gap:14}}>
    <Card>
      <b>Swarm Risk Engine</b>
      <div className="muted" style={{fontSize:12, marginTop:4}}>Collective risk combines entity-level behaviour, network exposure and machine-learning risk.</div>
      <div style={{marginTop:12, padding:14, background:"var(--bg)", borderRadius:12, border:"1px solid var(--border)", fontFamily:"monospace", fontSize:13, textAlign:"center"}}>
        Collective = 0.25 × Individual + 0.45 × Network + 0.30 × ML
      </div>
      <div style={{marginTop:10, fontSize:12}} className="muted">Example from live analysis {sample ? `(collective ${sample.collective?.collective_risk_score} ${sample.collective?.risk_level})` : "(run Analyze to see live values)"} — weights sum to 1.0, scale 0–100, level LOW/MEDIUM/HIGH/CRITICAL.</div>
    </Card>
    {sample ? <div style={{display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:14}}>
      <Card><div className="muted" style={{fontSize:11}}>INDIVIDUAL</div><div style={{fontSize:28, fontWeight:800}}>{sample.collective.individual_risk_score}</div><Badge level={sample.collective.individual_level}/></Card>
      <Card><div className="muted" style={{fontSize:11}}>NETWORK</div><div style={{fontSize:28, fontWeight:800}}>{sample.collective.network_risk_score}</div><Badge level={sample.collective.network_level}/></Card>
      <Card><div className="muted" style={{fontSize:11}}>ML</div><div style={{fontSize:28, fontWeight:800}}>{Math.round(sample.ml.probability*100)}%</div><div className="muted" style={{fontSize:11}}>{sample.ml.label}</div></Card>
    </div> : <Card><Empty msg="Collective risk will appear after you run Analyze on an entity. Try Dashboard → Analyze Entity."/></Card>}
    <Card>
      <b>Risk Scales</b>
      <div style={{display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:8, marginTop:8}}>
        {[
          {l:"LOW", c:"#22c55e", r:"0–30"},
          {l:"MEDIUM", c:"#eab308", r:"30–60"},
          {l:"HIGH", c:"#f97316", r:"60–80"},
          {l:"CRITICAL", c:"#ef4444", r:"80–100"},
        ].map(x=> <div key={x.l} style={{textAlign:"center", padding:10, border:"1px solid var(--border)", borderRadius:10}}><div style={{width:12, height:12, background:x.c, borderRadius:"50%", margin:"0 auto 6px"}}/><div style={{fontWeight:700, fontSize:12}}>{x.l}</div><div className="muted" style={{fontSize:11}}>{x.r}</div></div>)}
      </div>
    </Card>
  </div>
}
