export function Card({children, ...p}:any){ return <div className="card" {...p}>{children}</div>}
export function Badge({level}:{level:string}){ return <span className={`badge ${level}`}>{level}</span>}
export function Skeleton(){ return <div className="skeleton" style={{width:"100%"}}/>}
export function Empty({msg}:{msg:string}){ return <div className="card muted" style={{padding:24, textAlign:"center"}}>{msg}</div>}
export function ErrorState({msg, retry}:{msg:string, retry?:()=>void}){ return <div className="card" style={{borderColor:"#fecaca"}}><b>Unable to load</b><div className="muted">{msg}</div>{retry&&<button className="btn" style={{marginTop:8}} onClick={retry}>Try Again</button>}</div>}
export function Metric({label,value,sub}:{label:string,value:string|number,sub?:string}){ return <div className="card"><div className="muted">{label}</div><div className="kpi">{value}</div>{sub&&<div className="muted">{sub}</div>}</div>}
