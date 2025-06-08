<template>
  <div id="app">
    <header>
      <div class="auth-section">
        <GoogleLogin v-if="!isLoggedIn" @logged-in="handleLogin" />
        <div v-else class="user-info">
          <span>Welcome, {{ userName }}</span>
          <button @click="handleLogout">Logout</button>
        </div>
      </div>

      <nav>
        <router-link to="/">Q&A Review</router-link> |
        <router-link to="/leaderboard">Leaderboard</router-link>
      </nav>
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
    },
  },
};
</script>

<style>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f0f0f0;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.user-info span {
  font-weight: bold;
}
</style>
