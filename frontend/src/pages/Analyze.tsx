import { useState, useEffect } from "react"
import { api } from "../api/client"
import { Card, Badge, Empty } from "../components/ui"

const ENTITY_TYPES = ["CUSTOMER","DEVICE","DEALER","APPLICATION","LOAN"] as const
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i
const LABELS: Record<string,string> = { CUSTOMER:"Customer ID", DEVICE:"Device ID", DEALER:"Dealer ID", APPLICATION:"Application ID", LOAN:"Loan ID" }

export default function Analyze(){
  const [et,setEt]=useState<string>("CUSTOMER")
  const [id,setId]=useState("")
  const [customers,setCustomers]=useState<any[]>([])
  const [apps,setApps]=useState<any[]>([])
  const [dealers,setDealers]=useState<any[]>([])
  const [loading,setLoading]=useState(false)
  const [res,setRes]=useState<any>(null)
  const [err,setErr]=useState("")
  const [fieldErr,setFieldErr]=useState("")

  useEffect(()=>{ api.customers(1,20).then(r=>setCustomers(r.items||[])).catch(()=>{}) },[])
  useEffect(()=>{
    if(et==="DEALER") api.dealers(1,20).then(r=>setDealers(r.items||[])).catch(()=>{})
    if(et==="APPLICATION") api.applications(1,20).then(r=>setApps(r.items||[])).catch(()=>{})
  },[et])

  const validate = (v:string)=>{
    if(!v.trim()) return `Please enter a valid ${LABELS[et]}.`
    if(!UUID_RE.test(v.trim())) return `Please enter a valid UUID for ${LABELS[et]}.`
    return ""
  }

  const run=async()=>{
    const fe = validate(id)
    if(fe){ setFieldErr(fe); return }
    setFieldErr(""); setLoading(true); setErr(""); setRes(null)
    try{ const r=await api.analyze(et, id.trim()); setRes(r)}catch(e:any){ setErr(e.message ? e.message.slice(0,500) : String(e)) } finally{ setLoading(false) }
  }

  const selectOptions = ()=>{
    if(et==="CUSTOMER") return customers.map(c=> <option key={c.customer_id} value={c.customer_id}>{c.customer_ref} — {c.full_name} ({c.customer_status})</option>)
    if(et==="DEALER") return dealers.map(d=> <option key={d.dealer_id} value={d.dealer_id}>{d.dealer_code} — {d.dealer_name}</option>)
    if(et==="APPLICATION") return apps.map(a=> <option key={a.application_id} value={a.application_id}>{a.application_ref} — {a.application_status}</option>)
    return null
  }
  const showSelect = et==="CUSTOMER" || et==="DEALER" || et==="APPLICATION"

  return <>
    <Card>
      <b>Analyze Entity</b>
      <div style={{display:"grid",gap:10,marginTop:10,maxWidth:560}}>
        <label className="muted">Entity Type</label>
        <select value={et} onChange={e=>{ setEt(e.target.value); setId(""); setRes(null); setErr(""); setFieldErr("") }}>
          {ENTITY_TYPES.map(t=> <option key={t} value={t}>{t}</option>)}
        </select>
        <label className="muted">{LABELS[et]}</label>
        {showSelect && <select value={id} onChange={e=>{ setId(e.target.value); setFieldErr("") }}>
          <option value="">Select {et.toLowerCase()} or paste UUID</option>
          {selectOptions()}
        </select>}
        <input className="input" placeholder={`Paste ${LABELS[et]} (UUID)`} value={id} onChange={e=>{ setId(e.target.value); if(fieldErr) setFieldErr(validate(e.target.value)) }} aria-label={LABELS[et]} aria-invalid={!!fieldErr} />
        {fieldErr && <div style={{color:"#b42318", fontSize:13}}>{fieldErr}</div>}
        <button className="btn" onClick={run} disabled={loading}>{loading?"Analyzing...":"ANALYZE"}</button>
        {loading && <div className="muted">Analyzing network… Building relationships… Checking fraud signals… Running anomaly detection… Running ML prediction… Calculating collective risk…</div>}
        {err && <div style={{color:"#b42318", whiteSpace:"pre-wrap"}}>{err}</div>}
      </div>
    </Card>
    {res && <>
      <div className="grid3">
        <Card><div className="muted">Individual Risk</div><div className="kpi">{res.collective.individual_risk_score} <Badge level={res.collective.individual_level}/></div></Card>
        <Card><div className="muted">Network Risk</div><div className="kpi">{res.collective.network_risk_score} <Badge level={res.collective.network_level}/></div></Card>
        <Card><div className="muted">ML Probability</div><div className="kpi">{res.ml ? Math.round(res.ml.probability*100)+"%" : "—"}</div><div className="muted">{res.ml?.label || "ML prediction unavailable — model not connected yet."}</div></Card>
      </div>
      <Card style={{borderWidth:2, borderColor:"var(--accent)"}}>
        <div className="muted">COLLECTIVE RISK</div>
        <div style={{fontSize:34,fontWeight:800}}>{res.collective.collective_risk_score} <Badge level={res.collective.risk_level}/> <span className="muted" style={{fontSize:14}}>conf {res.collective.confidence}</span></div>
        <div className="muted">Weights: indiv {res.collective.weights.individual} + network {res.collective.weights.network} + ml {res.collective.weights.ml}</div>
      </Card>
      <Card>
        <b>Why is this risky?</b>
        <ul>{res.explanation.reasons.map((r:string,i:number)=><li key={i} style={{margin:"6px 0"}}>● {r}</li>)}</ul>
      </Card>
      <Card>
        <b>Network</b>
        <div className="net">
          {res.features.network_degree===0 ? <Empty msg="Isolated — no relationships"/> :
            <>
              <div className="muted">Degree {res.features.network_degree} • Density {res.features.network_density} • High-risk neighbors {res.features.high_risk_neighbor_count}</div>
              <div style={{marginTop:8}}>
                {Object.entries(res.features).slice(0,18).map(([k,v]:any)=><span key={k} className="node">{k}: {String(v)}</span>)}
              </div>
            </>}
        </div>
      </Card>
      <Card>
        <b>Fraud Signals ({res.rules.length})</b>
        <table className="table"><thead><tr><th>Type</th><th>Severity</th><th>Score</th><th>Explanation</th></tr></thead>
        <tbody>{res.rules.map((s:any)=><tr key={s.signal_type}><td>{s.signal_type}</td><td><Badge level={s.severity}/></td><td>{s.score}</td><td className="muted">{s.explanation}</td></tr>)}</tbody></table>
      </Card>
      {res.alert && <Card><b>Alert</b> {res.alert.alert_ref} <Badge level={res.alert.severity}/></Card>}
    </>}
  </>
}
