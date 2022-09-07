const fs = require('fs');
const path = require('path');
const studentDatabase = require('./student.mongo');

async function addNewStudent(array) {
  let currentObject = {}

  for (var i = 0; i < array.length; i++) {
    currentSemester = 0;

    if (array[i][3] == "NULL") {
      currentObject["grade"] = [[]];
      currentObject["name"] = array[i][2];
      currentObject["rollNumber"] = array[i][0];
      currentObject["fatherName"] = array[i][1];
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
        currentSemester++;
        currentObject["grade"].push([]);
      }
    }


    else if (array[i][1] == "NewLine"){
      currentObject["cgpaTotal"] = parseFloat(array[i-1][3].split("=")[1]);
      currentObject['grade'].pop();


      await insertDataInDatabase(currentObject);
      currentObject = {};

    }else if (array[i][0] == ''){

    }else{
      currentObject["grade"][currentSemester].push(array[i]);
    }

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

}

function loadStudentsData() {
  return new Promise((resolve, reject) => {
    fs.createReadStream(path.join(__dirname, '..', '..', 'public', 'NITResults.csv'))
    .on('data', async (data) => {

      let array = CSVToArray((""+data));
      addNewStudent(array);
    });

  });
}
module.exports = {loadStudentsData};
