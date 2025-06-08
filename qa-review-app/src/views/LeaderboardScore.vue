<template>
  <div class="page-container">
    <div class="leaderboard-card">
      <h2>Leaderboard</h2>
      <p>Top contributors based on the number of reviews submitted.</p>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>User</th>
              <th>Reviews</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="leaderboard.length === 0">
              <td colspan="3" class="no-data">No reviews submitted yet.</td>
            </tr>
            <tr v-for="(user, index) in leaderboard" :key="user.name">
              <td class="rank">{{ index + 1 }}</td>
              <td class="user-name">{{ user.name }}</td>
              <td class="review-count">{{ user.count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "LeaderboardScore",
  data() {
    return {
      reviews: [],
    };
  },
  computed: {
    leaderboard() {
      const userCounts = this.reviews.reduce((acc, review) => {
        acc[review.user] = (acc[review.user] || 0) + 1;
        return acc;
      }, {});

      return Object.entries(userCounts)
        .map(([name, count]) => ({ name, count }))
        .sort((a, b) => b.count - a.count);
    },
  },
  created() {
    this.fetchReviews();
  },
  methods: {
    async fetchReviews() {
      try {
        // Fetch reviews from our FastAPI backend API
        const response = await axios.get("/api/reviews");
        this.reviews = response.data;
      } catch (error) {
        console.error("Could not load reviews:", error);
        // Handle error gracefully, e.g., show a message to the user
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

.leaderboard-card {
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
  margin-bottom: 2rem;
}

.table-container {
  width: 100%;
  overflow-x: auto; /* For responsiveness on small screens */
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

th {
  background-color: #f9fafb;
  color: #555;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 1rem;
}

td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  color: #444;
}

tbody tr:last-child td {
  border-bottom: none;
}

tbody tr:nth-child(even) {
  background-color: #fdfdfd;
}

tbody tr:hover {
  background-color: #f5f5f5;
}

.rank {
  font-weight: bold;
  color: #4a90e2;
  font-size: 1.1rem;
  width: 15%;
}

.user-name {
  font-weight: 500;
}

.review-count {
  font-weight: bold;
  text-align: center;
  width: 20%;
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: #888;
}
</style>
