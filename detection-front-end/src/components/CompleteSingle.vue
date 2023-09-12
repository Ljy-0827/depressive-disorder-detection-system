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
        单项测试已经结束，您可以点击"查看测试结果"按钮查看单项测试结果，或点击"返回主页"按钮浏览其他测试项目
      </div>
      <div class="button-group">
        <button class="next-step-button" @click="toResultPage">查看测试结果</button>
        <button class="back-home-button" @click="backToHomePage">返回主页</button>
      </div>
    </div>
    <div class="right">
      <img src="../assets/setting-pic/complete-img-right1.png" class="right-img"/>
    </div>
  </div>
</template>

<script>
import {getImageUrl} from "@/utils.js";

export default {
  name: "CompleteSingle",
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
      currentStepName: '量表填写',
      resultPageRoute: '/questionnaire_result',
    }
  },
  methods:{
    calculateAttributes(){
      switch (this.currentStep){
        case "1":
          this.currentStepName = '量表填写';
          this.resultPageRoute = '/questionnaire_result';
          break;
        case "2":
          this.currentStepName = '情绪图片观看';
          this.resultPageRoute = '/watch_result';
          break;
        case "3":
          this.currentStepName = '文字朗读';
          this.resultPageRoute = '/read_result';
          break;
        case "4":
          this.currentStepName = '人脸图片描述';
          this.resultPageRoute = '/describe_result';
          break;
        case "5":
          this.currentStepName = '机器人访谈';
          this.resultPageRoute = '/interview_result';
          break;
        default:
          this.currentStepName = '量表填写';
          this.resultPageRoute = '/questionnaire_result';
          break;
      }
    },
    backToHomePage(){
      this.$router.push('/');
    },
    toResultPage(){
      this.$router.push(this.resultPageRoute);
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