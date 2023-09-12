<template>
  <div class="top-container">
    <div class="top-banner">
      <img class="top-banner-pic" src="../assets/setting-pic/page-banner.png" alt="" />
    </div>
    <div class="step-bar-container">
      <el-steps :active="3" align-center>
        <el-step title="量表填写" />
        <el-step title="情绪图片观看" />
        <el-step title="文字朗读" />
        <el-step title="人脸图片描述" />
        <el-step title="机器人访谈" />
      </el-steps>
    </div>
    <div class="title-box">
      <div class="page-title">文字朗读</div>
      <div class="page-description">请您大声朗读屏幕上的两段短文</div>
    </div>
  </div>
  <RouterView class="bottom-container">

  </RouterView>
</template>

<script>
export default {
  name: "Step3General",
  data() {
    return {
      isRecording: false,
      audioChunks: [],
      audioUrl: null,
      mediaRecorder: null,
    };
  },
  methods: {

  },
}
</script>

<style scoped>
@import "@/components/stylesheet/steps/step-3-general.css";
</style>