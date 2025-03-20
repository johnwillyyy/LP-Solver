import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import UserPage from "./pages/userPage";
import SimplexResult from "./pages/simplexResult";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UserPage />} />
        <Route path="/simplex-result" element={<SimplexResult />} />
      </Routes>
    </Router>
  );
}

export default App;
