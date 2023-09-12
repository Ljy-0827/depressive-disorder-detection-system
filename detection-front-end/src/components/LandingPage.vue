<template>
  <div class="top-container">
    <img class="background-pic" src="../assets/setting-pic/landing-page-background.png" alt="" />
    <div class="top-box">
      <div class="text-header">抑郁症多模态识别系统</div>
      <div class="text-content">内容描述占位内容描述占位内容描述占位内容描述占位内容描述占位内容描述占位内容描述占位内容描述占位</div>
      <button class="begin-button" @click="this.$router.push('/1_questionnaire')">开始检测</button>
    </div>
  </div>
  <div class="card-container">
    <div class="card-first">
      <div class="icon-circle">
        <i class="bi bi-clipboard-data" id="icon-1"></i>
      </div>
      <div class="card-title">量表填写</div>
      <button class="card-button" @click="this.$router.push('/questionnaire')" v-show="!this.is1Complete">开始检测</button>
      <button class="card-button-complete" disabled v-show="this.is1Complete">您已完成填写</button>
      <button class="card-button-check-result" v-show="this.is1Complete">查看检测结果</button>
    </div>
    <div class="card-mid">
      <div class="icon-circle">
        <i class="bi bi-easel2" id="icon-2"></i>
      </div>
      <div class="card-title">情绪图片观看</div>
      <button class="card-button" @click="this.$router.push('/watch')" v-show="!this.is2Complete">开始检测</button>
      <button class="card-button-complete" disabled v-show="this.is2Complete">您已完成填写</button>
      <button class="card-button-check-result" v-show="this.is2Complete">查看检测结果</button>
    </div>
    <div class="card-mid">
      <div class="icon-circle">
        <i class="bi bi-mic" id="icon-3"></i>
      </div>
      <div class="card-title">文字朗读</div>
      <button class="card-button">开始检测</button>
    </div>
    <div class="card-mid">
      <div class="icon-circle">
        <i class="bi bi-person-video3" id="icon-4"></i>
      </div>
      <div class="card-title">人脸图片描述</div>
      <button class="card-button">开始检测</button>
    </div>
    <div class="card-mid">
      <div class="icon-circle">
        <i class="bi bi-robot" id="icon-5"></i>
      </div>
      <div class="card-title">机器人访谈</div>
      <button class="card-button">开始检测</button>
    </div>
  </div>
</template>

<script>
import {ipAddress} from "@/utils.js";

export default {
  name: "LandingPage",
  data(){
    return{
      is1Complete: false,
      is2Complete: false,
      is3Complete: false,
      is4Complete: false,
      is5Complete: false,
    }
  },
  mounted() {
    this.initialStatus();
  },
  methods:{
    initialStatus(){
      fetch(`http://${ipAddress}/update_status`, {
        method: 'get',
      })
          .then(x => x.json())
          .then(x => {
            console.log(x);
            this.is1Complete = x[0];
            this.is2Complete = x[1];
            this.is3Complete = x[2];
            this.is4Complete = x[3];
            this.is5Complete = x[4];
          })
    }
  }
}
</script>

<style scoped>
@import "./stylesheet/landing-page";
</style>