<template>
<div class="pure-g">
    <div class="photo-detail pure-u-1 pure-u-md-1 pure-u-lg-1 pure-u-xl-1">
        <!-- <img v-bind:src="image_url_base + '/' + photo_id + '.' + type"> -->
        <video v-bind:src="video_url_base + '/' + video_id + '.' + type" autoplay />
    </div>
    <button v-on:click="deleteVideo" class="pure-button">この画像を削除する</button>
</div>
</template>
<script>
/* eslint-disable */
import axios from "axios";
import appConfig from "../config";
import auth from "../auth";

const API_BASE_URL = appConfig.VideosApiBaseUrl;
const VIDEO_BASE_URL = appConfig.S3BaseUrl;

export default {
  data: function() {
    return {
      video_url_base: appConfig.S3BaseUrl,
      // photo_id: this.$route.params.photo_id,
      video_id: this.$route.params.video_id,
      type: this.$route.params.type,
      labels: []
    };
  },
  created: function() {
    this.getVideo();
  },
  methods: {
    getVideo: function() {
      var self = this;
      var auth_header = auth.get_id_token();

      axios
        // .get(API_BASE_URL + "/videos/" + this.photo_id, {
        .get(API_BASE_URL + "/videos/" + this.video_id, {
          headers: { Authorization: auth_header }
        })
        .then(function(res) {
          console.log(res.data);
          self.$data.type = res.data[0].type.split("/")[1];
        });
    },
    deleteVideo: function() {
      var self = this;
      var auth_header = auth.get_id_token();
      axios
        // .delete(API_BASE_URL + "/videos/" + this.photo_id, {
        .delete(API_BASE_URL + "/videos/" + this.video_id, {
          headers: { Authorization: auth_header }
        })
        .then(function(res) {
          // console.log(self.photo_id + "is deleted.");
          console.log(self.video_id + "is deleted.");
          alert("動画を削除しました");
          self.$router.replace("/");
        });
    }
  }
};
</script>
<style>
.header .pure-menu {
  border-bottom-color: black;
  border-radius: 0;
}
.pure-menu-link {
  padding: 1em 0.7em;
}
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
.photo-detail img {
  max-width: 100%;
  min-height: 250px;
  height: auto;
}
.photo img {
  max-width: 100%;
  min-height: 250px;
  height: auto;
}
a {
  letter-spacing: 0em;
}
</style>