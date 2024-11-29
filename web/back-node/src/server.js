const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 5000;

app.use(cors()); // React와 통신을 위해 CORS 허용

// 간단한 API
app.get('/api', (req, res) => {
    res.json({ message: 'Hello World from Node.js!' });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
