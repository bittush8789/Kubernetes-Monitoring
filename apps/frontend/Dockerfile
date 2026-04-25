# Frontend Dockerfile
FROM node:18-alpine

WORKDIR /app

# Create a minimal next.js style mock
RUN echo 'const http = require("http"); \
const server = http.createServer((req, res) => { \
  if (req.url === "/health") { \
    res.writeHead(200); \
    res.end("OK"); \
  } else { \
    res.writeHead(200); \
    res.end("<h1>SRE Monitoring Frontend</h1><p>Monitoring Backend API...</p>"); \
  } \
}); \
server.listen(3000);' > server.js

EXPOSE 3000

CMD ["node", "server.js"]
