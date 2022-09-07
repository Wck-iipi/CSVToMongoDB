const express = require('express');
const app = express();
const path = require('path');

const {studentsRouter} = require('./routes/student.router');

app.use(express.json());
app.use(express.static(path.join(__dirname, '..', 'public' )));
app.use('/students', studentsRouter);

app.get('/' , (req, res)=>{
  res.send("Data time");
});
module.exports = app;
