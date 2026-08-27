import { createContext, useContext, useEffect, useState } from "react"
type Theme="light"|"dark"|"system"
const Ctx=createContext<{theme:Theme,setTheme:(t:Theme)=>void}>({theme:"light",setTheme:()=>{}})
export function ThemeProvider({children}:{children:React.ReactNode}){
  const [theme,setTheme]=useState<Theme>(()=> (localStorage.getItem("theme") as Theme)||"light")
  useEffect(()=>{
    const resolved= theme==="system" ? (matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light") : theme
    document.documentElement.setAttribute("data-theme", resolved)
    localStorage.setItem("theme", theme)
  },[theme])
  return <Ctx.Provider value={{theme,setTheme}}>{children}</Ctx.Provider>
}
export const useTheme=()=>useContext(Ctx)
