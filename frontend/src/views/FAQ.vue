<template>
  <div id="faq" class="faq">
    <div class="container">
      <h2 class="section-title">Часті питання</h2>
      <div class="faq-list">
        <div class="faq-item" v-for="faq in faqs" :key="faq.id">
          <h4 class="faq-item__question">{{ faq.question }}</h4>
          <p class="faq-item__answer">{{ faq.answer }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FAQ',
  data() {
    return {
      faqs: [
        {
          id: 1,
          question: 'Як створити акаунт?',
          answer: 'Перейдіть на сторінку реєстрації та заповніть всі необхідні поля.',
        },
        {
          id: 2,
          question: 'Як орендувати об\'єкт?',
          answer: 'Виберіть доступний об\'єкт на панелі керування та натисніть кнопку "Орендувати".',
        },
        {
          id: 3,
          question: 'Як скасувати оренду?',
          answer: 'Перейдіть на сторінку "Ваші оренди" та натисніть кнопку "Скасувати" поруч із відповідною орендою.',
        },
      ],
    };
  },
};
</script>

<style scoped>
.faq-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
}

.faq-item {
    background: var(--white);
    padding: 2rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-md);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.faq-item:hover {
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

.faq-item__question {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.75rem;
    color: var(--primary-color);
}

.faq-item__answer {
    color: var(--gray-600);
    line-height: 1.6;
}
</style>
