<template>
  <div class="category-selector-card">
    <div class="panel-header">
      <h3 class="panel-title">Select Categories to Review</h3>
      <div class="bulk-actions">
        <button
          @click="selectAll"
          :disabled="availableCategories.length === 0"
          class="bulk-action-btn"
        >
          Select All
        </button>
        <button
          @click="unselectAll"
          :disabled="selectedCategories.length === 0"
          class="bulk-action-btn"
        >
          Unselect All
        </button>
      </div>
    </div>
    <div class="selector-content">
      <select
        @change="onAddCategory($event.target.value)"
        class="category-dropdown"
        :disabled="availableCategories.length === 0"
      >
        <option disabled selected value="">
          {{
            availableCategories.length > 0
              ? "-- Add a category --"
              : "-- All categories selected --"
          }}
        </option>
        <option v-for="cat in availableCategories" :key="cat" :value="cat">
          {{ cat }}
        </option>
      </select>
      <div class="selected-tags-container">
        <span
          v-for="(tag, index) in selectedCategories"
          :key="tag"
          class="category-tag"
        >
          {{ tag }}
          <button
            @click="$emit('remove-category', index)"
            class="remove-tag-btn"
            title="Remove category"
          >
            ×
          </button>
        </span>
        <span v-if="!selectedCategories.length" class="no-tags-placeholder">
          Select one or more categories to begin.
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CategorySelector",
  props: {
    categories: {
      type: Array,
      required: true,
    },
    selectedCategories: {
      type: Array,
      required: true,
    },
  },
  computed: {
    availableCategories() {
      // Returns categories that are not yet selected
      return this.categories.filter(
        (c) => !this.selectedCategories.includes(c)
      );
    },
  },
  methods: {
    onAddCategory(category) {
      this.$emit("add-category", category);
      // Reset dropdown after selection
      this.$el.querySelector(".category-dropdown").value = "";
    },
    selectAll() {
      this.$emit("select-all");
    },
    unselectAll() {
      this.$emit("unselect-all");
    },
  },
};
</script>

<style scoped>
/* --- Category Selector Styles --- */
.category-selector-card {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  padding: 1.5rem 2.5rem;
  max-width: 800px;
  width: 100%;
  margin-bottom: 2rem;
}
.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.panel-title {
  font-size: 1.3rem;
  color: #444;
  margin: 0;
}
.bulk-actions {
  display: flex;
  gap: 0.75rem;
}
.bulk-action-btn {
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 500;
  color: #555;
  transition: background-color 0.2s, color 0.2s;
}
.bulk-action-btn:hover:not(:disabled) {
  background-color: #e0e0e0;
}
.bulk-action-btn:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
.selector-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.category-dropdown {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  background-color: #fff;
  cursor: pointer;
}
.category-dropdown:disabled {
  background-color: #f8f8f8;
  cursor: not-allowed;
}
.selected-tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  padding: 0.5rem;
  min-height: 40px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  align-items: center;
}
.no-tags-placeholder {
  color: #999;
  padding-left: 0.5rem;
  font-style: italic;
}
.category-tag {
  display: inline-flex;
  align-items: center;
  background-color: #4a90e2;
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 16px;
  font-weight: 500;
  font-size: 0.9rem;
  animation: fadeIn 0.3s ease-in-out;
}
.remove-tag-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  font-weight: bold;
  margin-left: 0.5rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  opacity: 0.7;
  transition: opacity 0.2s;
}
.remove-tag-btn:hover {
  opacity: 1;
}
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
