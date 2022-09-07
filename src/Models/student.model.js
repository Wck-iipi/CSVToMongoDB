const {parse} = require('csv-parse');
const fs = require('fs');
const path = require('path');
const studentDatabase = require('./student.mongo');

async function addNewStudent(studentObject) {
  await studentDatabase.insert(studentObject);
}

function loadStudentsData() {
  return new Promise((resolve, reject) => {
    fs.createReadStream(path.join(__dirname, '..', '..', 'public', 'NITResults.csv'))
    .pipe(parse({
      comment: '#',
      columns: true,
    }))
    .on('data', async (data) => {
      console.log(data);
    });

  });
}
module.exports = {loadStudentsData};
