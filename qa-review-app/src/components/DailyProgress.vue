<template>
  <div class="progress-container">
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
</template>

<script>
export default {
  name: "DailyProgress",
  props: {
    dailyProgress: {
      type: Number,
      required: true,
    },
    dailyObjective: {
      type: Number,
      required: true,
    },
  },
  computed: {
    progressBarWidth() {
      if (this.dailyObjective === 0) return 0;
      return Math.min((this.dailyProgress / this.dailyObjective) * 100, 100);
    },
  },
};
</script>

<style scoped>
/* --- Progress Bar Styles --- */
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
</style>
