import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import vue3GoogleLogin from "vue3-google-login";
// e.g., in your main.js
import "highlight.js/styles/atom-one-dark.css"; // Using a different theme for this example

const app = createApp(App);

app.use(router);

// Initialize the vue3-google-login plugin
// Replace with your actual Google Client ID
app.use(vue3GoogleLogin, {
  clientId:
    "966096773005-27b9q2i13lea2m5s3i8nemvj4qtanuie.apps.googleusercontent.com",
});

app.mount("#app");
