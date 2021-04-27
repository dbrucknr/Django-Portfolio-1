<template>
  <div>
    <b-button v-b-toggle.sidebar-backdrop-right>Messenger</b-button>
    <b-sidebar 
      id="sidebar-backdrop-right" 
      title="Messenger"
      :backdrop-variant="'dark'" 
      backdrop
      right 
      shadow
    >
      <div>
        <div v-for="(message, index) in messageThread" :key="index">
          <b-card
            :border-variant="setMessageColor(message.sender)"
            :header-bg-variant="setMessageColor(message.sender)"
            header-text-variant="white"
            :header="message.sender" 
            class="mb-2"
          >
            <b-card-text>
              {{ message.message }}
            </b-card-text>
           </b-card>
        </div>
        <b-form-group
          id="message-input"
        >
          <b-form-input
            id="main-message-input"
            v-model="messageContent"
            type="text"
            placeholder="Input Message"
            required
          ></b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary" @click="sendMessage">Submit</b-button>
        <!-- <button @click="sendMessage">Send Test Message</button> -->
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
        MessengerService.createMessage(payload);
        this.messageContent = '';
      },
      setMessageColor(sender) {
        return sender == this.getUsername ? 'primary' : 'success'
      }
    }
}
</script>