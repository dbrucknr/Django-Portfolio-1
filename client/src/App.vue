<template>
  <div id="app">
    <NavigationBar :authStatus="isAuthenticated" />
    <router-view />
    <FooterBar />
  </div>
</template>

<script>
  import NavigationBar from './components/NavigationBar'
  import FooterBar from './components/FooterBar'
  import { mapActions, mapGetters } from 'vuex'
  export default {
    components: {
      NavigationBar,
      FooterBar
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
