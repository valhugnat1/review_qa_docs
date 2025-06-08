<template>
  <div class="page-container">
    <div class="stats-card">
      <h2>Category Review Distribution</h2>
      <p>A breakdown of submitted reviews by category.</p>
      <div class="histogram-container">
        <div v-if="!stats.length" class="no-data">
          No category data available yet. Submit some reviews first!
        </div>
        <div v-for="stat in stats" :key="stat.category" class="bar-item">
          <span class="bar-label">{{ stat.category }}</span>
          <div class="bar-wrapper">
            <div
              class="bar"
              :style="{ width: barWidth(stat.count) + '%' }"
            ></div>
          </div>
          <span class="bar-value">{{ stat.count }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CategoryStats",
  data() {
    return {
      stats: [],
    };
  },
  computed: {
    maxCount() {
      if (this.stats.length === 0) return 0;
      return Math.max(...this.stats.map((s) => s.count));
    },
  },
  methods: {
    async fetchCategoryStats() {
      try {
        const response = await axios.get("/api/reviews/category-stats");
        this.stats = response.data;
      } catch (error) {
        console.error("Failed to load category stats:", error);
      }
    },
    barWidth(count) {
      if (this.maxCount === 0) return 0;
      return (count / this.maxCount) * 100;
    },
  },
  created() {
    this.fetchCategoryStats();
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

.stats-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  padding: 2rem 2.5rem;
  max-width: 800px;
  width: 100%;
  text-align: center;
}

h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 0.5rem;
}

p {
  font-size: 1rem;
  color: #777;
  margin-bottom: 2.5rem;
}

.histogram-container {
  width: 100%;
}

.bar-item {
  display: flex;
  align-items: center;
  margin-bottom: 1.25rem;
}

.bar-label {
  width: 120px; /* Fixed width for labels */
  text-align: right;
  padding-right: 1rem;
  font-weight: 500;
  color: #555;
  text-transform: capitalize;
}

.bar-wrapper {
  flex-grow: 1;
  background-color: #eef2f7;
  border-radius: 6px;
  height: 28px;
}

.bar {
  background: linear-gradient(90deg, #6aa9f4, #4a90e2);
  height: 100%;
  border-radius: 6px;
  transition: width 0.5s ease-in-out;
}

.bar-value {
  width: 50px; /* Fixed width for values */
  text-align: left;
  padding-left: 1rem;
  font-weight: bold;
  color: #333;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #888;
}
</style>
