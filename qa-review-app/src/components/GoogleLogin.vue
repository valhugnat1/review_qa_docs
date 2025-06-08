<template>
  <div id="google-login-button"></div>
</template>

<script>
import { googleSdkLoaded, decodeCredential } from "vue3-google-login";

export default {
  name: "GoogleLogin",
  mounted() {
    // We wait for the Google SDK to be fully loaded before doing anything.
    googleSdkLoaded((google) => {
      // Initialize the Google Identity Services library.
      google.accounts.id.initialize({
        client_id:
          "966096773005-27b9q2i13lea2m5s3i8nemvj4qtanuie.apps.googleusercontent.com", // IMPORTANT: Replace with your actual Client ID
        callback: this.handleCredentialResponse, // The function to call on successful login
      });

      // Manually render the Google One Tap button in our target div.
      google.accounts.id.renderButton(
        document.getElementById("google-login-button"),
        { theme: "outline", size: "large" } // Customize the button appearance
      );

      // Optional: If you want the One Tap prompt, you can uncomment the next line
      // google.accounts.id.prompt();
    });
  },
  methods: {
    handleCredentialResponse(response) {
      // This function is called by the Google SDK, not by a Vue event.
      const userData = decodeCredential(response.credential);
      console.log("Logged in user:", userData);
      // Emit the user's name up to the parent App.vue.
      this.$emit("loggedIn", userData.name);
    },
  },
};
</script>
