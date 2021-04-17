<template>
  <div id="app">
    <NavigationBar />
    <router-view />
  </div>
</template>

<script>
  import NavigationBar from './components/NavigationBar'
  import { mapState, mapMutations, mapActions } from 'vuex'
  export default {
    components: {
      NavigationBar
    },
    created() {
      this.initializeAuth();
      this.initializeAuthAction()
    },
    computed: {
      ...mapState('authentication', ['isAuthenticated'])
    },
    methods: {
      ...mapMutations('authentication', ['initializeAuth']),
      ...mapActions('authentication', ['initializeAuthAction'])
    }
  }
</script>

<style>

</style>
