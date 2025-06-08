import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import vue3GoogleLogin from "vue3-google-login";

const app = createApp(App);

app.use(router);

// Initialize the vue3-google-login plugin
// Replace with your actual Google Client ID
app.use(vue3GoogleLogin, {
  clientId:
    "966096773005-27b9q2i13lea2m5s3i8nemvj4qtanuie.apps.googleusercontent.com",
});

app.mount("#app");
