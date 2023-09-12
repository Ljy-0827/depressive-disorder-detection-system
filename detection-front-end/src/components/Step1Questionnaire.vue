<template>
  <div class="mask" v-loading="isUploading"
       element-loading-text="请稍等，数据正在上传中" v-if="isUploading" >
  </div>
  <div class="top-container">
    <div class="top-banner">
      <img class="top-banner-pic" src="../assets/setting-pic/page-banner.png" alt="" />
    </div>
    <div class="step-bar-container">
      <el-steps :active="1" align-center>
        <el-step title="量表填写" />
        <el-step title="情绪图片观看" />
        <el-step title="文字朗读" />
        <el-step title="人脸图片描述" />
        <el-step title="机器人访谈" />
      </el-steps>
    </div>
    <div class="title-box">
      <div class="page-title">量表填写</div>
      <div class="page-description">在过去的两周里, 你生活中以下症状出現的频率有多少？选择你认为最合适的一个选项。</div>
    </div>
  </div>
  <div class="bottom-container">
    <el-scrollbar class="scroll-container" always>
      <el-form :model="questionnaire" label-position="top">
        <div class="question-wrapper" v-for="(item, index) in questionnaire" >
          <div class="question-index">{{index +1}}.</div>
          <el-form-item  :label="item.question" required>
            <el-radio-group  v-model="this.answer[index]">
              <el-radio v-for="option in item.options" :label="option">
              </el-radio>
            </el-radio-group>
          </el-form-item>
        </div>

      </el-form>
    </el-scrollbar>
    <button class="complete-button" @click="submitForm">完成填写</button>
  </div>
</template>

<script>
import {questionnaire, ipAddress} from "@/utils.js";
import {ElMessage} from "element-plus";

export default {
  name: "Step1Questionnaire",
  data(){
    return{
      questionnaire,
      answer:[],
      isUploading: false,
    }
  },
  methods:{
    postDataToBackend(){
      console.log(this.answer)
      fetch(`http://${ipAddress}/upload-answer`, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(this.answer),
      })
      .then(response => {
        if (response.ok) {
          console.log('JSON data sent successfully!');
          this.isUploading = false;
          this.$router.push({name: 'step-complete', query: {currentPage: '1'}});
        } else {
          console.error('Failed to send JSON data to backend.');
        }
      })
      .catch(error => {
        console.error('An error occurred while sending JSON data:', error);
      });
    },

    submitForm() {
      if(this.answer.length === this.questionnaire.length){
        ElMessage({
          message: '量表填写完成',
          type: 'success',
        });
        this.isUploading = true;
        setTimeout(this.postDataToBackend,1000);

      } else{
        ElMessage.error('请您作答全部题目');
      }
    }
  }
}
</script>

<style scoped>
@import "@/components/stylesheet/steps/step-1-questionnaire.css";
</style>