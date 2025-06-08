<template>
  <div class="progress-container">
    <div class="progress-header">
      <span class="progress-title">Daily Goal</span>
      <span class="progress-count">{{ dailyProgress }} / {{ nextGoal }}</span>
    </div>
    <div class="progress-bar">
      <div
        class="progress-bar-fill"
        :style="{ width: progressBarWidth + '%' }"
      ></div>
    </div>
    <div v-if="achievementMessage" class="achievement-reward">
      🎉 {{ achievementMessage }} 🎉
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
      default: 0,
    },
  },
  data() {
    return {
      // Define the goal tiers
      goalTiers: [5, 10, 20, 30],
    };
  },
  computed: {
    /**
     * Determines the next goal based on the current progress.
     * It finds the first goal in the tiers that is greater than the current progress.
     * If all goals are met, it displays the final goal.
     */
    nextGoal() {
      const goal = this.goalTiers.find((g) => this.dailyProgress < g);
      return goal || this.goalTiers[this.goalTiers.length - 1];
    },

    /**
     * Calculates the width of the progress bar fill.
     * The percentage is based on the progress towards the *next* goal.
     */
    progressBarWidth() {
      if (this.nextGoal === 0) return 0;
      // The progress bar can exceed 100% if the user surpasses the final goal
      return Math.min((this.dailyProgress / this.nextGoal) * 100, 100);
    },

    /**
     * Generates a reward message when a specific goal tier is achieved.
     * It checks if the current progress is greater than or equal to any goal.
     */
    achievementMessage() {
      // Find the highest goal that has been reached
      const reachedGoal = [...this.goalTiers]
        .reverse()
        .find((goal) => this.dailyProgress >= goal);

      if (reachedGoal) {
        return `Goal Achieved! You've completed ${reachedGoal} reviews today!`;
      }
      return null; // No message if no goal has been reached yet
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

/* --- Reward Message Styles --- */
.achievement-reward {
  margin-top: 1rem;
  padding: 0.8rem 1rem;
  background-color: #e8f5e9; /* Light green background */
  border-left: 5px solid #4caf50; /* Green accent border */
  color: #2e7d32; /* Dark green text */
  font-weight: 500;
  text-align: center;
  border-radius: 8px;
}
</style>
