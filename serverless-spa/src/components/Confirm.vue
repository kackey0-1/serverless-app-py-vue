<template>
  <div id="confirm">
    <div id="confirm-form">
      <h2>Confirmation</h2>
      <p>
        We sent a confirmation code to {{ email }}.<br>
        Enter it below to activate your account.
      </p>
      <form v-on:submit.prevent="confirm" class="pure-form pure-form-stacked">
        <label><input v-model="confirmation_code" placeholder="Cofirmation code"></label><br>
        <button type="submit" class="pure-button pure-button-primary">登録</button>
        <p v-if="error" class="error">サインアップに失敗しました</p>
    </form>
    </div>
  </div>
</template>

<script>
/* eslint-disable */ 
import axios from 'axios'
import auth from '../auth'
import store from '../credential_store'

export default {
  
  data: function() {
    return {
        username: '',
        email: '',
        error: false,
        confirmation_code: '',
        state: store.state
    }
  },

  created: function(){
      console.log(this.state.email)
      this.email = this.state.email
      this.username = this.state.username
  },

  methods: {
    confirm: function() {
      let _this = this
      auth.confirm(this.username, this.confirmation_code).then(function(res){
        console.log(res)
        _this.$router.replace('/home') 
      }).catch(function(err){
        console.log(err)
        _this.error = true
      })
    },
    changeEmail: function(email) {
      this.$data.email = email
    }

  }
};
</script>

<style>
#confirm {
  text-align: center;
}
#confirm-form {
  padding: .5em 1em;
  display: inline-block;
  margin: 0 auto;
}
#confirm-form input {
  width: 100%;
  text-align: center;
}
</style>