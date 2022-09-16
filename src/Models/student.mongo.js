const mongoose = require('mongoose');
const studentSchema = new mongoose.Schema({
  name: {
    type: String,
  },
  rollNumber: {
    type: String,
  },
  fatherName: {
    type: String,
  },
  cgpa: {
    type: [ Number ],
  },
  cgpaTotal:{
    type: Number,
  },
  sgpa: {
    type:[ Number ],
  },
  year: {
    type: String,
  },
  grade: {
    type: [ String ],
  },
  cumulativePoints: {
    type: [ Number ],
  }
});
module.exports = mongoose.model("student", studentSchema);
