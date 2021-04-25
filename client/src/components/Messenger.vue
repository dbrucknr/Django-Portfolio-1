<template>
  <div>
    <b-button v-b-toggle.sidebar-right>Messenger</b-button>
    <b-sidebar id="sidebar-right" title="Messenger" right shadow>
      <div>
        <div v-for="(message, index) in messageThread" :key="index">
          {{ message.sender }}: {{ message.message }}
        </div>
        <input type="text" v-model="messageContent">
        <button @click="sendMessage">Send Test Message</button>
      </div>
    </b-sidebar>
  </div>
</template>

<script>
import MessengerService from '../services/messenger.service'
import { mapState } from 'vuex'
export default {
    name: 'Messenger',
    created() {
      MessengerService.connect();
    },
    data() {
      return {
        messageContent: '',
        messageThread: MessengerService.messageThread()
      }
    },
    computed: {
      ...mapState('authentication', ['user']),
      getUsername() {
        return JSON.parse(this.user).username
      }
    },
    methods: {
      sendMessage() {
        let payload = {
          'sender': this.getUsername,
          'content': this.messageContent
        }
        MessengerService.createMessage(payload)
      }
    }
}
</script>