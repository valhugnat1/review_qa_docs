<template>
  <div>
    <div class="qa-content">
      <div class="qa-section">
        <h2 class="question-title">Question</h2>
        <div class="content-display" v-html="formattedQuestion"></div>
      </div>
      <div class="qa-section">
        <h2 class="answer-title">Answer</h2>
        <div class="content-display" v-html="formattedAnswer"></div>
      </div>
    </div>

    <div v-if="mode === 'view'" class="actions-panel">
      <div class="view-actions">
        <button @click="$emit('set-mode', 'rate')" class="action-button">
          Rate
        </button>
        <button
          @click="$emit('set-mode', 'edit')"
          class="action-button secondary"
        >
          Edit
        </button>
        <button
          @click="$emit('pass-question')"
          class="action-button pass-button"
        >
          Pass
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QaDisplay",
  props: {
    formattedQuestion: String,
    formattedAnswer: String,
    mode: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
/* Styles remain the same */
.qa-content {
}
.qa-section {
  margin-bottom: 1.5rem;
}
.question-title,
.answer-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
  border-bottom: 2px solid #eee;
  padding-bottom: 0.5rem;
}
.content-display {
  line-height: 1.7;
  color: #333;
}
.content-display :deep(p) {
  margin-bottom: 1em;
}
.content-display :deep(pre) {
  background-color: #282c34;
  color: #abb2bf;
  border-radius: 8px;
  padding: 1rem;
  overflow-x: auto;
  font-family: "Fira Code", "Courier New", Courier, monospace;
}
.content-display :deep(code) {
  font-size: 0.95em;
}
.actions-panel {
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e9ecef;
}
.view-actions {
  display: flex;
  gap: 1rem;
}
.action-button {
  flex-grow: 1;
  padding: 0.9rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: white;
  background-color: #4a90e2;
}
.action-button:hover {
  background-color: #357abd;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
.action-button.secondary {
  background-color: #6c757d;
}
.action-button.secondary:hover {
  background-color: #5a6268;
}
.action-button.pass-button {
  background-color: #ef6c00;
}
.action-button.pass-button:hover {
  background-color: #e65100;
}
</style>
