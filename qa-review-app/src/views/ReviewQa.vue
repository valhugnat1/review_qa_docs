<template>
  <div class="page-container">
    <div v-if="user" class="progress-container">
      <div class="progress-header">
        <span class="progress-title">Daily Goal</span>
        <span class="progress-count"
          >{{ dailyProgress }} / {{ dailyObjective }}</span
        >
      </div>
      <div class="progress-bar">
        <div
          class="progress-bar-fill"
          :style="{ width: progressBarWidth + '%' }"
        ></div>
      </div>
    </div>

    <div class="category-selector-card">
      <h3 class="panel-title">Select Categories to Review</h3>
      <div class="selector-content">
        <select
          @change="addCategory($event.target.value)"
          class="category-dropdown"
          :disabled="availableCategories.length === 0"
        >
          <option disabled selected value="">
            {{
              availableCategories.length > 0
                ? "-- Add a category --"
                : "-- All categories selected --"
            }}
          </option>
          <option v-for="cat in availableCategories" :key="cat" :value="cat">
            {{ cat }}
          </option>
        </select>
        <div class="selected-tags-container">
          <span
            v-for="(tag, index) in selectedCategories"
            :key="tag"
            class="category-tag"
          >
            {{ tag }}
            <button
              @click="removeCategory(index)"
              class="remove-tag-btn"
              title="Remove category"
            >
              ×
            </button>
          </span>
          <span v-if="!selectedCategories.length" class="no-tags-placeholder">
            Select one or more categories to begin.
          </span>
        </div>
      </div>
    </div>

    <div v-if="currentPair" class="review-card">
      <div class="qa-content">
        <div class="qa-section">
          <h2 class="question-title">Question</h2>
          <div class="content-display" v-html="formattedQuestion"></div>
        </div>
        <div class="qa-section">
          <h2 class="answer-title">Answer</h2>
          <div class="content-display" v-html="formattedAnswer"></div>
        </div>
      </div>

      <div class="actions-panel">
        <div v-if="mode === 'view'" class="view-actions">
          <button @click="setMode('rate')" class="action-button">Rate</button>
          <button @click="setMode('edit')" class="action-button secondary">
            Edit
          </button>
          <button @click="passQuestion" class="action-button pass-button">
            Pass
          </button>
        </div>

        <div v-else-if="mode === 'edit'" class="edit-panel">
          <h3 class="panel-title">Edit Q&A</h3>
          <div class="qa-section">
            <label class="text-field-label">Edit Question</label>
            <textarea
              v-model="editablePair.question"
              class="text-field"
            ></textarea>
          </div>
          <div class="qa-section">
            <label class="text-field-label">Edit Answer</label>
            <textarea
              v-model="editablePair.answer"
              class="text-field answer-field"
            ></textarea>
          </div>
          <div class="panel-actions">
            <button @click="submitEditedContent" class="submit-button">
              Submit Changes
            </button>
            <button @click="setMode('view')" class="cancel-button">
              Cancel
            </button>
          </div>
        </div>

        <div v-else-if="mode === 'rate'" class="rate-panel">
          <h3 class="panel-title">Rate this Q&A</h3>
          <div class="ratings-wrapper">
            <div class="rating-group">
              <label>Question Rating</label>
              <div class="star-rating">
                <span
                  v-for="n in 5"
                  :key="n"
                  @click="questionRating = n"
                  :class="{ filled: n <= questionRating }"
                  >★</span
                >
              </div>
            </div>
            <div class="rating-group">
              <label>Answer Rating</label>
              <div class="star-rating">
                <span
                  v-for="n in 5"
                  :key="n"
                  @click="answerRating = n"
                  :class="{ filled: n <= answerRating }"
                  >★</span
                >
              </div>
            </div>
          </div>
          <textarea
            v-model="comment"
            class="comment-field"
            placeholder="Add an optional comment..."
          ></textarea>
          <div class="panel-actions">
            <button @click="submitReview" class="submit-button">
              Submit and Next
            </button>
            <button @click="setMode('view')" class="cancel-button">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="loading-card">
      <p v-if="isLoading">Loading Q&A pairs...</p>
      <p v-else-if="!selectedCategories.length">
        Please select one or more categories to start reviewing.
      </p>
      <p v-else>
        No more questions available for the selected categories. Try adding more
        categories!
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { marked } from "marked";
import hljs from "highlight.js";
import confetti from "canvas-confetti";

export default {
  name: "ReviewQa",
  props: {
    user: String,
  },
  data() {
    return {
      // NEW: State for category management
      categories: [],
      selectedCategories: [],
      isLoading: false,

      // Existing state
      qaPairs: [],
      currentPair: null,
      editablePair: { question: "", answer: "" },
      questionRating: 3,
      answerRating: 3,
      comment: "",
      mode: "view", // 'view', 'edit', 'rate'
      dailyProgress: 0,
      dailyObjective: 5,
    };
  },
  created() {
    this.configureMarked();
    // Fetch categories when the component is created
    this.fetchCategories();
    if (this.user) {
      this.fetchUserProgress();
    }
  },
  watch: {
    // NEW: Watch for changes in selected categories to fetch new data
    selectedCategories: {
      handler() {
        this.fetchData();
      },
      deep: true, // Necessary because we are watching an array
    },
  },
  computed: {
    // NEW: Computed property to find categories that are not yet selected
    availableCategories() {
      return this.categories.filter(
        (c) => !this.selectedCategories.includes(c)
      );
    },
    formattedQuestion() {
      return this.currentPair?.question
        ? marked(this.currentPair.question)
        : "";
    },
    formattedAnswer() {
      return this.currentPair?.answer ? marked(this.currentPair.answer) : "";
    },
    progressBarWidth() {
      if (this.dailyObjective === 0) return 0;
      return Math.min((this.dailyProgress / this.dailyObjective) * 100, 100);
    },
  },
  methods: {
    configureMarked() {
      marked.setOptions({
        highlight: function (code, lang) {
          const language = hljs.getLanguage(lang) ? lang : "plaintext";
          return hljs.highlight(code, { language }).value;
        },
        langPrefix: "hljs language-",
        gfm: true,
        breaks: true,
      });
    },

    // MODIFIED: Fetches data based on the selected categories from the new API endpoint
    async fetchData() {
      if (this.selectedCategories.length === 0) {
        this.qaPairs = [];
        this.currentPair = null;
        return;
      }
      this.isLoading = true;
      try {
        const categoryQuery = this.selectedCategories
          .map((cat) => `categories=${encodeURIComponent(cat)}`)
          .join("&");
        const response = await axios.get(`/api/questions?${categoryQuery}`);
        this.qaPairs = response.data.qa_pairs.filter(
          (p) => p.question && p.answer
        );
        this.getRandomPair();
      } catch (error) {
        console.error("Error fetching data:", error);
        this.qaPairs = [];
        this.currentPair = null;
      } finally {
        this.isLoading = false;
      }
    },

    // NEW: Method to fetch the list of available categories from the backend
    async fetchCategories() {
      try {
        const response = await axios.get("/api/categories");
        this.categories = response.data.sort(); // Sort categories alphabetically
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    },

    // NEW: Method to add a category to the selection list
    addCategory(category) {
      if (category && !this.selectedCategories.includes(category)) {
        this.selectedCategories.push(category);
      }
      // Reset dropdown
      event.target.value = "";
    },

    // NEW: Method to remove a category from the selection list
    removeCategory(index) {
      this.selectedCategories.splice(index, 1);
    },

    getRandomPair() {
      if (this.qaPairs.length > 0) {
        const randomIndex = Math.floor(Math.random() * this.qaPairs.length);
        this.currentPair = { ...this.qaPairs[randomIndex] };
        // Remove the selected pair to avoid repetition until the list is exhausted
        this.qaPairs.splice(randomIndex, 1);
      } else {
        this.currentPair = null;
      }
      this.resetState();
    },

    passQuestion() {
      // This will now get a new random question from the remaining pool
      this.getRandomPair();
    },

    setMode(newMode) {
      if (newMode === "edit") {
        this.editablePair = { ...this.currentPair };
      }
      this.mode = newMode;
    },

    resetState() {
      this.mode = "view";
      this.questionRating = 3;
      this.answerRating = 3;
      this.comment = "";
      this.editablePair = { question: "", answer: "" };
    },

    submitEditedContent() {
      this.currentPair.question = this.editablePair.question;
      this.currentPair.answer = this.editablePair.answer;
      this.submitReview();
    },

    async fetchUserProgress() {
      try {
        const response = await axios.get(
          `/api/reviews/progress?user=${this.user}`
        );
        this.dailyProgress = response.data.daily_count;
      } catch (error) {
        console.error("Error fetching user progress:", error);
      }
    },

    triggerVictoryAnimation() {
      confetti({
        particleCount: 150,
        spread: 90,
        origin: { y: 0.6 },
        angle: 90,
      });
    },

    // MODIFIED: Submits review with the question's category
    async submitReview() {
      if (!this.user) {
        alert("Please log in to submit a review.");
        return;
      }

      const reviewData = {
        user: this.user,
        question: this.currentPair.question,
        answer: this.currentPair.answer,
        question_rating: this.questionRating,
        answer_rating: this.answerRating,
        comment: this.comment,
        timestamp: new Date().toISOString(),
        // NEW: Include the category of the question being reviewed
        category: this.currentPair.category,
      };

      try {
        await axios.post("/api/submit-review", reviewData);
        alert("Review submitted successfully!");

        this.dailyProgress++;
        if (this.dailyProgress === this.dailyObjective) {
          this.triggerVictoryAnimation();
        }

        this.getRandomPair(); // Move to the next question
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
/* --- Main Styles --- */
.page-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  background-color: #f7f9fc;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
}

/* --- Progress Bar --- */
.progress-container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  padding: 1rem 1.5rem;
  max-width: 800px;
  width: 100%;
  margin-bottom: 2rem;
}
.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}
.progress-title {
  font-weight: 600;
  color: #333;
}
.progress-count {
  font-weight: bold;
  color: #4a90e2;
  font-size: 1.1rem;
}
.progress-bar {
  width: 100%;
  height: 12px;
  background-color: #e9ecef;
  border-radius: 6px;
  overflow: hidden;
}
.progress-bar-fill {
  height: 100%;
  background-image: linear-gradient(45deg, #4a90e2, #55d7ff);
  border-radius: 6px;
  transition: width 0.5s ease-in-out;
}

/* --- NEW: Category Selector --- */
.category-selector-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  padding: 1.5rem 2.5rem;
  max-width: 800px;
  width: 100%;
  margin-bottom: 2rem;
}
.selector-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.category-dropdown {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  background-color: #fff;
  cursor: pointer;
}
.category-dropdown:disabled {
  background-color: #f8f8f8;
  cursor: not-allowed;
}
.selected-tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding: 0.5rem;
  min-height: 40px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  align-items: center;
}
.no-tags-placeholder {
  color: #999;
  padding-left: 0.5rem;
  font-style: italic;
}
.category-tag {
  display: inline-flex;
  align-items: center;
  background-color: #4a90e2;
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 16px;
  font-weight: 500;
  font-size: 0.9rem;
  animation: fadeIn 0.3s ease-in-out;
}
.remove-tag-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  font-weight: bold;
  margin-left: 0.5rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  opacity: 0.7;
  transition: opacity 0.2s;
}
.remove-tag-btn:hover {
  opacity: 1;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* --- Review Card --- */
.review-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  padding: 2rem 2.5rem;
  max-width: 800px;
  width: 100%;
}
.qa-section {
  margin-bottom: 1.5rem;
}
.question-title,
.answer-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
  border-bottom: 2px solid #eee;
  padding-bottom: 0.5rem;
}
.content-display {
  line-height: 1.7;
  color: #333;
}
.content-display :deep(p) {
  margin-bottom: 1em;
}
.content-display :deep(pre) {
  background-color: #282c34;
  color: #abb2bf;
  border-radius: 8px;
  padding: 1rem;
  overflow-x: auto;
  font-family: "Fira Code", "Courier New", Courier, monospace;
}
.content-display :deep(code) {
  font-size: 0.95em;
}

/* --- Panels (Actions, Edit, Rate) --- */
.actions-panel {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e9ecef;
}
.panel-title {
  font-size: 1.3rem;
  text-align: center;
  margin-bottom: 1.5rem;
  color: #444;
}
.text-field-label {
  display: block;
  font-weight: 500;
  color: #555;
  margin-bottom: 0.5rem;
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
  min-height: 200px;
}
.ratings-wrapper {
  display: flex;
  justify-content: space-around;
  gap: 2rem;
  margin-bottom: 1.5rem;
  text-align: center;
}
.rating-group label {
  font-weight: 500;
  color: #555;
  margin-bottom: 0.75rem;
  display: block;
}
.star-rating {
  cursor: pointer;
  font-size: 2.2rem;
  display: inline-block;
}
.star-rating span {
  transition: color 0.2s;
  color: #d1d5db;
}
.star-rating span.filled {
  color: #f59e0b;
}
.star-rating:hover span {
  color: #facc15;
}
.star-rating span:hover ~ span {
  color: #d1d5db;
}
.comment-field {
  min-height: 80px;
  margin-bottom: 1.5rem;
}
.view-actions,
.panel-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.action-button,
.submit-button,
.cancel-button {
  flex-grow: 1;
  padding: 0.9rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.submit-button,
.action-button {
  color: white;
  background-color: #4a90e2;
}
.submit-button:hover,
.action-button:hover {
  background-color: #357abd;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
.action-button.secondary {
  background-color: #6c757d;
}
.action-button.secondary:hover {
  background-color: #5a6268;
}
.action-button.pass-button {
  background-color: #ef6c00;
}
.action-button.pass-button:hover {
  background-color: #e65100;
}
.cancel-button {
  background-color: #f1f1f1;
  color: #555;
  border: 1px solid #ddd;
}
.cancel-button:hover {
  background-color: #e9e9e9;
}

/* --- Loading / Placeholder Card --- */
.loading-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  padding: 4rem;
  text-align: center;
  color: #666;
  max-width: 800px;
  width: 100%;
  font-size: 1.1rem;
}
</style>
