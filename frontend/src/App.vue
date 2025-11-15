<template>
  <div id="app">
    <AppHeader />
    <router-view />
    <AppFooter />
  </div>
</template>

<script>
import { onMounted } from 'vue';
import AppHeader from './components/AppHeader.vue';
import AppFooter from './components/AppFooter.vue';
import store from './store';
import axios from './axios';

export default {
  name: 'App',
  components: {
    AppHeader,
    AppFooter,
  },
  setup() {
    onMounted(() => {
      store.commit('setAuth', !!localStorage.getItem('access_token'));
      if (store.state.isAuthenticated && !store.state.user) {
        axios.get('/auth/me')
          .then(response => {
            if (response.status === 200) {
              store.commit('setUser', response.data);
            }
          })
          .catch(() => {
            store.dispatch('logout');
          });
      }
    });
  },
};
</script>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
