<template>
  <div id="login">
    <div id="login-form">
        <h2>Login</h2>
        <form v-on:submit.prevent="login" class="pure-form pure-form-stacked">
        <label><input v-model="email" placeholder="Email"></label>
        <label><input v-model="password" placeholder="Password" type="password"></label><br>
        <button type="submit" class="pure-button pure-button-primary">ログイン</button>
        <p>新たに<router-link to="signup">サインアップ</router-link>する</p>
        <p v-if="error" class="error">ログインに失敗しました</p>
        </form>
    </div>
  </div>
</template>

<script>
/* eslint-disable */ 
import axios from 'axios'
import auth from '../auth'

export default {
  
  data: function() {
    return {
        email: "",
        password: "",
        error: false,
    }
  },

  methods: {
    login: function() {
      let _this = this
      auth.authenticate(this.email, this.password).then(function(res){
        console.log(res)
        _this.$router.replace('/home')
      }).catch(function(err){
        console.log(err)
        _this.error = true
      })
    },
  }
};
</script>

<style>
#login {
    text-align: center;
}
#login-form {
    padding: .5em 1em;
    display: inline-block;
    margin: 0 auto;
}
</style>