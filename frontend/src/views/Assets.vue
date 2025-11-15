<template>
  <div class="assets">
    <div class="container">
      <h2 class="section-title">Доступний транспорт</h2>
      <div class="filter-group">
        <button
          class="filter-btn"
          :class="{ active: currentFilter === 'all' }"
          @click="setFilter('all')"
        >
          Усі
        </button>
        <button
          v-for="type in assetTypes"
          :key="type"
          class="filter-btn"
          :class="{ active: currentFilter === type }"
          @click="setFilter(type)"
        >
          {{ type }}
        </button>
      </div>

      <div v-if="filteredAssets.length > 0" class="assets-list">
        <div
          v-for="asset in filteredAssets"
          :key="asset.id"
          class="asset-item card"
        >
          <h3>{{ asset.name }}</h3>
          <p>Тип: {{ asset.type }}</p>
          <p>Ціна за день: {{ asset.price_per_day }}₴</p>
          <p>Статус: {{ asset.status }}</p>
          <router-link
            :to="`/rentals/create/${asset.id}`"
            class="btn btn--success"
          >
            Орендувати
          </router-link>
        </div>
      </div>
      <div v-else class="no-data">
        Немає доступних оренд.
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
  name: 'Assets',
  data() {
    return {
      assets: [],
      currentFilter: 'all',
      assetTypes: ['Автомобілі', 'Електросамокати', 'Велосипеди'],
      errorMessage: '',
    };
  },
  computed: {
    filteredAssets() {
      if (this.currentFilter === 'all') return this.assets;
      return this.assets.filter(asset => asset.type === this.currentFilter);
    },
  },
  methods: {
    async fetchAssets() {
      try {
        const response = await axios.get('/objects/');
        if (response.status === 200) {
          this.assets = response.data;
        }
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Не вдалося завантажити об\'єкти оренди.';
      }
    },
    setFilter(filter) {
      this.currentFilter = filter;
    },
  },
  created() {
    this.fetchAssets();
  },
};
</script>

<style scoped>
.assets {
    padding: 5rem 0;
}

.filter-group {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.filter-btn {
    padding: 0.5rem 1rem;
    border-radius: var(--radius-md);
    font-size: 0.875rem;
    border: 2px solid var(--primary-color);
    background: transparent;
    color: var(--primary-color);
    cursor: pointer;
    transition: background-color 0.3s ease, color 0.3s ease;
}

.filter-btn.active {
    background: var(--primary-color);
    color: var(--white);
}

.filter-btn:hover {
    background: var(--primary-dark);
    color: var(--white);
}

.assets-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.asset-item h3 {
    margin-top: 0;
}

.asset-item p {
    margin: 5px 0;
}

.asset-item .btn {
    margin-top: 10px;
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
