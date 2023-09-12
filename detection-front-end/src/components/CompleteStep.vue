<template>
  <div class="main-container">
    <div class="left">
      <img :src="this.illustrationSrc" class="main-img" />
    </div>
    <div class="mid">
      <div class="guide-text-title">
        您已完成{{ this.currentStepName }}测试
      </div>
      <div class="guide-text">
        您的下一项测试为{{ this.nextStepName }}，在您准备好时，请点击下方按钮进入测试页面
      </div>
      <button class="next-step-button" @click="toNextPage">开始下一项测试</button>
    </div>
    <div class="right">
      <img src="../assets/setting-pic/complete-img-right1.png" class="right-img"/>
    </div>
  </div>
</template>

<script>
import {getImageUrl} from "@/utils.js";

export default {
  name: "CompleteStep",
  setup(){
    function getImage(url) {
      return getImageUrl(url);
    }

    return {
      getImage
    }
  },
  data(){
    return{
      currentStep: '1',
      illustrationSrc: '',
      currentStepName: '',
      nextStepName: '',
      nextPageRoute: '/2_watch',
    }
  },
  methods:{
    calculateAttributes(){
      switch (this.currentStep){
        case "1":
          this.currentStepName = '量表填写';
          this.nextStepName = '情绪图片观看';
          this.nextPageRoute = '/2_watch';
          break;
        case "2":
          this.currentStepName = '情绪图片观看';
          this.nextStepName = '文字朗读';
          this.nextPageRoute = '/3_read';
          break;
        case "3":
          this.currentStepName = '文字朗读';
          this.nextStepName = '人脸图片描述';
          this.nextPageRoute = '/4_describe';
          break;
        case "4":
          this.currentStepName = '人脸图片描述';
          this.nextStepName = '机器人访谈';
          this.nextPageRoute = '/5_robot_interview';
          break;
        default:
          this.currentStepName = '量表填写';
          this.nextStepName = '情绪图片观看';
          this.nextPageRoute = '/2_watch_pic';
          break;
      }
    },
    toNextPage(){
      this.$router.push(this.nextPageRoute);
    }
  },
  mounted() {
    this.currentStep = this.$route.query.currentPage;
    this.illustrationSrc = this.getImage(`./assets/setting-pic/complete-img-${this.currentStep}.png`);
    this.calculateAttributes();
  }
}
</script>

<style scoped>
@import "@/components/stylesheet/complete.css";
</style>