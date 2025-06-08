<template>
  <div id="app">
    <header class="app-header">
      <div class="header-title">
        <router-link to="/">Q&A Insight</router-link>
      </div>

      <nav class="header-nav">
        <router-link to="/">Q&A Review</router-link>
        <router-link to="/leaderboard">Leaderboard</router-link>
        <router-link to="/category-stats">Category Stats</router-link>
      </nav>

      <div class="auth-section">
        <GoogleLogin v-if="!isLoggedIn" @logged-in="handleLogin" />
        <div v-else class="user-info">
          <span class="welcome-message">Welcome, {{ userName }}</span>
          <button @click="handleLogout" class="logout-button">Logout</button>
        </div>
      </div>
    </header>
    <main>
      <router-view :user="userName"></router-view>
    </main>
  </div>
</template>

<script>
import GoogleLogin from "./components/GoogleLogin.vue";

export default {
  name: "App",
  components: {
    GoogleLogin,
  },
  data() {
    return {
      userName: "",
      isLoggedIn: false,
    };
  },
  created() {
    const storedUserName = localStorage.getItem("userName");
    if (storedUserName) {
      this.userName = storedUserName;
      this.isLoggedIn = true;
    }
  },
  methods: {
    handleLogin(userName) {
      this.userName = userName;
      this.isLoggedIn = true;
      localStorage.setItem("userName", userName);
    },
    handleLogout() {
      this.userName = "";
      this.isLoggedIn = false;
      localStorage.removeItem("userName");
      // Redirect to home page on logout to prevent access to protected routes
      if (this.$route.path !== "/") {
        this.$router.push("/");
      }
    },
  },
};
</script>

<style>
/* --- Global Styles --- */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
    "Helvetica Neue", Arial, sans-serif;
  background-color: #f7f9fc; /* Match the page container background */
}

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

main {
  /* The router-view content will appear here */
}

/* --- Improved Header Styles --- */
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem; /* Vertical padding is 0, horizontal is 2rem */
  height: 64px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 100;
}

/* --- Title / Logo --- */
.header-title {
  font-size: 1.5rem;
  font-weight: 600;
}
.header-title a {
  text-decoration: none;
  color: #333;
}

/* --- Navigation --- */
.header-nav {
  display: flex;
  gap: 1.5rem;
}

.header-nav a {
  text-decoration: none;
  color: #555;
  font-weight: 500;
  font-size: 1rem;
  padding: 20px 4px; /* Increased padding for a larger click area */
  border-bottom: 3px solid transparent;
  transition: color 0.2s, border-bottom-color 0.2s;
}

.header-nav a:hover {
  color: #4a90e2; /* Use theme color on hover */
}

/* Style for the active page link */
.header-nav a.router-link-exact-active {
  color: #4a90e2;
  border-bottom-color: #4a90e2;
}

/* --- Auth Section --- */
.auth-section {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.welcome-message {
  font-weight: 500;
  color: #333;
}

.logout-button {
  background-color: #f1f1f1;
  color: #555;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s, box-shadow 0.2s;
}

.logout-button:hover {
  background-color: #e9e9e9;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>
