import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { api } from "../api/client"
import { Metric, Card, Skeleton, Empty, ErrorState, Badge } from "../components/ui"

function Donut({data}:{data:{label:string,value:number,color:string}[]}){
  const total = data.reduce((s,d)=>s+d.value,0) || 1
  let acc=0
  const r=64, cx=80, cy=80, stroke=18
  const circ=2*Math.PI*r
  return <svg viewBox="0 0 160 160" width="100%" height="180" role="img" aria-label="Risk distribution">
    {data.map((d,i)=>{
      const frac=d.value/total
      const dash=frac*circ
      const gap=circ-dash
      const el=<circle key={i} r={r} cx={cx} cy={cy} fill="transparent" stroke={d.color} strokeWidth={stroke} strokeDasharray={`${dash} ${gap}`} strokeDashoffset={-acc*circ} transform={`rotate(-90 ${cx} ${cy})`} strokeLinecap="round" style={{transition:"stroke-dasharray .6s"}}/>
      acc+=frac
      return el
    })}
    <text x={cx} y={cy} textAnchor="middle" dy="6" fontSize="22" fontWeight="700" fill="var(--text)">{total}</text>
  </svg>
}
function LineChart({points}:{points:{x:string,y:number}[]}){
  if(!points.length) return <div className="muted">No activity data</div>
  const w=600, h=160, pad=28
  const maxY=Math.max(...points.map(p=>p.y),1)
  const step=w/points.length
  const d=points.map((p,i)=>{
    const x=pad + i*step
    const y=h - pad - (p.y/maxY)*(h-pad*2)
    return `${i===0?'M':'L'} ${x} ${y}`
  }).join(" ")
  const area=d + ` L ${pad + (points.length-1)*step} ${h-pad} L ${pad} ${h-pad} Z`
  return <svg viewBox={`0 0 ${w} ${h}`} width="100%" height="180" role="img" aria-label="Fraud risk trend">
    <path d={area} fill="var(--accent)" opacity="0.08"/>
    <path d={d} fill="none" stroke="var(--accent)" strokeWidth="2.2" strokeLinejoin="round"/>
    {points.map((p,i)=>{
      const x=pad + i*step
      const y=h - pad - (p.y/maxY)*(h-pad*2)
      return <circle key={i} cx={x} cy={y} r="3" fill="var(--accent)"><title>{p.x}: {p.y}</title></circle>
    })}
    <text x={pad} y={h-6} fontSize="10" fill="var(--muted)">{points[0]?.x}</text>
    <text x={w-pad} y={h-6} fontSize="10" fill="var(--muted)" textAnchor="end">{points[points.length-1]?.x}</text>
  </svg>
}
function NetworkMap({nodes, edges}:{nodes:{id:string,type:string}[], edges:{source:string,target:string,label:string}[]}){
  // simple radial layout
  const cx=200, cy=120, r=90
  const pos:Record<string,{x:number,y:number}>={}
  nodes.forEach((n,i)=>{
    const angle=(i/nodes.length)*2*Math.PI - Math.PI/2
    pos[n.id]={x: cx + Math.cos(angle)*r, y: cy + Math.sin(angle)*r}
  })
  // center is first customer
  if(nodes[0]) pos[nodes[0].id]={x:cx, y:cy}
  return <svg viewBox="0 0 400 240" width="100%" height="240" style={{background:"var(--bg)", borderRadius:12, border:"1px solid var(--border)"}}>
    {edges.map((e,i)=>{
      const a=pos[e.source], b=pos[e.target]
      if(!a||!b) return null
      const isSusp=e.label.includes("SHARED")||e.label.includes("SUSPICIOUS")
      return <g key={i}><line x1={a.x} y1={a.y} x2={b.x} y2={b.y} stroke={isSusp?"#ef4444":"var(--border)"} strokeWidth={isSusp?1.8:1} opacity={isSusp?0.9:0.5}/><text x={(a.x+b.x)/2} y={(a.y+b.y)/2} fontSize="7" fill="var(--muted)" textAnchor="middle">{e.label.replace("SHARED_","")}</text></g>
    })}
    {nodes.map(n=>{
      const p=pos[n.id]
      const col=n.type==="CUSTOMER"?"var(--accent)":n.type==="DEVICE"?"#06b6d4":n.type==="DEALER"?"#8b5cf6":"#94a3b8"
      return <g key={n.id}><circle cx={p.x} cy={p.y} r={n.type==="CUSTOMER"?18:12} fill={col} stroke="var(--card)" strokeWidth="2"/><text x={p.x} y={p.y+4} textAnchor="middle" fontSize="7" fill="#fff" fontWeight="600">{n.type.slice(0,3)}</text><text x={p.x} y={p.y+28} textAnchor="middle" fontSize="8" fill="var(--muted)">{n.id.split(":")[1]?.slice(0,4)}</text></g>
    })}
  </svg>
}
const FAQ = [
  {q:"What is SWARM•INTEL?", a:"A collective lending intelligence platform that connects customers, devices, dealers, bank accounts and behaviour to uncover fraud ecosystems that are invisible at the single-loan level."},
  {q:"How does the platform detect fraud networks?", a:"By building a graph from entity_relationships, running fraud rules, anomaly and temporal analysis, then scoring network risk via the Swarm Risk Engine."},
  {q:"Why analyse relationships instead of only individuals?", a:"An entity can appear LOW individually but CRITICAL on network (e.g., shared device with a high-risk cluster). SWARM•INTEL exposes this difference."},
  {q:"What signals can the platform identify?", a:"Shared device/mobile/bank/address/guarantor, same IP/dealer, rapid bursts, dealer anomalies, high connectivity, repayment anomalies, and emerging growth."},
  {q:"How does the risk engine work?", a:"Collective = 0.25×Individual + 0.45×Network + 0.30×ML (0–100). Individual is entity-only, Network is shared-entity/graph, ML is model probability."},
  {q:"How does the ML model contribute?", a:"fraud_model_v2 (GradientBoosting, thr 0.35) on 7 features predicts fraud_probability, used as one input to collective risk, not the final decision."},
  {q:"What is a fraud cluster?", a:"A connected component of shared infrastructure with elevated risk (e.g., F-9001: 8 members sharing a device via DL003)."},
  {q:"How does an investigator use the platform?", a:"Start at Analyze → enter entity → review collective risk, evidence, network, signals, cluster, then create an Investigation from an Alert."},
]
function FaqSection(){
  const [open,setOpen]=useState<number|null>(null)
  return <section aria-labelledby="faq-heading" style={{marginTop:8}}>
    <h2 id="faq-heading" className="faq-heading" style={{fontSize:20, margin:"0 0 6px"}}>Frequently Asked Questions</h2>
    <p className="faq-subtitle" style={{margin:"0 0 12px", fontSize:13}}>How SWARM•INTEL works — actual implementation.</p>
    <div style={{display:"grid", gap:8}}>
      {FAQ.map((f,i)=>(
        <div key={i} className={`card faq-card ${open===i?'open':''}`} style={{padding:0, overflow:"hidden"}}>
          <button onClick={()=> setOpen(open===i?null:i)} aria-expanded={open===i} aria-controls={`faq-${i}`} style={{width:"100%", textAlign:"left", background:"transparent", border:"none", padding:"14px 16px", display:"flex", justifyContent:"space-between", alignItems:"center", cursor:"pointer", color:"var(--faq-question)"}}>
            <span className="faq-question" style={{fontWeight:600, fontSize:13}}>{f.q}</span>
            <span aria-hidden className="faq-chevron" style={{transform: open===i?"rotate(180deg)":"none", transition:".2s", fontSize:14}}>⌄</span>
          </button>
          {open===i && <div id={`faq-${i}`} style={{padding:"0 16px 14px", fontSize:13, lineHeight:1.6}} className="faq-answer">{f.a}</div>}
        </div>
      ))}
    </div>
  </section>
}

export default function Dashboard(){
  const [data,setData]=useState<any>(null)
  const [clusters,setClusters]=useState<any[]>([])
  const [alerts,setAlerts]=useState<any[]>([])
  const [apps,setApps]=useState<any[]>([])
  const [signals,setSignals]=useState<any[]>([])
  const [network,setNetwork]=useState<{nodes:any[],edges:any[]}|null>(null)
  const [e,setE]=useState("")
  const [loading,setLoading]=useState(true)

  const load=async()=>{
    setLoading(true); setE("")
    try{
      const [appsRes, clustersRes, alertsRes, appsForChart, sigRes, netRes] = await Promise.all([
        api.applications(1,1),
        api.clusters(),
        api.alerts(),
        api.applications(1,100),
        api.signalsList().catch(()=>({items:[]})),
        api.networkComponents().catch(()=>({components:[]})),
      ])
      const clItems=(clustersRes as any).items ?? (Array.isArray(clustersRes)?clustersRes:[])
      const alItems=(alertsRes as any).items ?? (Array.isArray(alertsRes)?alertsRes:[])
      setData({apps: (appsRes as any).total, clusters: clItems.length, alerts: alItems.length, customers: 10000})
      setClusters(clItems)
      setAlerts(alItems)
      setApps((appsForChart as any).items ?? [])
      setSignals((sigRes as any).items ?? [])
      // build sample network from largest component
      const comps=(netRes as any).components ?? []
      if(comps.length){
        const biggest=[...comps].sort((a,b)=>b.size-a.size)[0]
        const members=(biggest.members||[]).slice(0,8)
        const nodes=members.map((m:string)=>{
          const [type, id]=m.split(":")
          return {id:m, type, label:id.slice(0,4)}
        })
        const edges=members.slice(1).map((m,i)=>({source:members[0], target:m, label:"SHARED_DEVICE"}))
        setNetwork({nodes, edges})
      }
    }catch(err:any){ setE(err.message||String(err)) } finally{ setLoading(false) }
  }
  useEffect(()=>{ load() },[])

  if(loading) return <><Skeleton/><Skeleton/></>
  if(e) return <ErrorState msg={`Unable to load dashboard. ${e}`} retry={load}/>
  if(!data) return <Empty msg="No dashboard data."/>

  const buckets={LOW:0,MEDIUM:0,HIGH:0,CRITICAL:0} as Record<string,number>
  clusters.forEach((c:any)=>{
    const s=c.risk_score
    if(s<30) buckets.LOW++
    else if(s<60) buckets.MEDIUM++
    else if(s<80) buckets.HIGH++
    else buckets.CRITICAL++
  })
  const donut=[
    {label:"LOW", value:buckets.LOW, color:"#22c55e"},
    {label:"MEDIUM", value:buckets.MEDIUM, color:"#eab308"},
    {label:"HIGH", value:buckets.HIGH, color:"#f97316"},
    {label:"CRITICAL", value:buckets.CRITICAL, color:"#ef4444"},
  ].filter(d=>d.value>0)
  const byMonth:Record<string,number>={}
  apps.forEach((a:any)=>{
    const d=new Date(a.application_timestamp)
    const k=`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}`
    byMonth[k]=(byMonth[k]||0)+1
  })
  const linePoints=Object.entries(byMonth).sort(([a],[b])=>a.localeCompare(b)).slice(-8).map(([k,v])=>({x:k, y:v}))
  const topClusters=[...clusters].sort((a,b)=>b.risk_score-a.risk_score).slice(0,4)
  const recentAlerts=[...alerts].slice(0,4)
  const topSignals=[...signals].sort((a,b)=>b.score-a.score).slice(0,5)

  return <div style={{display:"grid", gap:22}}>
    {/* HERO */}
    <div className="card" style={{padding:"22px 20px", background:"linear-gradient(135deg, var(--card) 0%, var(--bg) 100%)"}}>
      <div style={{fontSize:11, letterSpacing:".12em", color:"var(--accent)", fontWeight:700}}>SWARM•INTEL</div>
      <h1 style={{margin:"6px 0 8px", fontSize:26, lineHeight:1.15}}>Detect the network.<br/>Understand the signal.<br/>Stop the fraud.</h1>
      <p className="muted" style={{margin:"0 0 14px", maxWidth:620}}>Collective lending intelligence that connects customers, devices, dealers, accounts and behaviour to uncover emerging fraud ecosystems.</p>
      <div style={{display:"flex", gap:8, flexWrap:"wrap"}}>
        <Link to="/analyze" className="btn">Analyze Entity</Link>
        <Link to="/networks" className="btn ghost">Explore Network</Link>
      </div>
    </div>

    {/* KPI */}
    <div className="grid4">
      <Metric label="Active Fraud Networks" value={data.clusters} sub="Connected components"/>
      <Metric label="High-Risk Entities" value={data.alerts} sub="Open alerts"/>
      <Metric label="Total Applications" value={data.apps}/>
      <Metric label="Total Customers" value={data.customers} sub="Synthetic • 10k"/>
    </div>

    {/* Network Intelligence - centerpiece */}
    <Card>
      <div style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}>
        <div><b>Network Intelligence</b><div className="muted" style={{fontSize:12}}>Customer → Device → Mobile → Bank → Dealer relationships</div></div>
        <Link to="/networks" className="muted" style={{fontSize:12}}>Open Networks →</Link>
      </div>
      <div style={{marginTop:12}}>
        {network ? <NetworkMap nodes={network.nodes} edges={network.edges}/> : <Empty msg="No network selected — explore via Analyze or Networks"/>}
      </div>
      <div className="muted" style={{fontSize:11, marginTop:6}}>Nodes from largest connected component • Red edges = suspicious shared infrastructure</div>
    </Card>

    {/* Risk distribution + Fraud risk trend */}
    <div style={{display:"grid", gap:14}} className="dash-main">
      <Card>
        <div style={{display:"flex", justifyContent:"space-between"}}><b>Risk Distribution</b><Link to="/clusters" className="muted" style={{fontSize:12}}>View all</Link></div>
        {donut.length ? <><Donut data={donut}/><div style={{display:"flex", gap:10, flexWrap:"wrap", justifyContent:"center"}}>{donut.map(d=> <span key={d.label} style={{fontSize:12}}><span style={{display:"inline-block", width:10, height:10, background:d.color, borderRadius:2, marginRight:4}}/>{d.label} {d.value}</span>)}</div></> : <Empty msg="No cluster risk data"/>}
      </Card>
      <Card>
        <div style={{display:"flex", justifyContent:"space-between"}}><b>Fraud Risk Trend</b><span className="muted" style={{fontSize:12}}>Applications per month</span></div>
        <LineChart points={linePoints}/>
      </Card>
    </div>

    {/* Top fraud signals + Top clusters */}
    <div style={{display:"grid", gap:14, gridTemplateColumns:"1fr 1fr"}} className="dash-main">
      <Card>
        <div style={{display:"flex", justifyContent:"space-between"}}><b>Top Fraud Signals</b><Link to="/signals" className="muted" style={{fontSize:12}}>View All Signals →</Link></div>
        {!topSignals.length ? <Empty msg="No signals"/> :
          <div style={{display:"grid", gap:8, marginTop:8}}>
            {topSignals.map((s:any)=><div key={s.signal_id} style={{display:"flex", justifyContent:"space-between", alignItems:"center", padding:"8px 0", borderBottom:"1px solid var(--border)"}}>
              <div><div style={{fontWeight:600, fontSize:12}}>{s.signal_type}</div><div className="muted" style={{fontSize:11}}>{s.entity_type}</div></div>
              <div style={{textAlign:"right"}}><div style={{fontWeight:700}}>{s.score}</div><Badge level={s.severity}/></div>
            </div>)}
          </div>}
      </Card>
      <Card>
        <div style={{display:"flex", justifyContent:"space-between"}}><b>Top Risky Clusters</b><Link to="/clusters" className="muted" style={{fontSize:12}}>View All</Link></div>
        {!topClusters.length ? <Empty msg="No clusters detected."/> :
          <table className="table"><thead><tr><th>Cluster</th><th>Members</th><th>Risk</th></tr></thead>
          <tbody>{topClusters.map((c:any)=><tr key={c.cluster_id}><td><Link to={`/clusters/${c.cluster_id}`} style={{color:"var(--accent)", fontWeight:600}}>{c.cluster_ref}</Link></td><td>{c.member_count}</td><td><Badge level={c.risk_score>80?"CRITICAL":c.risk_score>60?"HIGH":"MEDIUM"}/> {Math.round(c.risk_score)}</td></tr>)}</tbody></table>}
      </Card>
    </div>

    {/* Recent activity + Quick actions */}
    <div style={{display:"grid", gap:14, gridTemplateColumns:"2fr 1fr"}} className="dash-main">
      <Card>
        <div style={{display:"flex", justifyContent:"space-between"}}><b>Recent Intelligence Activity</b><Link to="/alerts" className="muted" style={{fontSize:12}}>View All Alerts</Link></div>
        {!recentAlerts.length ? <Empty msg="No recent activity"/> :
          <div style={{display:"grid", gap:0, marginTop:8}}>
            {recentAlerts.map((a:any,idx:number)=><div key={a.alert_id} style={{display:"flex", gap:10, padding:"10px 0", borderBottom: idx===recentAlerts.length-1?"none":"1px solid var(--border)"}}>
              <div style={{width:8, height:8, borderRadius:"50%", background: a.severity==="CRITICAL"?"#ef4444":a.severity==="HIGH"?"#f97316":"#eab308", marginTop:6}}/>
              <div><div style={{fontSize:13, fontWeight:600}}>{a.alert_type.replace(/_/g," ")}</div><div className="muted" style={{fontSize:11}}>{a.alert_ref} • {a.severity} • {new Date(a.generated_at).toLocaleDateString()}</div></div>
            </div>)}
          </div>}
      </Card>
      <Card>
        <b>Quick Actions</b>
        <div style={{display:"grid", gap:8, marginTop:10}}>
          <Link to="/analyze" className="btn" style={{textAlign:"center"}}>Analyze Entity</Link>
          <Link to="/networks" className="btn ghost" style={{textAlign:"center"}}>Explore Network</Link>
          <Link to="/alerts" className="btn ghost" style={{textAlign:"center"}}>View Alerts</Link>
          <Link to="/investigations" className="btn ghost" style={{textAlign:"center"}}>Investigations</Link>
        </div>
      </Card>
    </div>

    <FaqSection/>

    <div className="card" style={{textAlign:"center", padding:"20px"}}>
      <div style={{fontWeight:700}}>See the network before the fraud.</div>
      <div className="muted" style={{margin:"6px 0 12px"}}>Move from isolated loan decisions to collective lending intelligence.</div>
      <div style={{display:"flex", gap:8, justifyContent:"center", flexWrap:"wrap"}}>
        <Link to="/analyze" className="btn">Analyze Entity</Link>
        <Link to="/networks" className="btn ghost">Explore Networks</Link>
      </div>
    </div>
    <div className="muted" style={{textAlign:"center", fontSize:11, padding:"4px 0"}}>SWARM•INTEL • Synthetic demo data • Not production advice • © 2025</div>
  </div>
}
