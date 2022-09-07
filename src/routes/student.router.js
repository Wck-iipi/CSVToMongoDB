const express = require('express');
const studentsRouter = express.Router();
const studentsController = require('./student.controller');

studentsRouter.post('/', studentsController.postStudents);

module.exports = {studentsRouter};
