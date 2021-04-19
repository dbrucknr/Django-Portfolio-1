<template>
  <div id="app">
    <NavigationBar :authStatus="isAuthenticated" />
    <router-view />
  </div>
</template>

<script>
  import NavigationBar from './components/NavigationBar'
  import { mapMutations, mapActions, mapGetters } from 'vuex'
  export default {
    components: {
      NavigationBar
    },
    created() {
      this.initializeAuthAction();
    },
    computed: {
      ...mapGetters('authentication', ['isAuthenticated'])
    },
    methods: {
      ...mapActions('authentication', ['initializeAuthAction'])
    }
  }
</script>

<style>

</style>
