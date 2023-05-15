<template>
  <div>
    <div v-if="!connected">
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <input v-model="hostname" placeholder="Hostname" />
      <button @click="connect">Connect</button>
    </div>
    <div v-else>
      <textarea v-model="output" readonly></textarea>
      <input v-model="input" @keyup.enter="send" placeholder="Enter command" />
    </div>
  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  data() {
    return {
      username: '',
      password: '',
      hostname: '',
      connected: false,
      output: '',
      input: '',
      socket: null,
    };
  },
  methods: {
    connect() {
      this.socket = io('http://localhost:8000');
      this.socket.on('connect', () => {
        this.connected = true;
        this.socket.emit('message', `${this.username}:${this.password}:${this.hostname}`);
      });
      this.socket.on('message', (data) => {
        this.output += data;
      });
    },
    send() {
      this.socket.emit('message', this.input);
      this.input = '';
    },
  },
};
</script>