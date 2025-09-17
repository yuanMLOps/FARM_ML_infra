
import {
  createBrowserRouter,
  Route,
  createRoutesFromElements,
  RouterProvider
} from "react-router-dom"

import AuthRequired from "./components/AuthRequired"

import RootLayout from "./layouts/RootLayout"

import Home from "./pages/Home"
import Login from "./pages/Login"
import Formulations from "./pages/Formulations"
import {formulationsLoader} from "./loaders/formulations_loader"
import NewFormulation from "./pages/NewFormulation"
import SingleFormulation from "./pages/SingleFormulation"
import NotFound from "./pages/NotFound"
import { AuthProvider } from "./contexts/AuthContext"


const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<RootLayout />}>
      <Route index element={<Home />} />
      <Route path="formulations" element={<Formulations />} 
      loader={formulationsLoader}/>
      <Route path="login" element={<Login />} />
      <Route element={<AuthRequired/>}>
        <Route path="new-formulation" element={<NewFormulation />} />
      </Route>
      <Route path="formulations/:id" element={<SingleFormulation />} />  
      <Route path="*" element={<NotFound />} />         
    </Route>
  )
)

export default function App() {
  return (
    <AuthProvider>
       <RouterProvider router={router} />
    </AuthProvider>
    
  )
}