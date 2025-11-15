<template>
  <div class="stat-card">
    <div class="stat-card__icon">{{ icon }}</div>
    <div class="stat-card__details">
      <h3 class="stat-card__title">{{ title }}</h3>
      <p class="stat-card__value">{{ value }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatCard',
  props: {
    icon: {
      type: String,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    value: {
      type: [String, Number],
      required: true,
    },
  },
};
</script>

<style scoped>
.stat-card {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: var(--gray-100);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.stat-card__icon {
  font-size: 2rem;
  margin-right: 1rem;
}

.stat-card__details {
  display: flex;
  flex-direction: column;
}

.stat-card__title {
  font-size: 1rem;
  color: var(--gray-700);
}

.stat-card__value {
  font-size: 1.25rem;
  font-weight: bold;
  color: var(--gray-900);
}
</style>
