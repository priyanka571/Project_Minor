// Backend Structure (Node.js)
// server.js
const express = require('express');
const mongoose = require('mongoose');
const qr = require('qrcode');
const multer = require('multer');
const cors = require('cors');

// User Model
const userSchema = new mongoose.Schema({
  user_id: { type: String, required: true, unique: true },
  user_name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true }
});

// Event Model
const eventSchema = new mongoose.Schema({
  event_id: { type: String, required: true, unique: true },
  event_name: { type: String, required: true },
  event_des: String,
  user_id: { type: String, required: true },
  created_at: { type: Date, default: Date.now }
});

// Image Model
const imageSchema = new mongoose.Schema({
  photo_id: { type: String, required: true, unique: true },
  event_id: { type: String, required: true },
  photo_url: { type: String, required: true },
  uploaded_by: { type: String, required: true },
  uploaded_at: { type: Date, default: Date.now }
});

// QR Model
const qrSchema = new mongoose.Schema({
  qr_id: { type: String, required: true, unique: true },
  event_id: { type: String, required: true },
  qr_data: { type: String, required: true },
  generated_at: { type: Date, default: Date.now }
});

// API Routes
app.post('/api/register', async (req, res) => {
  // User registration logic
});

app.post('/api/login', async (req, res) => {
  // User login logic
});

app.post('/api/events', auth, async (req, res) => {
  // Create event logic
});

app.post('/api/upload', auth, upload.array('photos'), async (req, res) => {
  // Photo upload logic
});

app.post('/api/generate-qr', auth, async (req, res) => {
  // QR generation logic
});

app.get('/api/photos/:eventId', async (req, res) => {
  // Fetch photos by event ID
});




// ############ frontend part
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { QrReader } from 'react-qr-reader';

const App = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow-lg">
          <div className="max-w-6xl mx-auto px-4">
            <div className="flex justify-between items-center py-4">
              <div className="text-xl font-bold">PIXCODE</div>
              <div className="space-x-4">
                <button className="bg-blue-500 text-white px-4 py-2 rounded">Login</button>
                <button className="bg-green-500 text-white px-4 py-2 rounded">Register</button>
              </div>
            </div>
          </div>
        </nav>
        
        <main className="max-w-6xl mx-auto mt-8 px-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/scan" element={<QRScanner />} />
            <Route path="/event/:id" element={<EventGallery />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

const QRScanner = () => {
  const [data, setData] = useState('');

  const handleScan = (result) => {
    if (result) {
      setData(result?.text);
      // Navigate to event gallery with the scanned event ID
    }
  };

  return (
    <div className="max-w-md mx-auto">
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold mb-4">Scan QR Code</h2>
        <QrReader
          onResult={handleScan}
          className="w-full"
          constraints={{ facingMode: 'environment' }}
        />
        {data && <p className="mt-4">Redirecting to gallery...</p>}
      </div>
    </div>
  );
};

export default App;