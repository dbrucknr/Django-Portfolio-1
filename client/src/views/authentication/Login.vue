<template>
  <div>
    <b-container fluid="sm">
      <h2>Welcome</h2>
      <b-card bg-variant="light" class="mb-3">
          <b-form-group
            label="Email"
            label-cols-lg="3"
          >
            <b-form-input v-model="user.email" type="email"></b-form-input>
          </b-form-group>
          <b-form-group
            label="Password"
            label-cols-lg="3"
          >
            <b-form-input v-model="user.password" type="password"></b-form-input>
          </b-form-group>
          <b-button @click="authenticate" variant="primary">Log In</b-button>
      </b-card>

      <b-button variant="outline-success" @click="registrationRedirect">Create an Account</b-button>
    </b-container>
  </div>
</template>

<script>
import User from '../../models/user';
import { mapActions, mapState } from "vuex";

export default {
  name: 'Login',
  data() {
    return {
      user: new User('', '')
    }
  },
  computed: {
    ...mapState('authentication', ['isAuthenticated'])
  },
  methods: {
    ...mapActions('authentication', ['login']),
    authenticate() {
      if (this.user.email && this.user.password) {
        this.login(this.user).then(
          () => { 
            this.$router.push('/home'); 
          },
          error => {
            console.log(error)
          }
        )
      }
    },
    registrationRedirect() {
      this.$router.push('/register');
    }
  }
}
</script>

