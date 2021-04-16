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

</style>
