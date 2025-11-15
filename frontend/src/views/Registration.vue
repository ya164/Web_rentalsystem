<template>
  <div class="register">
    <div class="container">
      <h2 class="section-title">Реєстрація</h2>
      <form @submit.prevent="registerUser">
        <div class="form-group">
          <label for="username">Ім'я користувача</label>
          <input
            type="text"
            id="username"
            v-model="username"
            required
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label for="email">Електронна пошта</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            class="form-control"
          />
        </div>
        <div class="form-group">
          <label for="password">Пароль</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            class="form-control"
          />
        </div>
        <div v-if="errorMessage" class="alert alert-danger">
          {{ errorMessage }}
        </div>
        <button type="submit" class="btn btn--primary">Зареєструватися</button>
      </form>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    ...mapActions(['register']),
    async registerUser() {
      const userData = {
        username: this.username,
        email: this.email,
        password: this.password,
      };
      const { success, message } = await this.register(userData);
      if (success) {
        this.$router.push('/dashboard');
      } else {
        this.errorMessage = message;
      }
    },
  },
};
</script>

<style scoped>
.register {
  padding: 5rem 0;
}

.container {
  max-width: 500px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 1.5rem;
}

.alert {
  padding: 0.75rem 1.25rem;
  border: 1px solid transparent;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  color: #721c24;
  background-color: #f8d7da;
  border-color: #f5c6cb;
  margin-bottom: 1rem;
}

.btn--primary {
  background-color: var(--primary-color);
  color: var(--white);
  border: none;
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn--primary:hover {
  background-color: #0056b3;
}
</style>
