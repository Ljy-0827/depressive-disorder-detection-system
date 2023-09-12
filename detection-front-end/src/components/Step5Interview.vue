<template style="padding: 0">
  <div class="mask" v-loading="isUploading"
       element-loading-text="请稍等，视频正在上传中" v-if="isUploading" >
  </div>
  <div class="top-container">
    <div class="top-banner">
      <img class="top-banner-pic" src="../assets/setting-pic/page-banner.png" alt="" />
    </div>
    <div class="step-bar-container">
      <el-steps :active="5" align-center>
        <el-step title="量表填写" />
        <el-step title="情绪图片观看" />
        <el-step title="文字朗读" />
        <el-step title="人脸图片描述" />
        <el-step title="机器人访谈" />
      </el-steps>
    </div>
    <div class="title-box">
      <div class="page-title">机器人访谈</div>
      <div class="page-description">请您认真观看屏幕上的图片，观看时，将视线集中在屏幕中央</div>
    </div>
  </div>
  <div class="bottom-container">
    <div class="main-emotion-pic-container">
      <div class="question-box">
        <div class="question-text">
          {{interview[this.count]}}
        </div>
      </div>
      <button class="begin-watching-button" @click="startRecording" v-show="!this.isRecording">开始回答</button>
      <button class="begin-watching-button" @click="stopRecording" v-show="this.isRecording">结束作答</button>
    </div>
    <div class="camera-container">
      <button class="open-camera-button" v-if="!isCameraOpen" @click="openCamera">打开摄像头</button>
      <video ref="videoElement" autoplay class="camera" v-if="isCameraOpen" muted></video>
    </div>
  </div>

</template>

<script>
import { interview, getImageUrl } from "@/utils.js";
import { ElMessage } from 'element-plus'

export default {
  name: "Step2Watch",
  data() {
    return {
      interview,
      count: 0,
      questionNum: -1,
      isCameraOpen: false,
      isRecording: false,
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
  mounted() {
    this.questionNum = this.interview.length;
  },
  methods: {

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
      if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
        this.mediaRecorder.stop();
        if(this.count < this.questionNum){
          setTimeout(this.postVideoToBackend, 1000);
        }
      }
    },

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
        formData.append('video', blob, `interview-video-${this.count + 1}.webm`);

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
          this.count++;
          this.isUploading = false;
          // 清空chunks数组，准备进行下一次录制
          this.chunks = [];
          if(this.count === this.questionNum){
            this.$router.push('/all_complete');
          }
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
@import "@/components/stylesheet/steps/step-5-interview.css";
</style>