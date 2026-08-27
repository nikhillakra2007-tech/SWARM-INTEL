import { BrowserRouter, Routes, Route } from "react-router-dom"
import { Layout } from "./components/Layout"
import Dashboard from "./pages/Dashboard"
import Analyze from "./pages/Analyze"
import Clusters from "./pages/Clusters"
import ClusterDetail from "./pages/ClusterDetail"
import { Customers, Applications, Loans, Devices, Dealers, Signals, Alerts, Investigations, Networks, RiskPage } from "./pages/GenericList"
import { ThemeProvider } from "./lib/theme"
import { useEffect } from "react"
import Lenis from "lenis"

function LenisProvider({children}:{children:React.ReactNode}){
  useEffect(()=>{
    const lenis=new Lenis({autoRaf:true})
    return()=>{ lenis.destroy() }
  },[])
  return <>{children}</>
}

export default function App(){
  return <ThemeProvider><LenisProvider><BrowserRouter>
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard/>}/>
        <Route path="/analyze" element={<Analyze/>}/>
        <Route path="/networks" element={<Networks/>}/>
        <Route path="/clusters" element={<Clusters/>}/>
        <Route path="/clusters/:id" element={<ClusterDetail/>}/>
        <Route path="/risk" element={<RiskPage/>}/>
        <Route path="/signals" element={<Signals/>}/>
        <Route path="/alerts" element={<Alerts/>}/>
        <Route path="/investigations" element={<Investigations/>}/>
        <Route path="/customers" element={<Customers/>}/>
        <Route path="/applications" element={<Applications/>}/>
        <Route path="/loans" element={<Loans/>}/>
        <Route path="/devices" element={<Devices/>}/>
        <Route path="/dealers" element={<Dealers/>}/>
      </Routes>
    </Layout>
  </BrowserRouter></LenisProvider></ThemeProvider>
}
