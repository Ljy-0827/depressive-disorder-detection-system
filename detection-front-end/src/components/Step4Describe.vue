<template>
  <div class="mask" v-loading="isUploading"
       element-loading-text="请稍等，数据正在上传中" v-if="isUploading" >
  </div>
  <div class="top-container">
    <div class="top-banner">
      <img class="top-banner-pic" src="../assets/setting-pic/page-banner.png" alt="" />
    </div>
    <div class="step-bar-container">
      <el-steps :active="4" align-center>
        <el-step title="量表填写" />
        <el-step title="情绪图片观看" />
        <el-step title="文字朗读" />
        <el-step title="人脸图片描述" />
        <el-step title="机器人访谈" />
      </el-steps>
    </div>
    <div class="title-box">
      <div class="page-title">人脸图片描述</div>
      <div class="page-description">请您认真观看并描述屏幕上的图片，请尽可能多地说出您理解的内容</div>
    </div>
  </div>
  <div class="bottom-container">
    <div class="pic-box">
      <img src="../assets/detection-images/face-1.bmp" class="picture" v-show="this.describePic === 'pic1'">
      <img src="../assets/detection-images/face-2.bmp" class="picture" v-show="this.describePic === 'pic2'">
      <img src="../assets/detection-images/face-3.bmp" class="picture" v-show="this.describePic === 'pic3'">
    </div>
    <button class="begin-watching-button" @click="startDescribe" v-show="this.describePic === '0'">开始描述</button>
    <button class="begin-watching-button" @click="nextPicture" v-show="this.describePic === 'pic1' || this.describePic === 'pic2'">下一张</button>
    <button class="begin-watching-button" @click="finishDescribe" v-show="this.describePic === 'pic3'">结束描述</button>
  </div>
</template>

<script>
import {ElMessage} from "element-plus";

export default {
  name: "Step4Describe",
  data(){
    return{
      describePic: '0',
      isRecording: false,
      audioChunks: [],
      audioUrl: null,
      mediaRecorder: null,
      isUploading: false,
    }
  },
  methods:{
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
        this.isUploading = true;
        setTimeout(this.sendAudioToBackend,1000);
      }
    },

    async sendAudioToBackend() {
      try {
        const blob = new Blob(this.audioChunks, {type: 'audio/wav'});
        const formData = new FormData();
        formData.append('audio', blob, 'step4-audio.wav');

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
          this.$router.push({name: 'step-complete', query: {currentPage: '4'}});
        } else {
          ElMessage.error('录音上传失败');
          this.isUploading = false;
        }
      } catch (error) {
        ElMessage.error('录音上传失败');
        this.isUploading = false;
      }
    },

    startDescribe(){
      this.startRecording();
      this.describePic = 'pic1';
    },

    nextPicture(){
      if(this.describePic === 'pic1'){
        this.describePic = 'pic2';
      }else if(this.describePic === 'pic2'){
        this.describePic = 'pic3';
      }
    },

    finishDescribe(){
      this.describePic = '0';
      this.stopRecording();
    }
  }
}
</script>

<style scoped>
@import "@/components/stylesheet/steps/step-4-describe.css";
</style>