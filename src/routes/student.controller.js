const launchesModel = require('../models/student.model')

function postStudents(req, res) {
  return res.status(200).send({message:"This one is running"});
}

module.exports = {postStudents};
