// This is the entry point for the backend server
// Using the ES6 syntax

import express from 'express';
import cors from 'cors';
import {sql} from './db.js';

// CORS options for frontend access
const corsOptions = {
    origin: 'http://localhost:5173',
    credentials: false,
    methods: "POST, GET"
}

// Creating the express app
const app = express();
app.use(express.json());
app.use(cors(corsOptions));




// Starting the server
app.listen(3000,()=>{
    console.log("Server is running on port 3000");
});