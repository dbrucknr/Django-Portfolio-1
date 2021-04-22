<template>
  <b-navbar toggleable="sm" type="light" variant="light" class="fixed-bottom">
    <b-navbar-brand>Footer</b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <b-nav-item right>
            <Messenger />
        </b-nav-item>
      </b-navbar-nav>
  </b-navbar>
</template>

<script>
import Messenger from './Messenger'
export default {
  name: 'Footer',
  components: {
    Messenger
  }
}
</script>
