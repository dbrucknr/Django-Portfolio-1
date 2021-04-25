<template>
  <div>
    <b-button v-b-toggle.sidebar-right>Messenger</b-button>
    <b-sidebar id="sidebar-right" title="Messenger" right shadow>
      <div>
        <div v-for="(message, index) in messageThread" :key="index">
          {{ message.data.sender.username }} - {{ message.data.content }}
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
    data() {
      return {
        messageContent: '',
        messageThread: MessengerService.messageThread()
      }
    },
    computed: {
      ...mapState('authentication', ['user']),
      // test() {
      //   return MessengerService.messageThread()
      // }
    },
    methods: {
      sendMessage() {
        let payload = {
          sender: "1",
          receiver: '2',
          content: this.messageContent
        }
        MessengerService.createMessage(payload)
      }
    }
}
</script>