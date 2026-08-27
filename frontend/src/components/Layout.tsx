import { NavLink } from "react-router-dom"
import { useTheme } from "../lib/theme"
import { useState } from "react"
export function Layout({children}:{children:React.ReactNode}){
  const {theme,setTheme}=useTheme()
  const [open,setOpen]=useState(false)
  const Link=({to,label}:{to:string,label:string})=><NavLink to={to} className={({isActive})=> isActive?"active":""} onClick={()=>setOpen(false)}>{label}</NavLink>
  return <div className="layout">
    <aside className={`sidebar ${open?"open":""}`}>
      <div style={{fontWeight:800,letterSpacing:"-.02em"}}>SWARM<span style={{color:"var(--accent)"}}>•</span>INTEL</div>
      <div className="muted" style={{fontSize:12}}>Lending Fraud Intelligence</div>
      <nav className="nav">
        <Link to="/" label="Dashboard"/>
        <div className="section">Intelligence</div>
        <Link to="/analyze" label="Analyze"/>
        <Link to="/networks" label="Networks"/>
        <Link to="/clusters" label="Clusters"/>
        <Link to="/risk" label="Risk"/>
        <div className="section">Fraud</div>
        <Link to="/signals" label="Signals"/>
        <Link to="/alerts" label="Alerts"/>
        <Link to="/investigations" label="Investigations"/>
        <div className="section">Entities</div>
        <Link to="/customers" label="Customers"/>
        <Link to="/applications" label="Applications"/>
        <Link to="/loans" label="Loans"/>
        <Link to="/devices" label="Devices"/>
        <Link to="/dealers" label="Dealers"/>
      </nav>
      <div style={{marginTop:"auto",display:"flex",gap:8}}>
        <select value={theme} onChange={e=>setTheme(e.target.value as any)} style={{flex:1}}>
          <option value="light">Light</option><option value="dark">Dark</option><option value="system">System</option>
        </select>
      </div>
    </aside>
    <div style={{minWidth:0}}>
      <header className="header">
        <button className="btn ghost" onClick={()=>setOpen(v=>!v)} aria-label="Toggle menu">☰</button>
        <div style={{fontWeight:700, letterSpacing:"-.02em"}}>SWARM<span style={{color:"var(--accent)"}}>•</span>INTEL</div>
        <div style={{marginLeft:"auto", display:"flex", gap:8, alignItems:"center"}}>
          <span className="muted" style={{fontSize:12, display:"none"}}></span>
        </div>
      </header>
      <main style={{padding:"20px 18px", display:"grid", gap:20, maxWidth:1280, margin:"0 auto", width:"100%"}}>{children}</main>
    </div>
  </div>
}
