<template>
  <footer class="footer">
    <div class="container">
      <div class="footer__content">
        <div class="footer__brand">
          <router-link to="/" class="logo logo--white">
            <span class="logo__icon">📦</span>
            <span class="logo__text">RentalSystem</span>
          </router-link>
          <p class="footer__description">
            Система для ефективного управління орендою об'єктів
          </p>
        </div>

        <div class="footer__links">
          <div class="footer__column">
            <h4 class="footer__title">Навігація</h4>
            <ul class="footer__list">
              <li><router-link to="/features">Можливості</router-link></li>
              <li><router-link to="/how">Інструкції</router-link></li>
            </ul>
          </div>
          <div class="footer__column">
            <h4 class="footer__title">Підтримка</h4>
            <ul class="footer__list">
              <li><router-link to="/faq">FAQ</router-link></li>
            </ul>
          </div>
          <div class="footer__column">
            <h4 class="footer__title">Контакти</h4>
            <ul class="footer__list">
              <li>📧 yardid@ukr.net</li>
              <li>📞 +38(093)590-69-96</li>
              <li>📍 м. Київ, вул. Христини Сушко, 49</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="footer__bottom">
        <div class="footer__copy">
          © 2024 RentalSystem. Всі права захищено
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter',
};
</script>

<style scoped>
.footer {
    background: var(--gray-800);
    color: var(--white);
    padding: 4rem 0;
}

.footer__content {
    display: flex;
    justify-content: space-between;
    gap: 2rem;
    flex-wrap: wrap;
}

.footer__brand {
    flex: 1;
    min-width: 200px;
}

.footer__brand .logo {
    text-decoration: none;
    display: flex;
    align-items: center;
    color: var(--white);
    font-weight: 700;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.footer__description {
    color: var(--gray-400);
    font-size: 0.875rem;
    max-width: 300px;
}

.footer__links {
    display: flex;
    gap: 2rem;
    flex: 2;
    justify-content: space-between;
    flex-wrap: wrap;
}

.footer__column {
    min-width: 150px;
}

.footer__title {
    font-size: 1.125rem;
    margin-bottom: 1rem;
    color: var(--white);
}

.footer__list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer__list li {
    margin-bottom: 0.5rem;
}

.footer__list a {
    color: var(--gray-400);
    text-decoration: none;
    font-size: 0.875rem;
    transition: color 0.3s ease;
}

.footer__list a:hover {
    color: var(--primary-color);
}

.footer__bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 1rem;
    margin-top: 2rem;
    flex-wrap: wrap;
    gap: 1rem;
}

.footer__copy {
    font-size: 0.875rem;
    color: var(--gray-400);
}

.footer__social {
    display: flex;
    gap: 1rem;
}

.social-link {
    color: var(--gray-400);
    text-decoration: none;
    font-size: 1rem;
    transition: color 0.3s ease;
}

.social-link:hover {
    color: var(--primary-color);
}
</style>
