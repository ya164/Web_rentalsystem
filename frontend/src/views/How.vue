<template>
  <div id="how" class="how">
    <div class="container">
      <h2 class="section-title">Як користуватись системою</h2>
      <div class="steps">
        <div class="step" v-for="step in steps" :key="step.number">
          <div class="step__number">{{ step.number }}</div>
          <h3 class="step__title">{{ step.title }}</h3>
          <p class="step__text">{{ step.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'How',
  data() {
    return {
      steps: [
        {
          number: 1,
          title: 'Реєстрація',
          description: 'Створіть обліковий запис, заповнивши необхідні поля на сторінці реєстрації.',
        },
        {
          number: 2,
          title: 'Вибір об\'єкта',
          description: 'Перейдіть до розділу "Доступний транспорт" та оберіть об\'єкт для оренди.',
        },
        {
          number: 3,
          title: 'Створення оренди',
          description: 'Натисніть кнопку "Орендувати" поруч із обраним об\'єктом та заповніть необхідні дані.',
        },
        {
          number: 4,
          title: 'Контроль статусу',
          description: 'Переглядайте статус вашої оренди на панелі приладів та здійснюйте необхідні дії.',
        },
      ],
    };
  },
};
</script>

<style scoped>
.steps {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 3rem;
    margin-top: 3rem;
}

.step {
    text-align: center;
    background: var(--white);
    padding: 2rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.step:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.step__number {
    width: 4rem;
    height: 4rem;
    background: var(--primary-color);
    color: var(--white);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 700;
    margin: 0 auto 1.5rem;
}

.step__title {
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
    color: var(--gray-900);
}

.step__text {
    font-size: 1rem;
    color: var(--gray-600);
}
</style>
