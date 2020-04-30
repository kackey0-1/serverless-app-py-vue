<template>
<div id="app">
    <header class="text-box pure-u-1 pure-u-md-1 pure-u-lg-1 pure-u-xl-1">
        <div class="l-box">
            <h1 class="text-box-head">Sample Gallery</h1>
            <p class="text-box-subhead">A collection of various assets from around the world</p>
        </div>
    </header>
    <div class="content">
        <nav class="sidebar-left" v-if="isLoggedIn">
            <div class="pure-menu">
                <ul class="pure-menu-list">
                    <li class="pure-menu-item">
                        <router-link to="/home" class="pure-menu-link">Home</router-link>
                    </li>
                    <li class="pure-menu-item">
                        <a href="#upload-image" class="pure-menu-link">Upload</a>
                    </li>
                    <li class="pure-menu-item">
                        <a href="#" class="pure-menu-link">Settings</a>
                    </li>
                    <li class="pure-menu-item">
                        <router-link to="/logout" class="pure-menu-link">Logout</router-link>
                    </li>
                </ul>
            </div>
        </nav>
        <main><router-view/></main>
    </div>
    <footer>
        This sample app was made by kackey0-1.
    </footer>
</div>
</template>

<script>
/* eslint-disable */ 
import auth from "./auth";
export default {
  data() {
    return {
        isLoggedIn: auth.loggedIn()
    };
  },
  created: function() {
    auth.onChange = isLoggedIn => {
        this.isLoggedIn = isLoggedIn;
    };
  }
};
</script>

<style>
#app {
    display: flex;
    flex-direction: column;
}
/* header css */
.text-box-head {
  color: #fff;
  padding-bottom: 0.2em;
  font-weight: 400;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 24px;
}

.text-box-subhead {
  font-weight: normal;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}

h1 {
  font-size: 2em;
  margin: 0.67em 0;
}

.l-box {
  padding: 2em;
}

.text-box {
  text-align: left;
  overflow: hidden;
  position: relative;
  height: 180px;
  background: rgb(49, 49, 49);
  color: rgb(255, 190, 94);
}

/* content css */
.content {
    flex: 1;
    display: flex;
}

.sidebar-left {
    width: 150px;
    display: flex;
    text-align: center;
    flex-direction: column;
    background: rgb(49, 49, 49);
}
.pure-menu {
    border-radius: 0;
    color: white;
    font-style: bold;
}
main {
    flex: 1;
}

.pure-menu-link {
  padding: 1em 1em;
}

/* footer css */
footer {
    color: #ffffff;
    font-size: 87.5%;
    border-top: 0;
    margin-top: 0;
    padding: 1em;
    background: rgb(49, 49, 49);
}
</style>
