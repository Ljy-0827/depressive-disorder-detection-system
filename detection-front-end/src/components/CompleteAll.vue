<template>
  <div class="main-container">
    <div class="left">
      <img :src="this.illustrationSrc" class="main-img" />
    </div>
    <div class="mid">
      <div class="guide-text-title">
        您已完成全部测试环节
      </div>
      <div class="guide-text">
        您的所有测试数据都已成功上传并完成分析，您可以点击下方按钮查看您的详细检测报告
      </div>
      <button class="next-step-button" >查看检测报告</button>
    </div>
    <div class="right">
      <img src="../assets/setting-pic/complete-img-right1.png" class="right-img"/>
    </div>
  </div>
</template>

<script>
import {getImageUrl} from "@/utils.js";

export default {
  name: "CompleteAll",
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
      illustrationSrc: '',
    }
  },
  methods:{
    toNextPage(){

    }
  },
  mounted() {
    this.illustrationSrc = this.getImage(`./assets/setting-pic/complete-img-5.png`);
  }
}
</script>

<style scoped>
@import "@/components/stylesheet/complete.css";
</style>