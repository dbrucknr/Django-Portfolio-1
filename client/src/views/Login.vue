<template>
  <div>
    <form>
      <div>
        <label for="email">Email</label>
        <input
          v-model="email" 
          type="text"
          placeholder="Email"
        >
      </div>
      <div>
        <label for="password">Password</label>
        <input
          v-model="password" 
          type="text"
          placeholder="Password"
        >
      </div>
      <button
        @click.prevent="authenticate"
        type="submit"
      >
        Log In
      </button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import { mapMutations } from "vuex";

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    ...mapMutations(['updateToken', 'setAuthUser']),
    authenticate() {
      const payload = {
        email: this.email,
        password: this.password
      }
      axios.post('http://127.0.0.1:8000/api/log_in/', payload)
        .then((response) => {
          console.log(response);
          this.updateToken(response.data.access);
          const base = {
            baseURL: 'http://127.0.0.1:8000/api/users/',
            headers: {
              Authorization: `Bearer ${this.$store.state.token}`,
              'Content-Type': 'application/json'
            },
            xhrFields: {
                withCredentials: true
            }
          };
          const axiosInstance = axios.create(base)
          axiosInstance({
            url: "/",
            method: "get",
            params: {}
          }).then((response) => {
            // console.log('Is there a user object here:', response)
            this.setAuthUser({ user: response.data, isAuthenticated: true })
          })
        })
    }
  }
}
</script>

