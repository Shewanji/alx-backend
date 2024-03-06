const chai = require('chai');
const expect = chai.expect;
const kue = require('kue');
import createPushNotificationsJobs from "./8-job.js";

const queue = kue.createQueue();

// Enter the test mode without processing jobs
queue.testMode.enter();

describe('createPushNotificationsJobs', () => {
  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs(null, queue)).to.throw('Jobs is not an array');
  });

  it('should create jobs and add them to the queue', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
      { phoneNumber: '4153518781', message: 'This is the code 4562 to verify your account' },
      { phoneNumber: '4153518743', message: 'This is the code 4321 to verify your account' }
    ];

    createPushNotificationsJobs(jobs, queue);

    // Validate the number of jobs in the queue
    expect(queue.testMode.jobs.length).to.equal(jobs.length);

    // Validate the type of jobs in the queue
    expect(queue.testMode.jobs.map(job => job.type)).to.deep.equal(jobs.map(() => 'push_notification_code_3'));

    // Validate the data of each job in the queue
    jobs.forEach((jobData, index) => {
      expect(queue.testMode.jobs[index].data).to.deep.equal(jobData);
    });
  });
});

// Clear the queue and exit the test mode after executing the tests
after(() => {
  queue.testMode.clear();
  queue.testMode.exit();
});
