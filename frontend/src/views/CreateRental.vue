<template>
  <div class="create-rental">
    <div class="container">
      <h2 class="section-title">Створити оренду</h2>
      <div v-if="asset">
        <h3>Транспорт: {{ asset.name }}</h3>
        <p>Ціна за день: {{ asset.price_per_day }}₴</p>
      </div>
      <div v-else-if="errorMessage && !isLoading" class="alert alert-danger">
        {{ errorMessage }}
      </div>
      <div v-else class="alert alert-info">
        Завантаження даних про транспорт...
      </div>
      <form v-if="asset" @submit.prevent="createRental">
        <div class="form-group">
          <label for="start_date">Дата початку</label>
          <input
            type="date"
            id="start_date"
            v-model="startDate"
            required
            class="form-control"
            :min="todayStr"
            @change="calculateCost"
          />
        </div>
        <div class="form-group">
          <label for="end_date">Дата закінчення</label>
          <input
            type="date"
            id="end_date"
            v-model="endDate"
            required
            class="form-control"
            :min="startDate || todayStr"
            @change="calculateCost"
          />
        </div>
        <div v-if="totalCost !== null" class="cost-summary">
          <p>Орієнтовна вартість: {{ totalCost }}₴</p>
        </div>
        <button type="submit" class="btn btn--primary" :disabled="totalCost === null">
          Орендувати
        </button>
      </form>
      <div v-if="asset && errorMessage && !isLoading" class="alert alert-danger mt-3">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  name: 'CreateRental',
  props: {
    asset_id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      startDate: '',
      endDate: '',
      totalCost: null,
      pricePerDay: null,
      errorMessage: '',
      asset: null,
      todayStr: this.formatDate(new Date()),
      isLoading: true,
    };
  },
  methods: {
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    async fetchAssetDetails() {
      try {
        const response = await axios.get(`/objects/${this.asset_id}`);
        if (response.status === 200) {
          this.asset = response.data;
          this.pricePerDay = parseFloat(response.data.price_per_day);
          console.log('Asset details fetched:', this.asset);
        }
      } catch (error) {
        console.error('Error fetching asset details:', error);
        this.errorMessage = 'Не вдалося завантажити дані про транспорт.';
      } finally {
        this.isLoading = false;
      }
    },
    calculateCost() {
      if (this.startDate && this.endDate && this.pricePerDay) {
        const start = new Date(this.startDate);
        const end = new Date(this.endDate);
        if (end > start) {
          const diffTime = end - start;
          const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
          this.totalCost = diffDays * this.pricePerDay;
          this.errorMessage = '';
        } else {
          this.totalCost = null;
          this.errorMessage = 'Дата закінчення повинна бути після дати початку.';
        }
      } else {
        this.totalCost = null;
        this.errorMessage = '';
      }
    },
    async createRental() {
      if (!this.startDate || !this.endDate || this.totalCost === null) {
        this.errorMessage = 'Будь ласка, оберіть дати оренди.';
        return;
      }

      try {
        const payload = {
          asset_id: this.asset_id,
          start_date: this.startDate,
          end_date: this.endDate,
        };
        const response = await axios.post('/rentals/', payload);
        if (response.status === 201) {
          alert('Оренда створена успішно!');
          this.$router.push('/dashboard');
        }
      } catch (error) {
        console.error(error);
        if (error.response && error.response.data && error.response.data.msg) {
          this.errorMessage = `Помилка: ${error.response.data.msg}`;
        } else {
          this.errorMessage = 'Не вдалося створити оренду.';
        }
      }
    },
  },
  created() {
    if (!this.asset_id) {
      this.errorMessage = 'Невідомий транспорт.';
      this.isLoading = false;
      return;
    }
    this.fetchAssetDetails();
  },
};
</script>

<style scoped>
.create-rental {
  padding: 5rem 0;
}

.container {
  max-width: 500px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1.5rem;
}

.cost-summary {
  margin-bottom: 1rem;
  font-size: 1.1rem;
  font-weight: bold;
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

.alert-info {
  color: #0c5460;
  background-color: #d1ecf1;
  border-color: #bee5eb;
}
</style>
