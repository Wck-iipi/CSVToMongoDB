const mongoose = require('mongoose');
const MONGO_URL = 'mongodb+srv://admin:admin@cluster0.nhltug1.mongodb.net/NITHamirpurResultsDatabase?retryWrites=true&w=majority';

mongoose.connection.once('open', () => {
  console.log("Mongoose connection is ready");
});

mongoose.connection.on('error', (err) => {
  console.log(err);
});

async function mongoConnect() {
  await mongoose.connect(MONGO_URL, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  });
}

module.exports = mongoConnect;
