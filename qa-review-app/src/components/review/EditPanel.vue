<template>
  <div class="edit-panel">
    <h3 class="panel-title">Edit Q&A</h3>
    <div class="qa-section">
      <label class="text-field-label">Edit Question</label>
      <textarea v-model="editablePair.question" class="text-field"></textarea>
    </div>
    <div class="qa-section">
      <label class="text-field-label">Edit Answer</label>
      <textarea
        v-model="editablePair.answer"
        class="text-field answer-field"
      ></textarea>
    </div>
    <div class="panel-actions">
      <button @click="$emit('submit-edit', editablePair)" class="submit-button">
        Submit Changes
      </button>
      <button @click="$emit('cancel-edit')" class="cancel-button">
        Cancel
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "EditPanel",
  props: {
    initialPair: { type: Object, required: true },
  },
  data() {
    return {
      // Use a local copy to avoid directly mutating the prop
      editablePair: { ...this.initialPair },
    };
  },
};
</script>

<style scoped>
/* --- Edit Panel Styles --- */
.panel-title {
  font-size: 1.3rem;
  text-align: center;
  margin-bottom: 1.5rem;
  color: #444;
}
.qa-section {
  margin-bottom: 1.5rem;
}
.text-field-label {
  display: block;
  font-weight: 500;
  color: #555;
  margin-bottom: 0.5rem;
}
.text-field {
  width: 100%;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 0.75rem;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.text-field:focus {
  outline: none;
  border-color: #4a90e2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.2);
}
.answer-field {
  min-height: 200px;
}
.panel-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.submit-button,
.cancel-button {
  flex-grow: 1;
  padding: 0.9rem;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}
.submit-button {
  color: white;
  background-color: #4a90e2;
}
.submit-button:hover {
  background-color: #357abd;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
.cancel-button {
  background-color: #f1f1f1;
  color: #555;
  border: 1px solid #ddd;
}
.cancel-button:hover {
  background-color: #e9e9e9;
}
</style>
