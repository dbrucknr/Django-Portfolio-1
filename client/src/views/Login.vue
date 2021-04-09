<template>
  <div>
    <b-container fluid="sm">
      <b-card bg-variant="light">
          <b-form-group
            label="Email"
            label-cols-lg="3"
          >
            <b-form-input v-model="email" type="email"></b-form-input>
          </b-form-group>
          <b-form-group
            label="Password"
            label-cols-lg="3"
          >
            <b-form-input v-model="password" type="password"></b-form-input>
          </b-form-group>
          <b-button @click="authenticate" variant="primary">Log In</b-button>
      </b-card>
    </b-container>
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
          let user = { 'email': response.data.email, 'username': response.data.username }
          this.updateToken(response.data.access);
          this.setAuthUser({ user: user, isAuthenticated: true })
          // const base = {
          //   baseURL: 'http://127.0.0.1:8000/api/users/',
          //   headers: {
          //     Authorization: `Bearer ${this.$store.state.token}`,
          //     'Content-Type': 'application/json'
          //   },
          //   xhrFields: {
          //       withCredentials: true
          //   }
          // };
          // const axiosInstance = axios.create(base)
          // axiosInstance({
          //   url: "/",
          //   method: "get",
          //   params: {}
          // }).then((response) => {
          //   // console.log('Is there a user object here:', response)
          //   this.setAuthUser({ user: response.data, isAuthenticated: true })
          // })
        })
    }
  }
}
</script>

