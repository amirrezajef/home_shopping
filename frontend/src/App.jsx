import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import Dashboard from './components/Dashboard';
import ItemDetail from './components/ItemDetail';
import NewItem from './components/NewItem';
import Header from './components/Header';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-background">
        <Header />
        <main className="pt-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/items/new" element={<NewItem />} />
            <Route path="/items/:itemId" element={<ItemDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 