const express = require('express');
const cors = require('cors');
const redis = require("redis");
const app = express();
const PORT = 8080;

const client = redis.createClient({
    host: "redis-server",
    port: 6379
})

client.set("number", 40);

app.use(cors()); // React와 통신을 위해 CORS 허용

// 간단한 API
app.get('/api', (req, res) => {
    client.get("number", (err, number) => {
        res.send("number: " + number)
        client.set("number", parseInt(number) + 1)
    })
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
