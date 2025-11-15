<template>
  <header class="header">
    <div class="container header__container">
      <router-link to="/" class="logo">
        <span class="logo__icon">📦</span>
        <span>RentalSystem</span>
      </router-link>
      <nav class="nav">
        <ul class="nav__list">
          <li class="nav__item"><router-link to="/features" class="nav__link">Можливості</router-link></li>
          <li class="nav__item"><router-link to="/how" class="nav__link">Як користуватись</router-link></li>
          <li class="nav__item"><router-link to="/faq" class="nav__link">FAQ</router-link></li>
        </ul>
      </nav>
      <div class="auth-buttons">
        <template v-if="isAuthenticated">
          <router-link v-if="isAdmin" to="/admin" class="btn btn--secondary">Адмін Панель</router-link>
          <router-link v-else to="/dashboard" class="btn btn--secondary">Кабінет користувача</router-link>
          <button class="btn btn--danger" @click="handleLogout">Вийти</button>
        </template>
        <template v-else>
          <router-link to="/login" class="btn btn--outlined">Увійти</router-link>
          <router-link to="/registration" class="btn btn--primary">Реєстрація</router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  name: 'AppHeader',
  computed: {
    ...mapGetters(['isAuthenticated', 'user']),
    isAdmin() {
      return this.user && this.user.is_admin;
    },
  },
  methods: {
    ...mapActions(['logout']),
    async handleLogout() {
      await this.logout();
      this.$router.push('/');
    },
  },
};
</script>

<style scoped>
.header {
  position: fixed;
  width: 100%;
  top: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: var(--shadow-sm);
  z-index: 1000;
  padding: 1rem 0;
}

.header__container {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--gray-900);
  font-weight: 700;
  font-size: 1.5rem;
  gap: 0.5rem;
  transition: var(--transition);
}

.logo:hover {
  transform: scale(1.05);
}

.logo__icon {
  font-size: 1.75rem;
}

.nav__list {
  display: flex;
  list-style: none;
  gap: 2.5rem;
}

.nav__link {
  text-decoration: none;
  color: var(--gray-600);
  font-weight: 500;
  position: relative;
  padding: 0.5rem 0;
}

.nav__link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--primary-color);
  transition: width 0.3s ease;
}

.nav__link:hover::after {
  width: 100%;
}

.auth-buttons {
  display: flex;
  gap: 1rem;
}

.btn--danger {
  background: var(--danger-color);
  color: var(--white);
}

.btn--danger:hover {
  background: #c53030;
}

.btn--secondary {
  background: var(--gray-300);
  color: var(--gray-800);
}

.btn--secondary:hover {
  background: var(--gray-400);
}

.btn--outlined {
  border: 2px solid var(--primary-color);
  background: transparent;
  color: var(--primary-color);
}

.btn--outlined:hover {
  background: var(--primary-color);
  color: var(--white);
}

.btn--primary {
  background: var(--primary-color);
  color: var(--white);
  border: none;
}

.btn--primary:hover {
  background: var(--primary-dark);
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  opacity: 0.9;
}
</style>
