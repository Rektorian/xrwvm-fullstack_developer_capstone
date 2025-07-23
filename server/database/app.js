const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
// This is a built-in Node.js function that allows you to import modules in your application. 
// In this case, it's importing the 'cors' module, which is a Node.js package 
// that enables Cross-Origin Resource Sharing (CORS) with various options. 
// CORS is a mechanism that allows many resources (e.g., fonts, JavaScript, etc.) on a web page to be requested 
// from another domain outside the domain from which the resource originated.
const  cors = require('cors')
const app = express()
const port = 3030;

app.use(cors())
app.use(require('body-parser').urlencoded({ extended: false }));

const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

mongoose.connect("mongodb://mongo_db:27017/",{'dbName':'dealershipsDB'});

// This is a built-in Node.js function that is used to include external modules in a Node.js application. 
// The argument './review' is the path to the module file relative to the current file. In this case, 
// it's importing a module named review that is located in the same directory as the current file.
const Reviews = require('./review');

const Dealerships = require('./dealership');

/*
This JavaScript code is using the MongoDB Node.js driver to interact with a MongoDB database.
Here's a breakdown of what the code does:
1. `try { ... } catch (error) { ... }`: This is a try-catch block used for error handling.
 The code within the `try` block is executed, and if an error occurs, the code within the `catch` block is executed instead.
2. `Reviews.deleteMany({})`: This line deletes all documents from the 'Reviews' collection in the MongoDB database.
 The empty object `{}` is a query that matches all documents.
3. `.then(() => { ... })`: This is a method of a Promise returned by the `deleteMany()` method.
 It specifies a callback function to be executed once the `deleteMany()` operation is completed,
 regardless of whether it succeeded or failed. In this case, the callback function inserts new documents into
 the 'Reviews' collection using the `insertMany()` method.
4. `Reviews.insertMany(reviews_data['reviews'])`: This line inserts multiple documents into the 'Reviews' collection.
 The `reviews_data['reviews']` is an array of documents to be inserted.
5. The same pattern is repeated for the 'Dealerships' collection, with `deleteMany()` and `insertMany()`
 methods used to clear and repopulate the collection, respectively.
6. If an error occurs during the execution of the `try` block, the `catch` block is executed.
 In this case, it sends a JSON response with a status code of 500 (Internal Server Error) and a message
 indicating that there was an error fetching documents.

In summary, this code attempts to clear and repopulate the 'Reviews' and 'Dealerships' collections in a
MongoDB database. If an error occurs during this process, it sends a 500 error response to the client.
Please note that the `reviews_data` and `dealerships_data` variables are assumed to be defined elsewhere in the code,
containing the data to be inserted into the respective collections.
*/

try {
  Reviews.deleteMany({}).then(()=>{
    Reviews.insertMany(reviews_data['reviews']);
  });
  Dealerships.deleteMany({}).then(()=>{
    Dealerships.insertMany(dealerships_data['dealerships']);
  });
  
} catch (error) {
  res.status(500).json({ error: 'Error fetching documents' });
}


// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

/**
 * Express route to fetch reviews by a particular dealer
 * 1. `app.get('/fetchReviews/dealer/:id', async (req, res) => { ... })`: This line defines a new route handler for GET requests to the `/fetchReviews/dealer/:id` endpoint. The `:id` part in the route path is a parameter that captures the value following `/dealer/` in the URL.
 * 2. `const documents = await Reviews.find({dealership: req.params.id})`: This line uses the MongoDB Node.js driver to find all documents in the 'Reviews' collection where the 'dealership' field matches the `:id` parameter from the request URL. The `find()` method returns a cursor, and the `await` keyword is used to pause the execution of the function until the promise returned by `find()` is resolved.
 * 3. `res.json(documents)`: This line sends a JSON response containing the found documents.
 * 4. The `try-catch` block is used for error handling. If an error occurs during the execution of the `try` block (e.g., a problem with the database query), the `catch` block is executed instead. In this case, it sends a JSON response with a status code of 500 (Internal Server Error) and a message indicating that there was an error fetching documents.
 * 
 * In summary, this code defines a route handler that fetches all reviews associated with a specific dealership (identified by the `:id` parameter in the URL) from the 'Reviews' collection in a MongoDB database and sends them as a JSON response. If an error occurs during this process, it sends a 500 error response to the client.
 */
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await Reviews.find({dealership: req.params.id});
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
//Write your code here
  try {
    const documents = await Dealerships.find();
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
//Write your code here
  try {
    const documents = await Dealerships.find({state: req.params.state});
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
  });

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
//Write your code here
  try {
    const documents = await Reviews.find({id: req.params.id});
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
  });

//Express route to insert review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  data = JSON.parse(req.body);
  const documents = await Reviews.find().sort( { id: -1 } )
  let new_id = documents[0]['id']+1

  const review = new Reviews({
		"id": new_id,
		"name": data['name'],
		"dealership": data['dealership'],
		"review": data['review'],
		"purchase": data['purchase'],
		"purchase_date": data['purchase_date'],
		"car_make": data['car_make'],
		"car_model": data['car_model'],
		"car_year": data['car_year'],
	});

  try {
    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
		console.log(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
