<template>
<div class="pure-g">
    <div class="text-box pure-u-1 pure-u-md-1 pure-u-lg-1 pure-u-xl-1">
        <div class="l-box">
            <h1 class="text-box-head">Photo Gallery</h1>
            <p class="text-box-subhead">A collection of various photos from around the world</p>
        </div>
    </div>
    <div v-for="image in images" :key="image.photo_id" class="photo pure-u-1-3 pure-u-md-1-3 pure-u-lg-1-3 pure-u-xl-1-3">
        <img v-bind:src="image_url_base + '/' +image.photo_id + '.' + image.type.split('/')[1]">
    </div>
    <div class="pure-u-1 form-box" id="upload-image">
        <div class="l-box">
            <h2>Upload a Photo</h2>
            <input v-on:change="onFileChange" type="file" name=" file" placeholder="Photo from your computer" accept=" image/*" required>
            <button v-on:click="uploadImage" class="pure-button pure-button-primary"> アップロード</button>
        </div>
    </div>
</div>
</template>
<script>
/* eslint-disable */
import axios from 'axios'
import appConfig from '../config'

const API_BASE_URL = appConfig.ApiBaseUrl
const IMAGE_BASE_URL = appConfig.ImageBaseUrl

export default {
  data: function () {
    return {
      image_url_base: appConfig.ImageBaseUrl,
      uploadFile: null,
      images: []
    }
  },
  // 初期化（ページのロード時）処理
  created: function() {
    this.listImages();  
  },
  // 初期化処理
  methods: {
    //画像情報の一覧取得APIにアクセスして結果をセットする
    listImages: function() {
      let self = this;
      let _this = this;
      axios.get(API_BASE_URL + "/images/").then(function(res) {
        console.log(res)
        self.$data.images = res.data;
      });
    },
    // onChangeを引数としてuploadFileに格納
    onFileChange: function (event) {
      this.uploadFile = event.target.files[0]
    },
    // 画像情報uploadAPIをキック
    uploadImage: function () {
      let file = this.uploadFile
      let json = null
      let _this = this
      // 画像アップロード用APIを呼び出してアップロードする画像のキーやアップロード用署名付きURLを取得
      let data = { size: file.size, type: file.type }
      axios
        .post(
          API_BASE_URL + '/images/',
          JSON.stringify(data)
        )
        .then(function (res) {
          json = JSON.parse(JSON.stringify(res.data))
          console.log(json)
          // 取得した署名付きURLを用いてファイルをAmazon S3にアップロード
          axios
            .put(json['signed_url'], file, {
              headers: {
                "Content-Type": file.type
              }
            })
            // 画像アップロードが成功したら画像情報のステータスを更新
            .then(function (res) {
              json['status'] = 'Uploaded'
              let self = this
              axios
                .put(
                  API_BASE_URL + '/images/',
                  json
                )
                .then(function (res) {
                  alert('Successfully uploaded photo.')
                  _this.$router.go(_this.$router.currentRoute);
                })
            })
            .catch(function (error) {
              // alert(error)
              console.log(error)
            })
        })
        .catch(function (error) {
          // alert(error)
          console.log(error)
        })
    }
  }
}
</script>
<style>
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
.photo {
  height: 250px;
  overflow: hidden;
}
.photo img {
  max-width: 100px;
  min-height: 250px;
  height: auto;
}
</style>
