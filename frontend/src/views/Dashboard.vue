<template>
  <div class="dashboard">
    <div class="container">
      <div v-if="user" class="welcome">
        <h1 class="welcome__title">Вітаємо, {{ user.username }}! 👋</h1>
        <p class="welcome__subtitle">Ось ваш огляд активності</p>
      </div>
      <div v-else class="welcome">
        <h1 class="welcome__title">Завантаження...</h1>
      </div>

      <div v-if="user" class="stats">
        <StatCard icon="🚗" title="Активні оренди" :value="activeRentalsCount" />
        <StatCard icon="💰" title="Витрати за місяць" :value="monthlyExpenses + ' ₴'" />
        <StatCard icon="🎯" title="Завершені оренди" :value="completedRentalsCount" />
      </div>

      <div v-if="user" class="grid">
        <!-- Активні оренди -->
        <div class="card">
          <div class="card__header">
            <h2 class="card__title">Активні оренди</h2>
            <router-link to="/rentals" class="btn btn--outlined">Усі оренди</router-link>
          </div>
          <div v-if="activeRentals.length > 0">
            <RentalItem
              v-for="rental in activeRentals"
              :key="rental.id"
              :rental="rental"
              @cancel="cancelRental"
            />
          </div>
          <div v-else class="no-data">
            У вас поки немає активних оренд.
          </div>
        </div>

        <div class="card">
          <div class="card__header">
            <h2 class="card__title">Доступний транспорт</h2>
            <router-link to="/assets" class="btn btn--outlined">Переглянути все</router-link>
          </div>
          <div class="filter-group">
            <button
              class="filter-btn"
              :class="{ active: currentCategory === 'all' }"
              @click="filterCategory('all')"
            >
              Усі
            </button>
            <button
              v-for="type in assetTypes"
              :key="type"
              class="filter-btn"
              :class="{ active: currentCategory === type }"
              @click="filterCategory(type)"
            >
              {{ type }}
            </button>
          </div>

          <div v-if="filteredAssets.length > 0">
            <div v-for="asset in filteredAssets" :key="asset.id" class="rental-item">
              <div class="rental-item__header">
                <h3 class="rental-item__title">{{ asset.name }}</h3>
                <span class="rental-item__status">{{ asset.status }}</span>
              </div>
              <router-link :to="`/rentals/create/${asset.id}`" class="btn btn--success">
                Орендувати
              </router-link>
            </div>
          </div>
          <div v-else class="no-data">
            Немає доступних оренд.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios';
import StatCard from '../components/StatCard.vue';
import RentalItem from '../components/RentalItem.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'Dashboard',
  components: { StatCard, RentalItem },
  computed: {
    ...mapGetters(['user']),
    activeRentalsCount() {
      return this.activeRentals.length;
    },
    monthlyExpenses() {
      return this.activeRentals.reduce((acc, rental) => acc + rental.total_cost, 0);
    },
    completedRentalsCount() {
      return this.activeRentals.filter(rental => rental.status === 'Завершена').length;
    },
    filteredAssets() {
      if (this.currentCategory === 'all') return this.availableAssets;
      return this.availableAssets.filter(asset => asset.type === this.currentCategory);
    },
  },
  data() {
    return {
      activeRentals: [],
      availableAssets: [],
      currentCategory: 'all',
      assetTypes: ['Автомобілі', 'Електросамокати', 'Велосипеди'],
      errorMessage: '',
    };
  },
  methods: {
    async fetchDashboardData() {
      try {
        const response = await axios.get('/dashboard/');
        if (response.status === 200) {
          const data = response.data;
          this.activeRentals = data.active_rentals;
          this.availableAssets = data.available_assets;
          console.log('Dashboard data fetched:', data);
        }
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        if (error.response && error.response.status === 401) {
          this.$router.push('/login');
        } else {
          alert('Не вдалося завантажити дані дешборду. Спробуйте пізніше.');
        }
      }
    },
    filterCategory(category) {
      this.currentCategory = category;
    },
    async cancelRental(rentalId) {
      if (!confirm('Ви впевнені, що хочете скасувати цю оренду?')) return;
      try {
        await axios.post(`/rentals/${rentalId}/cancel`, {});
        this.fetchDashboardData();
        alert('Оренда скасована успішно!');
      } catch (error) {
        console.error('Error cancelling rental:', error);
        if (error.response && error.response.data && error.response.data.msg) {
          alert(`Помилка: ${error.response.data.msg}`);
        } else {
          alert('Не вдалося скасувати оренду.');
        }
      }
    },
  },
  created() {
    this.fetchDashboardData();
  },
};
</script>

<style scoped>
.dashboard {
  padding: 5rem 0 2rem;
}

.welcome {
  padding: 2rem;
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  margin-bottom: 1.5rem;
  color: var(--white);
}

.welcome__title {
  font-size: 1.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.welcome__subtitle {
  opacity: 0.9;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.grid {
  display: grid;
  gap: 1.5rem;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.card {
  position: relative;
  padding: 1rem;
  background: var(--gray-100);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
}

.card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.card__title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--gray-900);
}

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

.rental-item__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.rental-item__title {
  font-weight: 600;
}

.rental-item__status {
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  background: var(--success-color);
  color: var(--white);
}

.rental-item__status--canceled {
  background: var(--danger-color);
}

.no-data {
  text-align: center;
  color: var(--gray-500);
  padding: 2rem 0;
  font-size: 1.2rem;
}

.filter-group {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: var(--radius-sm);
  background: var(--gray-200);
  cursor: pointer;
  transition: background 0.3s;
}

.filter-btn.active,
.filter-btn:hover {
  background: var(--primary-color);
  color: var(--white);
}

.btn--outlined {
  border: 1px solid var(--primary-color);
  background: transparent;
  color: var(--primary-color);
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background 0.3s, color 0.3s;
}

.btn--outlined:hover {
  background: var(--primary-color);
  color: var(--white);
}

.btn--success {
  background-color: #28a745;
  color: #fff;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn--success:hover {
  background-color: #218838;
}
</style>
