<template>
  <div id="app">
    <NavigationBar />
    <router-view />
  </div>
</template>

<script>
  import NavigationBar from './components/NavigationBar'
  import { mapState, mapMutations } from 'vuex'
  export default {
    components: {
      NavigationBar
    },
    created() {
      this.initializeAuth()
    },
    computed: {
      ...mapState('authentication', ['isAuthenticated'])
    },
    methods: {
      ...mapMutations('authentication', ['initializeAuth'])
    }
  }
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
