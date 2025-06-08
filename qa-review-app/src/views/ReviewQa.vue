<template>
  <div class="page-container">
    <DailyProgress
      v-if="user"
      :daily-progress="dailyProgress"
      :daily-objective="dailyObjective"
    />

    <CategorySelector
      :categories="categories"
      :selected-categories="selectedCategories"
      @add-category="addCategory"
      @remove-category="removeCategory"
    />

    <ReviewCard
      v-if="currentPair"
      :key="currentPair.id"
      :pair="currentPair"
      @submit-review="handleReviewSubmission"
      @pass-question="getRandomPair"
    />

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
import confetti from "canvas-confetti";
import DailyProgress from "@/components/DailyProgress.vue";
import CategorySelector from "@/components/CategorySelector.vue";
import ReviewCard from "@/components/review/ReviewCard.vue";

export default {
  name: "ReviewQa",
  components: {
    DailyProgress,
    CategorySelector,
    ReviewCard,
  },
  props: {
    user: String,
  },
  data() {
    return {
      categories: [],
      selectedCategories: [],
      isLoading: false,
      qaPairs: [],
      currentPair: null,
      dailyProgress: 0,
      dailyObjective: 5,
    };
  },
  created() {
    this.fetchCategories();
    if (this.user) {
      this.fetchUserProgress();
    }
  },
  watch: {
    selectedCategories: {
      handler() {
        this.fetchData();
      },
      deep: true,
    },
  },
  methods: {
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
    async fetchCategories() {
      try {
        const response = await axios.get("/api/categories");
        this.categories = response.data.sort();
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
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
    addCategory(category) {
      if (category && !this.selectedCategories.includes(category)) {
        this.selectedCategories.push(category);
      }
    },
    removeCategory(index) {
      this.selectedCategories.splice(index, 1);
    },
    getRandomPair() {
      if (this.qaPairs.length > 0) {
        const randomIndex = Math.floor(Math.random() * this.qaPairs.length);
        this.currentPair = this.qaPairs[randomIndex];
        this.qaPairs.splice(randomIndex, 1);
      } else {
        this.currentPair = null;
        if (this.selectedCategories.length > 0) {
          this.fetchData();
        }
      }
    },
    async handleReviewSubmission(reviewData) {
      if (!this.user) {
        alert("Please log in to submit a review.");
        return;
      }
      const completeReviewData = {
        ...reviewData,
        user: this.user,
        timestamp: new Date().toISOString(),
        category: this.currentPair.category,
      };
      try {
        await axios.post("/api/submit-review", completeReviewData);

        // SUCCESS ALERT REMOVED

        this.dailyProgress++;
        if (this.dailyProgress === this.dailyObjective) {
          this.triggerVictoryAnimation();
        }
        this.getRandomPair(); // This fetches the next card and solves the "didn't change" issue
      } catch (error) {
        console.error("Error submitting review:", error);
        // ERROR ALERT REMAINS
        alert(
          "Failed to submit review. Check the console and ensure the backend is running."
        );
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
  },
};
</script>

<style scoped>
/* Styles remain the same */
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
