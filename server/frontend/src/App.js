import LoginPanel from "./components/Login/Login"
import RegisterPanel from "./components/Register/Register"
import { Routes, Route } from "react-router-dom";
// add Dealer component
import Dealers from './components/Dealers/Dealers';
// Add the route for /dealers to render the Dealers component.
<Route path="/dealers" element={<Dealers/>} />

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPanel />} />
      <Route path="/register" element={<RegisterPanel />} />
    </Routes>
  );
}
export default App;
