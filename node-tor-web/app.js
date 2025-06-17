const express = require('express');
const app = express();

const PORT = 8080;

app.get('/', (req, res) => {
  res.send('Hello from Tor Express web!');
});

app.listen(PORT, () => {
  console.log(`Express server listening on http://localhost:${PORT}`);
});
