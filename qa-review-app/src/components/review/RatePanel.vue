<template>
  <div class="rate-panel">
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
      <button @click="submit" class="submit-button">Submit and Next</button>
      <button @click="$emit('cancel-rate')" class="cancel-button">
        Cancel
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "RatePanel",
  data() {
    return {
      questionRating: 3,
      answerRating: 3,
      comment: "",
    };
  },
  methods: {
    submit() {
      this.$emit("submit-review", {
        question_rating: this.questionRating,
        answer_rating: this.answerRating,
        comment: this.comment,
      });
    },
  },
};
</script>

<style scoped>
/* --- Rate Panel Styles --- */
.panel-title {
  font-size: 1.3rem;
  text-align: center;
  margin-bottom: 1.5rem;
  color: #444;
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
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 0.75rem;
  font-size: 1rem;
  font-family: inherit;
  min-height: 80px;
  margin-bottom: 1.5rem;
}
.panel-actions {
  display: flex;
  gap: 1rem;
}
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
.submit-button {
  color: white;
  background-color: #4a90e2;
}
.submit-button:hover {
  background-color: #357abd;
}
.cancel-button {
  background-color: #f1f1f1;
  color: #555;
  border: 1px solid #ddd;
}
.cancel-button:hover {
  background-color: #e9e9e9;
}
</style>
