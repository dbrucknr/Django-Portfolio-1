import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {},
    isAuthenticated: false,
    token: localStorage.getItem('token')
  },
  mutations: {
    initializeAuth(state) {
      if (localStorage.getItem('token')) {
        console.log('token found')
        state.token = localStorage.getItem('token');
        state.isAuthenticated = true;
      }
    },
    setAuthUser(state, { user, isAuthenticated }) {
      Vue.set(state, 'user', user)
      Vue.set(state, 'isAuthenticated', isAuthenticated)
    },
    updateToken(state, newToken) {
        // TODO: For security purposes, take localStorage out of the project.
        localStorage.setItem('token', newToken);
        state.token= newToken;
    },
    removeToken(state) {
        // TODO: For security purposes, take localStorage out of the project.
        localStorage.removeItem('token');
        state.token = null;
    }
  },
  actions: {
  },
  getters: {
    getToken(state) {
      return state.token
    }
  },
  modules: {
  }
})
