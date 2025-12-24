import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Diagnostics from './pages/Diagnostics';
import Treatment from './pages/Treatment';
import MentalHealth from './pages/MentalHealth';

function App() {
    return (
        <Router>
            <div className="flex bg-gray-100 min-h-screen">
                <Sidebar />
                <div className="flex-1 ml-64">
                    <Routes>
                        <Route path="/" element={<Dashboard />} />
                        <Route path="/diagnostics" element={<Diagnostics />} />
                        <Route path="/treatment" element={<Treatment />} />
                        <Route path="/mental-health" element={<MentalHealth />} />
                    </Routes>
                </div>
            </div>
        </Router>
    );
}

export default App;
