const fs = require('fs');
const path = require('path');
const toArrayPackage = require('stream-to-array');
const studentDatabase = require('./student.mongo');

async function addNewStudent(array) {

  let currentObject = {};
  try{

    for (var i = 0; i < array.length; i++) {

      if (array[i][3] == "NULL") {

        currentObject["grade"] = [];
        currentObject["name"] = array[i][2].trim();
        currentObject["rollNumber"] = array[i][0].trim();
        currentObject["fatherName"] = array[i][1].trim();
        if (array[i][0][2].toLowerCase() == 'b' || array[i][0][2].toLowerCase() == 'm') {
          currentObject["year"] = array[i][0].substring(0,3);
        }else {
          currentObject["year"] = array[i][0].substring(0,2);
        }
      }
      else if (array[i][5] == 'New Semester\r') {
        // const currentNumber = parseInt(array[i][0].replace('S',''));
        const currentSGPA = parseFloat(array[i][1].split('=')[1]);
        const currentCGPA = parseFloat(array[i][3].split('=')[1]);

        if ("sgpa" in currentObject) {
          currentObject["sgpa"].push(currentSGPA)
        }else {
          currentObject["sgpa"] = [currentSGPA]
        }

        if ("cgpa" in currentObject) {
          currentObject["cgpa"].push(currentCGPA)
        }else {
          currentObject["cgpa"] = [currentCGPA]
        }
        if (array[i+1][2] != 'NewLine') {
          currentObject["grade"].push("Delimiter");
        }
      }


      else if (array[i][1] == "NewLine"){

        if (parseFloat(array[i-1][3].split("=")[1]) === NaN) {
          currentObject["cgpaTotal"] = 0;
        }else{

          currentObject["cgpaTotal"] = parseFloat(array[i-1][3].split("=")[1]);
        }

        // console.log(currentObject);
        await insertDataInDatabase(currentObject);
        currentObject = {};

      }else if (array[i][0] == ''){

      }else{
        currentObject["grade"].push(...array[i]);
      }

    }


  } catch(err) {
    console.log("Error in database; "+ err);
  }
  // await studentDatabase.insert(studentObject);


}
function CSVToArray(data, delimiter = ',', omitFirstRow = false){
  return data
    .slice(omitFirstRow ? data.indexOf('\n') + 1 : 0)
    .split('\n')
    .map(v => v.split(delimiter));
}

async function insertDataInDatabase(studentObject) {
  await new studentDatabase(studentObject).save();
}

async function loadStudentsData() {
  return new Promise(async (resolve, reject) => {
    fs.readFile(path.join(__dirname, '..', '..', 'public', 'NITResults.csv'),async (err, data) =>{
    if (err) {
        throw err;
    }
    const content = "" +data;
    // console.log(content);
    let array = CSVToArray(content);
    await addNewStudent(array);
    console.log("I am finished");

    });
  });




    // var parse = fs.createReadStream(path.join(__dirname, '..', '..', 'public', 'NITResults.csv'))
    // .on('data', async (data) => {
    //   // parse.pause();
    //   // let array = CSVToArray((""+data));
    //   // await addNewStudent(array);
    //   // parse.resume();
    //   // this.toArrayPackage((err,arr) => {
    //   //   addNewStudent(arr);
    //   // });
    // })
    // .on('err', (err) => {
    //   console.log("loadStudentsData errror" + err);
    // })
    // .on('end', async () => {
    //   console.log("The entire process ended successfully.");
    // });

    // const parts = await toArrayPackage(fs.createReadStream(path.join(__dirname, '..', '..', 'public', 'NITResults.csv')));
    // // const buffers = parts.map(
    // //  part => (_.isBuffer(part) ? part : Buffer.from(part)),
    // // );
    // //
    // // const buffer = Buffer.concat(buffers);
    // // arr = [...parts]
    // // console.log(""+parts);
}
module.exports = {loadStudentsData};
