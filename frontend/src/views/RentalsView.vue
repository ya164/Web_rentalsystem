<template>
  <div class="rentals">
    <div class="container">
      <h2 class="section-title">Ваші оренди</h2>
      <div v-if="rentals.length > 0" class="rentals-list">
        <div
          v-for="rental in rentals"
          :key="rental.id"
          class="rental-item card"
        >
          <h3>{{ rental.asset_name }}</h3>
          <p>Статус: {{ rental.status }}</p>
          <p>Початок: {{ formatDate(rental.start_date) }}</p>
          <p>Кінець: {{ formatDate(rental.end_date) }}</p>
          <p>Сума: {{ rental.total_cost }}₴</p>
          <button
            v-if="rental.status === 'Активний'"
            class="btn btn--danger"
            @click="cancelRental(rental.id)"
          >
            Скасувати оренду
          </button>
        </div>
      </div>
      <div v-else class="no-data">
        У вас поки немає оренд.
      </div>
      <div v-if="errorMessage" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  name: 'RentalsView',
  data() {
    return {
      rentals: [],
      errorMessage: '',
    };
  },
  methods: {
    async fetchRentals() {
      try {
        const response = await axios.get('/rentals/');
        if (response.status === 200) {
          this.rentals = response.data;
          console.log('Rentals fetched:', this.rentals);
        }
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Не вдалося завантажити оренди.';
      }
    },
    async cancelRental(rentalId) {
      if (!confirm('Ви впевнені, що хочете скасувати цю оренду?')) return;
      try {
        await axios.post(`/rentals/${rentalId}/cancel`, {});
        this.fetchRentals();
        alert('Оренда скасована успішно!');
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.msg) {
          this.errorMessage = `Помилка: ${error.response.data.msg}`;
        } else {
          this.errorMessage = 'Не вдалося скасувати оренду.';
        }
      }
    },
    formatDate(dateStr) {
      if (!dateStr) return '—';
      const date = new Date(dateStr);
      return date.toLocaleDateString('uk-UA');
    },
  },
  created() {
    this.fetchRentals();
  },
};
</script>

<style scoped>
.rentals {
  padding: 5rem 0;
}

.rentals-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.rental-item h3 {
  margin-top: 0;
  color: var(--gray-900);
}

.rental-item p {
  margin: 5px 0;
  color: var(--gray-600);
}

.rental-item .btn {
  margin-top: 10px;
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

.no-data {
  text-align: center;
  color: var(--gray-500);
  padding: 2rem 0;
  font-size: 1.2rem;
}

.alert {
    padding: 0.75rem 1.25rem;
    border: 1px solid transparent;
    border-radius: var(--radius-md);
    font-size: 0.875rem;
}

.alert-danger {
    color: #721c24;
    background-color: #f8d7da;
    border-color: #f5c6cb;
}
</style>
