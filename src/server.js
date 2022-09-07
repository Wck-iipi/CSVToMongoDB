const http = require('http');
const PORT = process.env.PORT || 8000;
const app = require('./app');
const server = http.createServer(app);
const {loadStudentsData} = require('./models/student.model');
const { mongoConnect} = require('./services/mongo');

async function startServer(){
  await mongoConnect();
  await loadStudentsData();
  server.listen(PORT, ()=>{
    console.log(`Listening on PORT ${PORT}...`);
  });
}
startServer();
