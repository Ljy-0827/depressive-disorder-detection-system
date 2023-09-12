<template>
  <div class="view-container" style="display: block">
    <div class="mask" v-loading="isUploading"
         element-loading-text="请稍等，录音正在上传中" v-if="isUploading" >
    </div>
    <div class="box-container">
      <div class="text-box" v-show="isText1">
        {{this.readText1}}
      </div>
      <div class="text-box" v-show="isText2">
        {{this.readText2}}
      </div>
    </div>
    <div class="page-switch-container">
      <button class="page-switch-button" id="button-left" @click="toText1" v-show="isText2">
        <i class="bi bi-arrow-left-short" id="left-arrow"></i>
      </button>
      <button class="page-switch-button" id="button-right" @click="toText2" v-show="isText1">
        <i class="bi bi-arrow-right-short" id="right-arrow"></i>
      </button>
    </div>
    <div class="option-buttons">
      <button class="read-button" @click="startRecording" v-show="!isRecording">开始朗读</button>
      <button class="read-button" @click="stopRecording" v-show="isRecording">结束朗读</button>
    </div>
  </div>

</template>

<script>
import { text1, text2 } from "@/utils.js";
import { ElMessage } from "element-plus";

export default {
  name: "Step3MainTest",
  data(){
    return{
      readText1: text1,
      readText2: text2,
      isUploading: false,
      isText1: true,
      isText2: false,
      isRecording: false,
      audioChunks: [],
      audioUrl: null,
      mediaRecorder: null,
    }
  },

  methods:{
    toText1(){
      this.isText1 = true;
      this.isText2 = false;
    },

    toText2(){
      this.isText2 = true;
      this.isText1 = false;
    },

    startRecording() {
      navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        this.isRecording = true;
        this.audioChunks = [];
        this.mediaRecorder = new MediaRecorder(stream);
        this.mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            this.audioChunks.push(event.data);
          }
        };
        this.mediaRecorder.onstop = () => {
          this.isRecording = false;
          const audioBlob = new Blob(this.audioChunks, { type: "audio/wav" });
          this.audioUrl = URL.createObjectURL(audioBlob);
        };
        this.mediaRecorder.start();
        ElMessage({
          message: '录音已开始',
          type: 'success',
        });
      });
    },

    stopRecording() {
      if (this.mediaRecorder && this.isRecording) {
        this.mediaRecorder.stop();
        setTimeout(this.sendAudioToBackend,1000);
      }
    },

    async sendAudioToBackend() {
      this.isUploading = true;
      try {
        const blob = new Blob(this.audioChunks, {type: 'audio/wav'});
        const formData = new FormData();
        formData.append('audio', blob, 'step3-audio.wav');

        const response = await fetch("http://192.168.31.23:8080/upload-audio", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          ElMessage({
            message: '录音已成功上传',
            type: 'success',
          });
          this.isUploading = false;
          this.$router.push({name: 'step-complete', query: {currentPage: '3'}});
        } else {
          ElMessage.error('录音上传失败');
          this.isUploading = false;
        }
      } catch (error) {
        ElMessage.error('录音上传失败');
        this.isUploading = false;
      }
    },
  }
}
</script>

<style scoped>
@import "@/components/stylesheet/steps/step-3-main-test.css";
</style>