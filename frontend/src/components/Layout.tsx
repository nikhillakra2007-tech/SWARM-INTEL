import { NavLink, useLocation } from "react-router-dom"
import { useTheme } from "../lib/theme"
import { useState } from "react"
import { LiveStatus } from "./ui"

export function Layout({ children }: { children: React.ReactNode }) {
  const { theme, setTheme } = useTheme()
  const [open, setOpen] = useState(false)
  const location = useLocation()

  const Link = ({ to, label, icon }: { to: string; label: string; icon?: string }) => (
    <NavLink
      to={to}
      className={({ isActive }) => (isActive ? "active" : "")}
      onClick={() => setOpen(false)}
    >
      {icon && <span style={{ fontSize: 15, opacity: 0.9 }}>{icon}</span>}
      <span>{label}</span>
    </NavLink>
  )

  return (
    <div className="layout">
      <aside className={`sidebar ${open ? "open" : ""}`}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 34,
            height: 34,
            borderRadius: 10,
            background: "linear-gradient(135deg, var(--accent) 0%, #06b6d4 100%)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#fff",
            fontWeight: 800,
            fontSize: 16,
            boxShadow: "0 4px 14px var(--accent-glow)"
          }}>
            S
          </div>
          <div>
            <div style={{ fontWeight: 800, letterSpacing: "-0.02em", fontSize: 16 }}>
              SWARM<span style={{ color: "var(--accent)" }}>•</span>INTEL
            </div>
            <div className="muted" style={{ fontSize: 11.5, fontWeight: 500 }}>
              Fraud Intelligence Network
            </div>
          </div>
        </div>

        <nav className="nav">
          <Link to="/" label="Dashboard" icon="📊" />
          <div className="section">Intelligence</div>
          <Link to="/analyze" label="Analyze Entity" icon="🔍" />
          <Link to="/networks" label="Network Graph" icon="🕸️" />
          <Link to="/clusters" label="Fraud Clusters" icon="⚡" />
          <Link to="/risk" label="Risk Scoring" icon="🛡️" />
          <div className="section">Fraud Detection</div>
          <Link to="/signals" label="Signals" icon="📡" />
          <Link to="/alerts" label="Alerts" icon="🚨" />
          <Link to="/investigations" label="Investigations" icon="📋" />
          <div className="section">Entities (31 Tables)</div>
          <Link to="/customers" label="Customers" icon="👥" />
          <Link to="/applications" label="Applications" icon="📝" />
          <Link to="/loans" label="Loans" icon="💳" />
          <Link to="/devices" label="Devices" icon="📱" />
          <Link to="/dealers" label="Dealers" icon="🏢" />
        </nav>

        <div style={{ marginTop: "auto", display: "flex", flexDirection: "column", gap: 12 }}>
          <div style={{ padding: "10px 12px", background: "var(--bg)", borderRadius: 12, border: "1px solid var(--border)" }}>
            <LiveStatus text="Collective Engine Live" />
          </div>
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <span className="muted" style={{ fontSize: 12 }}>Theme:</span>
            <select
              value={theme}
              onChange={(e) => setTheme(e.target.value as any)}
              style={{ flex: 1, padding: "6px 10px", fontSize: 12 }}
            >
              <option value="light">Light</option>
              <option value="dark">Dark</option>
              <option value="system">System</option>
            </select>
          </div>
        </div>
      </aside>

      <div style={{ minWidth: 0, display: "flex", flexDirection: "column" }}>
        <header className="header">
          <button
            className="btn ghost"
            onClick={() => setOpen((v) => !v)}
            aria-label="Toggle menu"
            style={{ padding: "6px 10px", display: "none" }}
          >
            ☰
          </button>
          <div style={{ fontWeight: 700, letterSpacing: "-0.02em", display: "flex", alignItems: "center", gap: 8 }}>
            <span>Lending Fraud Swarm Intelligence</span>
          </div>
          <div style={{ marginLeft: "auto", display: "flex", gap: 14, alignItems: "center" }}>
            <LiveStatus />
            <a
              href="https://github.com/nikhillakra2007-tech/SWARM-INTEL"
              target="_blank"
              rel="noreferrer"
              className="btn ghost"
              style={{ padding: "6px 12px", fontSize: 12 }}
            >
              GitHub ↗
            </a>
          </div>
        </header>

        <main
          key={location.pathname}
          className="page-transition"
          style={{
            padding: "24px 22px",
            display: "grid",
            gap: 22,
            maxWidth: 1320,
            margin: "0 auto",
            width: "100%",
          }}
        >
          {children}
        </main>
      </div>
    </div>
  )
}
