<template>
  <div id="app">
    <div class="header">
      <div class="pure-menu pure-menu-horizontal">
        <a class="pure-menu-heading" href="#">Photo Gallery</a>
        <ul class="pure-menu-list">
          <li class="pure-menu-item selected"><a href="#" class="pure-menu-link">Home</a></li>
          <li class="pure-menu-item"><a href="#" class="pure-menu-link">Setting</a></li>
          <li class="pure-menu-item"><a href="#" class="pure-menu-link">Login</a></li>
        </ul>
      </div>
    </div>
    <router-view/>
    <div class="footer">
      This sample app was made by hogehoge fugafuga
    </div>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
.header {
  border-bottom-color: black;
  border-radius: 0;
}
.pure-menu-link {
  padding: 1em 0.7em;
}

.footer {
  color: #FFFFFF;
  border-top: 1px solid #eee;
  margin-top: 1em;
  padding: 1em;
  background: rgb(49, 49, 49);
}
</style>
