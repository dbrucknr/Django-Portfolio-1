import Vue from 'vue'
import Vuex from 'vuex'

import { authentication } from './modules/auth.module';

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    authentication
  },
  state: {
    isAuthenticated: false
  },
  mutations: {
  },
  actions: {
  },
  getters: {
  }
})
