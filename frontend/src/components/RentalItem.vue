<template>
  <div class="rental-item">
    <h3>{{ rental.asset_name }}</h3>
    <p>Статус: {{ rental.status }}</p>
    <p>Початок: {{ formatDate(rental.start_date) }}</p>
    <p>Кінець: {{ formatDate(rental.end_date) }}</p>
    <p>Сума: {{ rental.total_cost }}₴</p>
    <button
      v-if="rental.status === 'Активний'"
      class="btn btn--danger"
      @click="$emit('cancel', rental.id)"
    >
      Скасувати оренду
    </button>
  </div>
</template>

<script>
export default {
  name: 'RentalItem',
  props: {
    rental: {
      type: Object,
      required: true,
    },
  },
  methods: {
    formatDate(dateStr) {
      if (!dateStr) return '—';
      const date = new Date(dateStr);
      return date.toLocaleDateString('uk-UA');
    },
  },
};
</script>

<style scoped>
.rental-item {
  padding: 1rem;
  border-radius: var(--radius-md);
  background: var(--gray-50);
  margin-bottom: 1rem;
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.3s ease;
}

.rental-item:hover {
  box-shadow: var(--shadow-md);
}

.rental-item h3 {
  margin-top: 0;
  color: var(--gray-900);
}

.rental-item p {
  margin: 5px 0;
  color: var(--gray-600);
}

.btn--danger {
  background-color: #dc3545;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn--danger:hover {
  background-color: #c82333;
}
</style>
