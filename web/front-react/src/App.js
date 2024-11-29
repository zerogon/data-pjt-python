import './App.css';
import React, { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
      // 백엔드에서 데이터 가져오기
      fetch('http://localhost:5000/api')
          .then((response) => response.json())
          .then((data) => setMessage(data.message))
          .catch((error) => console.error('Error fetching data:', error));
  }, []);

  return (
      <div style={{ textAlign: 'center', marginTop: '50px' }}>
          <h1>React + Node.js</h1>
          <p>{message}</p>
      </div>
  );
}

export default App;
