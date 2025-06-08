<template>
  <div class="page-container">
    <div class="review-card" v-if="currentPair">
      <div class="qa-section">
        <h2 class="question-title">Question</h2>
        <textarea
          v-model="currentPair.question"
          class="text-field"
          placeholder="Enter the question..."
        ></textarea>
      </div>

      <div class="qa-section">
        <h2 class="answer-title">Answer</h2>
        <textarea
          v-model="currentPair.answer"
          class="text-field answer-field"
          placeholder="Enter the answer..."
        ></textarea>
      </div>

      <div class="actions">
        <div class="ratings-wrapper">
          <div class="rating-group">
            <label for="question-rating">Question Rating</label>
            <input
              id="question-rating"
              type="number"
              v-model.number="questionRating"
              min="1"
              max="5"
            />
          </div>
          <div class="rating-group">
            <label for="answer-rating">Answer Rating</label>
            <input
              id="answer-rating"
              type="number"
              v-model.number="answerRating"
              min="1"
              max="5"
            />
          </div>
        </div>
        <textarea
          v-model="comment"
          class="comment-field"
          placeholder="Add an optional comment..."
        ></textarea>
        <button @click="submitReview" class="submit-button">
          Submit and Next
        </button>
      </div>
    </div>
    <div v-else class="loading-card">
      <p>Loading Q&A pair...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ReviewQa",
  props: {
    user: String,
  },
  data() {
    return {
      qaPairs: [],
      currentPair: null,
      questionRating: 3,
      answerRating: 3,
      comment: "",
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get("/qa_data.json");
        this.qaPairs = response.data.qa_pairs.filter(
          (p) => p.question && p.answer
        );
        this.getRandomPair();
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    getRandomPair() {
      if (this.qaPairs.length > 0) {
        const randomIndex = Math.floor(Math.random() * this.qaPairs.length);
        this.currentPair = { ...this.qaPairs[randomIndex] };
      } else {
        this.currentPair = {
          question: "No more questions to review!",
          answer: "Please check back later.",
        };
      }
    },
    async submitReview() {
      if (!this.user) {
        alert("Please log in to submit a review.");
        return;
      }

      // We send the final state of the question and answer
      const reviewData = {
        user: this.user,
        question: this.currentPair.question,
        answer: this.currentPair.answer,
        question_rating: this.questionRating,
        answer_rating: this.answerRating,
        comment: this.comment,
        timestamp: new Date().toISOString(),
      };

      try {
        // Send the data to our FastAPI backend
        await axios.post("/api/submit-review", reviewData);
        alert("Review submitted successfully!");

        // Reset for the next one
        this.getRandomPair();
        this.questionRating = 3;
        this.answerRating = 3;
        this.comment = "";
      } catch (error) {
        console.error("Error submitting review:", error);
        alert(
          "Failed to submit review. Check the console and ensure the backend is running."
        );
      }
    },
  },
};
</script>

<style scoped>
.page-container {
  display: flex;
  justify-content: center;
  padding: 2rem;
  background-color: #f7f9fc;
  min-height: 100vh;
}

.review-card,
.loading-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  padding: 2rem 2.5rem;
  max-width: 800px;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.loading-card {
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: #555;
}

.qa-section {
  margin-bottom: 1.5rem;
}

.question-title,
.answer-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 0.75rem;
  border-bottom: 2px solid #eee;
  padding-bottom: 0.5rem;
}

.text-field,
.comment-field {
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 0.75rem;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.text-field:focus,
.comment-field:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
}

.answer-field {
  min-height: 250px;
}

.actions {
  margin-top: 1rem;
}

.ratings-wrapper {
  display: flex;
  gap: 2rem;
  margin-bottom: 1rem;
}

.rating-group {
  display: flex;
  flex-direction: column;
}

.rating-group label {
  font-weight: 500;
  color: #555;
  margin-bottom: 0.5rem;
}

.rating-group input {
  width: 80px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  text-align: center;
  font-size: 1rem;
}

.comment-field {
  min-height: 80px;
  margin-bottom: 1rem;
}

.submit-button {
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  font-weight: bold;
  color: white;
  background-color: #4a90e2;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
}

.submit-button:hover {
  background-color: #357abd;
}

.submit-button:active {
  transform: scale(0.99);
}
</style>
