<template>
  <div class="review-card">
    <QaDisplay
      :formatted-question="formattedQuestion"
      :formatted-answer="formattedAnswer"
      :mode="mode"
      @set-mode="setMode"
      @pass-question="$emit('pass-question')"
    />

    <EditPanel
      v-if="mode === 'edit'"
      :initial-pair="pair"
      @submit-edit="handleEditSubmission"
      @cancel-edit="setMode('view')"
    />

    <RatePanel
      v-else-if="mode === 'rate'"
      @submit-review="handleRateSubmission"
      @cancel-rate="setMode('view')"
    />
  </div>
</template>

<script>
import { marked } from "marked";
import hljs from "highlight.js";
import QaDisplay from "./QaDisplay.vue";
import EditPanel from "./EditPanel.vue";
import RatePanel from "./RatePanel.vue";

export default {
  name: "ReviewCard",
  components: { QaDisplay, EditPanel, RatePanel },
  props: {
    pair: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      mode: "view", // 'view', 'edit', 'rate'
    };
  },
  created() {
    this.configureMarked();
  },
  computed: {
    formattedQuestion() {
      return this.pair.question ? marked(this.pair.question) : "";
    },
    formattedAnswer() {
      return this.pair.answer ? marked(this.pair.answer) : "";
    },
  },
  methods: {
    configureMarked() {
      marked.setOptions({
        highlight: function (code, lang) {
          const language = hljs.getLanguage(lang) ? lang : "plaintext";
          return hljs.highlight(code, { language }).value;
        },
        langPrefix: "hljs language-",
        gfm: true,
        breaks: true,
      });
    },
    setMode(newMode) {
      this.mode = newMode;
    },
    // Handles submission from the EditPanel
    handleEditSubmission(editedPair) {
      this.$emit("submit-review", {
        question: editedPair.question,
        answer: editedPair.answer,
        question_rating: 3,
        answer_rating: 3,
        comment: "Content Edited",
      });
      // ***** CHANGE: Explicitly set mode back to 'view' to hide the panel *****
      this.setMode("view");
    },
    // Handles submission from the RatePanel
    handleRateSubmission(ratingData) {
      this.$emit("submit-review", {
        ...ratingData,
        question: this.pair.question,
        answer: this.pair.answer,
      });
      // ***** CHANGE: Explicitly set mode back to 'view' to hide the panel *****
      this.setMode("view");
    },
  },
};
</script>

<style scoped>
.review-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  padding: 2rem 2.5rem;
  max-width: 800px;
  width: 100%;
}
</style>
