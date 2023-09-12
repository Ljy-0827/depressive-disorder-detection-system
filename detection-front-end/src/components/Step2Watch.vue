<template style="padding: 0">
  <div class="mask" v-loading="isUploading"
       element-loading-text="请稍等，视频正在上传中" v-if="isUploading" >
  </div>
  <div class="top-container">
    <div class="top-banner">
      <img class="top-banner-pic" src="../assets/setting-pic/page-banner.png" alt="" />
    </div>
    <div class="step-bar-container">
      <el-steps :active="2" align-center>
        <el-step title="量表填写" />
        <el-step title="情绪图片观看" />
        <el-step title="文字朗读" />
        <el-step title="人脸图片描述" />
        <el-step title="机器人访谈" />
      </el-steps>
    </div>
    <div class="title-box">
      <div class="page-title">情绪图片观看</div>
      <div class="page-description">请您认真观看屏幕上的图片，观看时，将视线集中在屏幕中央</div>
    </div>
  </div>
  <div class="bottom-container">
    <div class="main-emotion-pic-container">
      <div class="pic-box">
        <img class="emotion-pic" v-if="showImage" :src="this.currentImageSrc"/>
      </div>
      <button class="begin-watching-button" @click="startRecording" v-show="!allowNextStep">开始观看</button>
      <button class="begin-watching-button" v-show="allowNextStep" @click="this.$router.push('/text_audio')">下一步</button>

    </div>
    <div class="camera-container">
      <button class="open-camera-button" v-if="!isCameraOpen" @click="openCamera">打开摄像头</button>
      <video ref="videoElement" autoplay class="camera" v-if="isCameraOpen" muted></video>
    </div>
  </div>

</template>

<script>
import { shuffleArray, getImageUrl } from "@/utils.js";
import { ElMessage } from 'element-plus'

export default {
  name: "Step2Watch",
  data() {
    return {
      isCameraOpen: false,
      isRecording: false,
      allowNextStep: false,
      isUploading: false,
      mediaStream: null,

      mediaRecorder: null,
      chunks: [],
      randomPicArray: [1,2,3,4,5,6,7,8,9,10],
      showImage: false,
      currentImageSrc: '',
      picCnt: 0,
      groupCnt: 1,
      picInterval: null,
    };
  },

  setup(){
    function getImage(url) {
      return getImageUrl(url);
    }

    return {
      getImage
    }
  },
  methods: {
    beginDisplayPic(){
      if(!this.isCameraOpen){
        ElMessage.error('需要先打开摄像头');
        return;
      }
      this.showImage = true;
      this.randomPicArray = shuffleArray(this.randomPicArray);
      this.currentImageSrc = this.getImage(`./assets/detection-images/group${this.groupCnt}-${this.randomPicArray[this.picCnt]}.png`);
      setTimeout(this.showBlank, 3000);
      this.picInterval = setInterval(this.showNextImage, 4000);
    },

    showNextImage(){
      if(this.picCnt < 9){
        this.picCnt ++;
        this.currentImageSrc = this.getImage(`./assets/detection-images/group${this.groupCnt}-${this.randomPicArray[this.picCnt]}.png`);
        setTimeout(this.showBlank, 3000);
      }else if(this.picCnt === 9 && this.groupCnt !== 3){
        this.picCnt = 0;
        this.groupCnt ++;
        this.randomPicArray = shuffleArray(this.randomPicArray);
        this.currentImageSrc = this.getImage(`./assets/detection-images/group${this.groupCnt}-${this.randomPicArray[this.picCnt]}.png`);
        setTimeout(this.showBlank, 3000);
      }else if(this.picCnt === 9 && this.groupCnt === 3){
        this.stopRecording();
        this.showImage = false;
        clearInterval(this.picInterval);
        setTimeout(this.postVideoToBackend, 1000);
      }
    },
    showBlank(){
      this.currentImageSrc = this.getImage('./assets/detection-images/blank.png');
    },

    async openCamera() {
      this.isCameraOpen = true;
      console.log(this.isRecording);
      try {
        this.mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        this.$refs.videoElement.srcObject = this.mediaStream;

        ElMessage({
          message: '摄像头连接成功',
          type: 'success',
        });
      } catch (error) {
        ElMessage.error('无法访问摄像头');
        console.error('无法访问摄像头', error);
      }
    },
    startRecording() {

      this.isRecording = true;
      this.beginDisplayPic();

      this.mediaRecorder = new MediaRecorder(this.mediaStream);
      this.chunks = [];

      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.chunks.push(event.data);
        }
      };

      this.mediaRecorder.start();
    },

    stopRecording() {
      this.isRecording = false;
      //this.isCameraOpen = false;
      if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
        this.mediaRecorder.stop();
        this.mediaStream.getTracks().forEach((track) => track.stop());
        this.$refs.videoElement.srcObject = null;
      }
    },
/*
    downloadVideo() {
      const blob = new Blob(this.chunks, {type: 'video/webm'});
      const url = URL.createObjectURL(blob);

      const a = document.createElement('a');
      a.href = url;
      a.download = 'recorded-video.webm';
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    },
 */

    async postVideoToBackend() {
      this.isUploading = true;
      console.log(this.chunks.length);
      if (this.chunks.length === 0) {
        console.warn('录制数据为空，无法发送至后端');
        ElMessage.error('录制数据为空，上传失败');
        this.isUploading = false;
        return;
      }

      try {
        const blob = new Blob(this.chunks, {type: 'video/webm'});
        const formData = new FormData();
        formData.append('video', blob, 'recorded-video.webm');

        // 使用fetch API将数据POST到后端
        const response = await fetch('http://192.168.31.23:8080/upload-video', {
          method: 'POST',
          body: formData,
        });
        if (response.ok) {
          console.log('视频上传成功！');
          ElMessage({
            message: '视频已成功上传',
            type: 'success',
          });
          this.isUploading = false;
          this.isCameraOpen = false;
          this.allowNextStep = true;
          // 清空chunks数组，准备进行下一次录制
          this.chunks = [];
        } else {
          ElMessage.error('视频上传失败');
          console.error('视频上传失败：', response.statusText);
          this.isUploading = false;
        }
      } catch (error) {
        ElMessage.error('视频上传失败');
        console.error('视频上传出错：', error);
        this.isUploading = false;
      }
    }
  }
}
</script>

<style scoped>
@import "@/components/stylesheet/steps/step-2-watch.css";
</style>