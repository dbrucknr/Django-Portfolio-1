<template>
  <div>
    <b-container fluid="sm">
      <h2>Register</h2>
      <b-card bg-variant="light" class="mb-3">
          <b-form-group
            label="Username"
            label-cols-lg="3"
          >
            <b-form-input v-model="user.username" type="text"></b-form-input>
          </b-form-group>

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
            <b-form-input v-model="user.password1" type="password"></b-form-input>
          </b-form-group>
          <b-form-group
            label="Verify Password"
            label-cols-lg="3"
          >
            <b-form-input v-model="user.password2" type="password"></b-form-input>
          </b-form-group>
          <b-button @click="completeRegistration" variant="primary">Create Account</b-button>
      </b-card>
        <p>Already have an Account?</p>
      <b-button @click="loginRedirect" variant="outline-success">Login</b-button>
    </b-container>
  </div>
</template>

<script>
import { mapActions } from "vuex";
import UserRegistration from '../../models/userRegistration';
export default {
    name: 'Registration',
    data() {
        return {
            user: new UserRegistration('', '', '', '')
        }
    },
    methods: {
        ...mapActions('authentication', ['register']),
        completeRegistration() {
            if (this.user.username && this.user.email && this.user.password1 == this.user.password2) {
                this.register(this.user).then(
                    () => {
                        this.$router.push('/login')
                    },
                    error => {
                        console.log(error)
                    }
                )
            }
        },
        loginRedirect() {
            this.$router.push('/login');
        }
    }

}
</script>