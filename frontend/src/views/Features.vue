<template>
  <div id="features" class="features">
    <div class="container">
      <h2 class="section-title">Основні можливості</h2>
      <div class="features-grid">
        <div class="feature-card" v-for="feature in features" :key="feature.id">
          <div class="feature-card__icon">{{ feature.icon }}</div>
          <h3 class="feature-card__title">{{ feature.title }}</h3>
          <p class="feature-card__text">{{ feature.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Features',
  data() {
    return {
      features: [
        {
          id: 1,
          icon: '🔐',
          title: 'Авторизація',
          description: 'Безпечна реєстрація та вхід через логін і пароль. Надійне зберігання даних користувачів.',
        },
        {
          id: 2,
          icon: '📦',
          title: 'Облік об\'єктів',
          description: 'Контроль статусів об\'єктів: доступно, зайнято, на обслуговуванні. Повна історія використання.',
        },
        {
          id: 3,
          icon: '👤',
          title: 'Особистий кабінет',
          description: 'Управління особистими даними, перегляд історії та активних оренд. Редагування контактної інформації.',
        },
        {
          id: 4,
          icon: '💰',
          title: 'Фінансовий облік',
          description: 'Підрахунок загальної вартості оренд за період. Аналіз витрат за місяць або рік.',
        },
      ],
    };
  },
};
</script>

<style scoped>
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
}

.feature-card {
    background: var(--white);
    padding: 2rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.feature-card__icon {
    font-size: 3rem;
    margin-bottom: 1.5rem;
    color: var(--primary-color);
}

.feature-card__title {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: var(--gray-900);
}

.feature-card__text {
    font-size: 1rem;
    color: var(--gray-600);
}
</style>
