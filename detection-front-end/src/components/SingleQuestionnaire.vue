<template>
  <div class="mask" v-loading="isUploading"
       element-loading-text="请稍等，数据正在上传中" v-if="isUploading" >
  </div>
  <div class="top-container">
    <div class="top-banner">
      <img class="top-banner-pic" src="../assets/setting-pic/page-banner-small.png" alt="" />
    </div>
    <button class="back-button" @click="backToHomePage">
      <i class="bi bi-chevron-left" id="back-icon"></i>
    </button>
    <div class="title-box">
      <div class="page-title">量表填写</div>
      <div class="page-description">在过去的两周里, 你生活中以下症状出現的频率有多少？选择你认为最合适的一个选项。</div>
    </div>
  </div>
  <div class="bottom-container">
    <el-scrollbar class="scroll-container" always>
      <el-form :model="questionnaire" label-position="top">
        <div class="question-wrapper" v-for="(item, index) in questionnaire" >
          <div class="question-index">{{index + 1}}.</div>
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
  name: "SingleQuestionnaire",
  data(){
    return{
      questionnaire,
      answer: [],
      is1Complete: false,
      isUploading: false,
    }
  },
  methods:{
    backToHomePage(){
      this.$router.push('/');
    },

    updateStatus(){
      fetch(`http://${ipAddress}/update_status`, {
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({is1Complete: this.is1Complete}),
      })
      .then(response => {
        if (response.ok) {
          console.log('Data sent successfully!');
        } else {
          console.error('Failed to send data to backend.');
        }
      })
      .catch(error => {
        console.error('An error occurred while sending data:', error);
      });
    },

    postDataToBackend(){
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
          this.$router.push({name: 'single-complete', query: {currentPage: '1'}});
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
        this.is1Complete = true;
        this.updateStatus();
        setTimeout(this.postDataToBackend,1000);

      } else{
        ElMessage.error('请您作答全部题目');
      }
    }
  }
}
</script>

<style scoped>
@import "./stylesheet/singles/single-questionnaire.css";
</style>