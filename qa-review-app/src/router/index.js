import { createRouter, createWebHistory } from "vue-router";
import Review from "../views/ReviewQa.vue";
import Leaderboard from "../views/LeaderboardScore.vue";

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
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
