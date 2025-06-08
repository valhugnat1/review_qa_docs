import { createRouter, createWebHistory } from "vue-router";
import Review from "../views/ReviewQa.vue";
import Leaderboard from "../views/LeaderboardScore.vue";
import CategoryStats from "../views/CategoryStats.vue";

const routes = [
  {
    path: "/",
    name: "ReviewQa",
    component: Review,
  },
  {
    path: "/leaderboard",
    name: "LeaderboardScore",
    component: Leaderboard,
  },
  {
    path: "/category-stats", // <-- Add the new route
    name: "CategoryStats",
    component: CategoryStats,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
