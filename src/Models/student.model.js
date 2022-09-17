const fs = require('fs');
const path = require('path');
const studentDatabase = require('./student.mongo');
studentDatabase.collection.drop();
const {
  parse
} = require('csv-parse');

async function addNewStudent(obj) {
  obj['grade'] = obj['grade'].replace(/'/g, '"')
  Object.assign(obj, {
    cgpa: JSON.parse(obj['cgpa']),
    cgpaTotal: parseFloat(obj['cgpaTotal']),
    sgpa: JSON.parse(obj['sgpa']),
    year: parseFloat(obj['year']),
    grade: JSON.parse(obj['grade']),
    cumulativePointsSemester: JSON.parse(obj['cumulativePointsSemester']),
  })
  await insertDataInDatabase(obj);
  console.log(obj['rollNumber'] + "is done....");
}

async function insertDataInDatabase(studentObject) {
  await new studentDatabase(studentObject).save();
}

async function loadStudentsData() {
  return new Promise(async (resolve, reject) => {
    fs.createReadStream(path.join(__dirname, '..', '..', 'public', 'NITResults.csv'))
      .pipe(parse({
        columns: true,
      }))
      .on('data', async (data) => {
        // console.log(data);
        await addNewStudent(data);
      })
      .on('err', (err) => {
        console.log("loadStudentsData error" + err);
      })
      .on('end', async () => {
        console.log("The entire process ended successfully.");
      });

    // const parts = await toArrayPackage(fs.createReadStream(path.join(__dirname, '..', '..', 'public', 'NITResults.csv')));
    // const buffers = parts.map(
    //  part => (_.isBuffer(part) ? part : Buffer.from(part)),
    // );
    //
    // const buffer = Buffer.concat(buffers);
    // arr = [...parts]
    // console.log(""+parts);

  });
  // });


  // fs.readFile(path.join(__dirname, '..', '..', 'public', 'NITResults.csv'),async (err, data) =>{
  // if (err) {
  //     throw err;
  // }
  // const content = "" +data;
  // // console.log(content);
  // let array = CSVToArray(content);
  // await addNewStudent(array);
  // console.log("I am finished");


}
module.exports = {
  loadStudentsData
};
