<template>
  <div class="financial-summary">
    <div class="container">
      <h2 class="section-title">Фінансовий підсумок</h2>
      <form @submit.prevent="createSummary">
        <div class="form-group">
          <label for="period_start">Початкова дата</label>
          <input type="date" id="period_start" v-model="periodStart" required class="form-control" />
        </div>
        <div class="form-group">
          <label for="period_end">Кінцева дата</label>
          <input type="date" id="period_end" v-model="periodEnd" required class="form-control" />
        </div>
        <div class="form-group">
          <label for="total_rentals">Загальна кількість оренд</label>
          <input type="number" id="total_rentals" v-model="totalRentals" required class="form-control" min="0" />
        </div>
        <div class="form-group">
          <label for="total_cost">Загальна сума витрат (₴)</label>
          <input type="number" id="total_cost" v-model="totalCost" required class="form-control" min="0" step="0.01" />
        </div>
        <button type="submit" class="btn btn--primary">Створити підсумок</button>
      </form>
      <div v-if="errorMessage" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="alert alert-success mt-3">
        {{ successMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  name: 'FinancialSummary',
  data() {
    return {
      periodStart: '',
      periodEnd: '',
      totalRentals: 0,
      totalCost: 0,
      errorMessage: '',
      successMessage: '',
    };
  },
  methods: {
    async createSummary() {
      try {
        const token = localStorage.getItem('access_token');
        const payload = {
          period_start: this.periodStart,
          period_end: this.periodEnd,
          total_rentals: this.totalRentals,
          total_cost: this.totalCost,
        };
        const response = await axios.post('/financial_summary/', payload, { // Заміна маршруту
          headers: { Authorization: `Bearer ${token}` },
        });
        if (response.status === 201) {
          this.errorMessage = '';
          this.successMessage = 'Фінансовий підсумок створено успішно!';
          this.periodStart = '';
          this.periodEnd = '';
          this.totalRentals = 0;
          this.totalCost = 0;
        }
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.msg) {
          this.errorMessage = error.response.data.msg;
        } else {
          this.errorMessage = 'Не вдалося створити фінансовий підсумок.';
        }
        this.successMessage = '';
      }
    },
  },
};
</script>

<style scoped>
.financial-summary {
    padding: 5rem 0;
}

.financial-summary form {
    max-width: 500px;
    margin: 0 auto;
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

.alert-success {
    color: #155724;
    background-color: #d4edda;
    border-color: #c3e6cb;
}
</style>
