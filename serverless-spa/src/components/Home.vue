<template>
<div class="pure-g">
    <div class="pure-u-1 form-box" id="upload-image">
        <div class="l-box">
            <h2>Home Page</h2>
        </div>
    </div>
</div>
</template>

<script>
/* eslint-disable */
import axios from "axios";
import appConfig from "../config";
import auth from "../auth";

const API_BASE_URL = appConfig.ImagesApiBaseUrl;
const IMAGE_BASE_URL = appConfig.S3BaseUrl;

export default {
  data: function() {
    return {
        image_url_base: appConfig.S3BaseUrl,
        title: "",
        uploadFile: null,
        images: []
    };
  },

  //初期化（ページのロード時）処理
  created: function() {
    this.listImages();
  },

  methods: {
    //画像情報の一覧取得APIにアクセスして結果をセットする
    listImages: function() {
      var self = this;
      var auth_header = auth.get_id_token();

      axios
        .get(API_BASE_URL + "/images/", {
          headers: { Authorization: auth_header }
        })
        .then(function(res) {
          self.$data.images = res.data;
        });
    },

    //onChangeを引数としてuploadFileに格納するだけ
    onFileChange: function(event) {
      this.uploadFile = event.target.files[0];
    },

    uploadImage: function() {
      var file = this.uploadFile;
      var json = null;
      var _this = this;
      var auth_header = auth.get_id_token();

      //画像アップロード用APIを呼び出してアップロードする画像のキーやアップロード用署名付きURLを取得
      var data = { size: file.size, type: file.type, title: this.title };
      axios
        .post(API_BASE_URL + "/images/", data, {
          headers: { Authorization: auth_header }
        })
        .then(function(res) {
          json = JSON.parse(JSON.stringify(res.data));
          //取得した署名付きURLを用いてファイルをAmazon S3にアップロード
          axios
            .put(json["signed_url"], file, {
              headers: {
                "Content-Type": file.type
                // 'Authorization': auth_header
              }
            })
            //画像のアップロードが成功したら画像情報のステータスを更新する
            .then(function(res) {
              json["status"] = "Uploaded";
              var self = this;
              axios
                .put(API_BASE_URL + "/images/", json, {
                  headers: { Authorization: auth_header }
                })
                .then(function(res) {
                  alert("Successfully uploaded photo.");
                  _this.$router.go(_this.$router.currentRoute);
                });
            })
            .catch(function(error) {
              alert(error);
              console.log(error);
            });
        })
        .catch(function(error) {
          alert(error);
        });
    }
  }
};
</script>

<style>

</style>