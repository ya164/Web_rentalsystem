import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import './assets/styles.css';
const app = createApp(App);

store.dispatch('initializeStore').then(() => {
  app.use(router).use(store).mount('#app');
});
