<template>
  <div class="hero">
    <div class="container hero__container">
      <div class="hero__content">
        <h1 class="hero__title">
          Ефективна система
          <span class="highlight">управління орендою</span>
        </h1>
        <p class="hero__description">
          Зручний облік об'єктів оренди, контроль статусів, історія операцій
          та фінансова аналітика в одному місці.
        </p>
        <div class="hero__cta">
          <router-link to="/registration" class="btn btn--primary btn--lg">Створити акаунт</router-link>
          <router-link to="/features" class="btn btn--secondary">Дізнатися більше</router-link>
        </div>
        <div class="hero__stats">
          <div class="stat-item">
            <span class="stat-item__number">1000+</span>
            <span class="stat-item__label">Активних об'єктів</span>
          </div>
          <div class="stat-item">
            <span class="stat-item__number">500+</span>
            <span class="stat-item__label">Користувачів</span>
          </div>
          <div class="stat-item">
            <span class="stat-item__number">2000+</span>
            <span class="stat-item__label">Орендних записів</span>
          </div>
        </div>
      </div>
      <div class="hero__image">
        <div class="floating-cards">
          <div class="float-card float-card--1">
            <div class="float-card__icon">👤</div>
            <div class="float-card__text">Особистий кабінет</div>
          </div>
          <div class="float-card float-card--2">
            <div class="float-card__icon">📊</div>
            <div class="float-card__text">Фінансовий підсумок</div>
          </div>
          <div class="float-card float-card--3">
            <div class="float-card__icon">📝</div>
            <div class="float-card__text">Облік об'єктів</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
};
</script>

<style scoped>
.hero {
    padding: 8rem 0 5rem;
    background: linear-gradient(135deg, var(--gray-50), var(--white));
    position: relative;
    overflow: hidden;
}

.hero__container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
}

.hero__content {
    animation: slideIn 1s ease-out;
}

.hero__title {
    font-size: 3rem;
    line-height: 1.2;
    margin-bottom: 1.5rem;
    color: var(--primary-color);
}

.hero__description {
    font-size: 1.25rem;
    color: var(--gray-600);
    margin-bottom: 2.5rem;
    max-width: 540px;
}

.hero__cta {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
}

.hero__stats {
    display: flex;
    gap: 3rem;
    margin-top: 3rem;
    flex-wrap: wrap;
}

.stat-item {
    background: var(--gray-100);
    padding: 1rem 2rem;
    border-radius: var(--radius-md);
    box-shadow: var(--shadow-sm);
    text-align: center;
}

.stat-item__number {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.stat-item__label {
    color: var(--gray-600);
    text-transform: uppercase;
    font-size: 0.875rem;
}

.hero__image {
    position: relative;
    height: 300px;
}

.floating-cards {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.float-card {
    position: absolute;
    background: var(--primary-color);
    padding: 0.5rem 1rem;
    border-radius: var(--radius-md);
    color: var(--white);
    display: flex;
    align-items: center;
    gap: 0.5rem;
    animation: float 3s ease-in-out infinite;
}

.float-card--1 {
    top: 10%;
    left: 20%;
    animation-delay: 0s;
}

.float-card--2 {
    top: 50%;
    left: 70%;
    animation-delay: 1s;
}

.float-card--3 {
    bottom: 10%;
    left: 40%;
    animation-delay: 2s;
}

.float-card__icon {
    font-size: 1.5rem;
}

.float-card__text {
    font-size: 1rem;
    font-weight: 500;
}

/* Анімації */
@keyframes float {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-20px);
    }
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-50px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@media (max-width: 768px) {
    .hero__container {
        grid-template-columns: 1fr;
        text-align: center;
    }

    .hero__stats {
        justify-content: center;
    }

    .hero__image {
        display: none;
    }
}
</style>
