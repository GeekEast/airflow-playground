const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.json());

// Connect to MongoDB
mongoose.connect('mongodb://localhost:27017/live-interview');

// Define JobRequisition model
const JobRequisition = mongoose.model(
  'jobRequisition',
  {
    numberOfCancelledCandidates: Number,
  },
  'jobRequisitions'
);

// POST route to update all job requisitions
app.post('/api/update-job-requisition', async (req, res) => {
  try {
    const { jobRequisitionId } = req.body;

    if (!jobRequisitionId) {
      return res.status(400).json({ error: 'jobRequisitionId is required' });
    }

    const result = await JobRequisition.findOneAndUpdate(
      { _id: new mongoose.Types.ObjectId(jobRequisitionId) },
      { $set: { numberOfCancelledCandidates: 0 } },
      { new: true }
    );

    if (!result) {
      return res.status(404).json({ error: 'Job requisition not found' });
    }

    res.json({
      message: 'Job requisition updated successfully',
      updatedJobRequisition: result,
    });
  } catch (error) {
    console.error('Error updating job requisition:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Start server
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
