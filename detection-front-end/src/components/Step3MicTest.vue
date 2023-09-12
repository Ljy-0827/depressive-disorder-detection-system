<template>
<div class="view-container">
  <div class="box-container">
    <div class="box-text">
      点击按钮测试麦克风，确认设备正确连接且声音正常后，点击开始检测
    </div>
    <button class="box-button-primary" id="open-mic" @click="startRecording" v-if="isAllowRecord">打开麦克风并开始录制</button>
    <button class="box-button-primary" id="stop-record" @click="stopRecording" v-if="isAllowStop">停止录制</button>
    <div class="box-button-group" v-if="isTesting">
      <button class="box-button-ghost" id="play-audio" v-if="audioUrl && !isPlaying" @click="playAudio">播放录音</button>
      <button class="box-button-ghost" id="stop-audio" v-if="audioUrl && isPlaying" @click="stopAudio">停止播放</button>
      <button class="box-button-ghost" id="try-again" @click="testAgain">重新测试</button>
      <button class="box-button-primary" id="finish" @click="this.$router.push('/3_read/main_test')">完成设备检查并开始检测</button>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: "Step3MicTest",
  data(){
    return{
      isAllowRecord: true,
      isRecording: false,
      isAllowStop: false,
      isTesting: false,
      isPlaying: false,
      audioChunks: [],
      audioUrl: null,
      mediaRecorder: null,
      audioElement: null,
    }
  },
  methods:{
    startRecording() {
      navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        this.isRecording = true;
        this.isAllowRecord = false;
        this.isAllowStop = true;
        this.isTesting = false;
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
      });
    },

    stopRecording() {
      if (this.mediaRecorder && this.isRecording) {
        this.mediaRecorder.stop();
      }
      this.isTesting = true;
      this.isAllowStop = false;
      this.isAllowRecord = false;
    },

    playAudio() {
      if (this.audioUrl && !this.isPlaying) {
        this.audioElement = new Audio(this.audioUrl);
        this.audioElement.addEventListener("ended", () => {
          this.isPlaying = false;
        });
        this.audioElement.play();
        this.isPlaying = true;
      }
    },

    stopAudio() {
      if (this.audioElement && this.isPlaying) {
        this.audioElement.pause();
        this.isPlaying = false;
      }
    },

    testAgain(){
      this.isAllowRecord = true;
      this.isRecording = false;
      this.isAllowStop = false;
      this.isTesting = false;
      this.isPlaying = false;
      this.audioChunks = [];
      this.audioUrl = null;
      this.mediaRecorder = null;
      this.audioElement = null;
    },

  }
}
</script>

<style scoped>
@import "@/components/stylesheet/steps/step-3-mic-test.css";
</style>