const mongoose = require('mongoose');
const studentSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  rollNumber: {
    type: String,
    required: true,
  },
  fatherName: {
    type: String,
    required: true,
  },
  cgpa: {
    type: Number,
    required: true,
  },
  sgpa: {
    type:[ Number ],
    required: true,
  },
  year: {
    type: String,
    required: true,
  },
  grade: {
    type: [ String ],
    required: true,
  }
});
module.exports = mongoose.model("student", studentSchema);
