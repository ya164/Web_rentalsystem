import { createStore } from 'vuex';
import axios from './axios';

const store = createStore({
  state: {
    isAuthenticated: false,
    user: null,
  },
  mutations: {
    SET_AUTH(state, value) {
      state.isAuthenticated = value;
    },

    SET_USER(state, userData) {
      state.user = userData;
    },
  },
  actions: {
    async login({ commit, dispatch }, credentials) {
      try {
        const response = await axios.post('/auth/login', credentials);
        if (response.status === 200 && response.data.access_token) {
          localStorage.setItem('access_token', response.data.access_token);
          commit('SET_AUTH', true);
          await dispatch('fetchUser');
          return { success: true, message: 'Вхід успішний' };
        } else {
          return { success: false, message: 'Несподівана відповідь від сервера' };
        }
      } catch (error) {
        console.error('Помилка входу:', error);
        let message = 'Вхід не вдалося. Спробуйте ще раз.';
        if (error.response && error.response.data && error.response.data.msg) {
          message = error.response.data.msg;
        }
        return { success: false, message };
      }
    },

    async register({ commit, dispatch }, userData) {
      try {
        const response = await axios.post('/auth/register', userData);
        if (response.status === 201 && response.data.access_token) {
          localStorage.setItem('access_token', response.data.access_token);
          commit('SET_AUTH', true);
          await dispatch('fetchUser');
          return { success: true, message: 'Реєстрація успішна' };
        } else {
          return { success: false, message: 'Несподівана відповідь від сервера' };
        }
      } catch (error) {
        console.error('Помилка реєстрації:', error);
        let message = 'Реєстрація не вдалася. Спробуйте ще раз.';
        if (error.response && error.response.data && error.response.data.msg) {
          message = error.response.data.msg;
        }
        return { success: false, message };
      }
    },

    async fetchUser({ commit }) {
      try {
        const response = await axios.get('/auth/me');
        if (response.status === 200) {
          commit('SET_USER', response.data);
          commit('SET_AUTH', true);
        } else {
          commit('SET_USER', null);
          commit('SET_AUTH', false);
        }
      } catch (error) {
        console.error('Помилка завантаження даних користувача:', error);
        commit('SET_USER', null);
        commit('SET_AUTH', false);
      }
    },

    async logout({ commit }) {
      try {
      } catch (error) {
        console.error('Помилка виходу:', error);
      } finally {
        localStorage.removeItem('access_token');
        commit('SET_USER', null);
        commit('SET_AUTH', false);
      }
    },

    async initializeStore({ dispatch }) {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          await dispatch('fetchUser');
        } catch (error) {
          console.error('Помилка ініціалізації store:', error);
          await dispatch('logout');
        }
      }
    },
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated,
    user: (state) => state.user,
  },
});

export default store;
