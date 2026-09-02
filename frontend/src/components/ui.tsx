import React from "react"

export function Card({children, className="", interactive=false, ...p}:any){ 
  return <div className={`card ${interactive ? "card-interactive" : ""} ${className}`} {...p}>{children}</div>
}

export function Badge({level}:{level:string}){ 
  return <span className={`badge ${level}`}>
    <span style={{
      width: 6, 
      height: 6, 
      borderRadius: "50%", 
      background: level==="CRITICAL"?"#ef4444":level==="HIGH"?"#f97316":level==="MEDIUM"?"#f59e0b":"#10b981",
      display: "inline-block"
    }}/>
    {level}
  </span>
}

export function Skeleton(){ 
  return <div className="skeleton" style={{width:"100%", margin:"8px 0"}}/>
}

export function Empty({msg}:{msg:string}){ 
  return <div className="card muted" style={{padding:28, textAlign:"center"}}>{msg}</div>
}

export function ErrorState({msg, retry}:{msg:string, retry?:()=>void}){ 
  return <div className="card" style={{borderColor:"#fecaca", background:"rgba(239, 68, 68, 0.04)"}}>
    <b style={{color:"#dc2626"}}>Unable to load</b>
    <div className="muted" style={{marginTop:4}}>{msg}</div>
    {retry && <button className="btn" style={{marginTop:12}} onClick={retry}>Try Again</button>}
  </div>
}

export function Metric({label, value, sub, icon}:{label:string, value:string|number, sub?:string, icon?:string}){ 
  return (
    <div className="card card-interactive" style={{display:"flex", flexDirection:"column", justifyContent:"space-between"}}>
      <div>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"center"}}>
          <span className="muted" style={{fontWeight:600, fontSize:12.5}}>{label}</span>
          {icon && <span style={{fontSize:16}}>{icon}</span>}
        </div>
        <div className="kpi" style={{color:"var(--text)"}}>{value}</div>
      </div>
      {sub && <div className="muted" style={{fontSize:11.5, marginTop:4}}>{sub}</div>}
    </div>
  )
}

export function LiveStatus({text="Swarm Engine Online"}:{text?:string}){
  return (
    <div className="live-indicator">
      <span className="live-dot" />
      <span>{text}</span>
    </div>
  )
}
