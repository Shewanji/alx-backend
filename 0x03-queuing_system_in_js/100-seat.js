const express = require('express');
const kue = require('kue');
const { promisify } = require('util');

const app = express();
const queue = kue.createQueue();

// Redis client
const redis = require('redis');
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Initialize available seats
let numberOfAvailableSeats = 50;
let reservationEnabled = true;

// Function to reserve a seat
async function reserveSeat() {
  await setAsync('available_seats', numberOfAvailableSeats);
}

// Function to get current available seats
async function getCurrentAvailableSeats() {
  const availableSeats = await getAsync('available_seats');
  return parseInt(availableSeats);
}

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  res.json({ numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (!err) {
      res.json({ status: 'Reservation in process' });
    } else {
      res.json({ status: 'Reservation failed' });
    }
  });
});

// Event listener for job completion
queue.on('job complete', (id) => {
  kue.Job.get(id, (err, job) => {
    if (err) return;
    console.log(`Seat reservation job ${job.id} completed`);
  });
});

// Process the queue and decrease available seats
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  // Get current available seats
  const currentAvailableSeats = await getCurrentAvailableSeats();

  // Check if there are enough seats available
  if (currentAvailableSeats === 0) {
    reservationEnabled = false;
  } else if (currentAvailableSeats > 0) {
    // Decrease the number of available seats
    numberOfAvailableSeats--;
    await reserveSeat();
  }

  // Check if reservationEnabled should be set to false
  if (numberOfAvailableSeats === 0) {
    reservationEnabled = false;
  }
});

// Start the server
const PORT = 1245;
app.listen(PORT, () => {
	console.log(`Server is running on port ${PORT}`);
});
