<template>
  <div class="top-container">
    <img class="banner-pic" src="../assets/setting-pic/result-banner.png" />
    <div class="top-content-box">
      <div class="dashboard-title">
        <button class="back-button">
          <i class="bi bi-house-door" id="back-icon"></i>
        </button>
        <div class="dashboard-title-text">
          检测结果
        </div>
      </div>
      <div class="primary-box">
        <div class="primary-box-left" id="primary-box-left">
          <div class="primary-box-title">抑郁症程度测评结果</div>
          <div class="primary-box-content">
            <img class="pie-chart" :src="imgURLs[1]" />
            <div class="primary-score">{{this.score}}</div>
            <div class="primary-inner-group" id="inner-group-left">
              <div class="primary-inner-group-title">抑郁症指数</div>
              <div class="primary-inner-group-content">{{this.score}}/100</div>
              <button class="primary-inner-group-button">评分
                <i class="bi bi-question-circle"></i>
              </button>
            </div>
            <div class="primary-inner-group">
              <div class="primary-inner-group-title">抑郁症级别</div>
              <div class="primary-inner-group-content" id="grade-text">{{ this.grade }}</div>
              <button class="primary-inner-group-button">级别
                <i class="bi bi-question-circle"></i>
              </button>
            </div>
            <div class="primary-inner-group">
              <div class="primary-inner-group-title">诊断</div>
              <div class="primary-inner-group-content" id="comment-text">{{ this.comment }}</div>
            </div>
          </div>
        </div>
        <div class="primary-box-right">
          <div class="primary-box-title">抑郁症程度测评解析</div>
          <div class="primary-box-content">
            <div class="primary-explanation-text">{{ this.exactExplanation }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="bottom-container">
      <div class="result-box" id="result-box-left">
        <div class="result-box-title">量表填写测评数据</div>
        <img class="bar-chart" :src="imgURLs[0]" />
        <div class="item-row">
          <div class="legend">
            <div class="legend-row">
              <div class="legend-item-icon" id="legend-item-icon-1"></div>
              <div class="legend-item-text">{{this.legend1Score}}分</div>
              <div class="legend-item-icon" id="legend-item-icon-2"></div>
              <div class="legend-item-text">{{this.legend2Score}}分</div>
            </div>
            <div class="legend-row">
              <div class="legend-item-icon" id="legend-item-icon-3"></div>
              <div class="legend-item-text">{{this.legend3Score}}分</div>
              <div class="legend-item-icon" id="legend-item-icon-4"></div>
              <div class="legend-item-text">{{this.legend4Score}}分</div>
            </div>
          </div>
          <div class="questionnaire-score">
            <div class="questionnaire-score-item">
              量表测评单项分数：
              <div class="questionnaire-score-digit">{{this.questionnaireSingleScore}}</div>
            </div>
            <div class="questionnaire-score-item">
              折合计入总测评分数：
              <div class="questionnaire-score-digit">{{this.questionnaireTotalScore}}</div>
            </div>
          </div>
        </div>
      </div>
      <div class="result-box" id="result-box-right">
        <div class="result-box-title">情绪图片观看测评数据</div>
        <img class="flow-chart" :src="imgURLs[2]" />
      </div>
  </div>

</template>

<script>
import {explanation, ipAddress} from "@/utils.js";
import JSZip from 'jszip';

export default {
  name: "ResultDashboard",
  data(){
    return{
      score: 68,
      grade: '中度抑郁',
      comment: '建议就医',
      explanation,
      exactExplanation: explanation.mid,
      legend1Score: 1,
      legend2Score: 2,
      legend3Score: 3,
      legend4Score: 4,
      questionnaireSingleScore: 27,
      questionnaireTotalScore: 27,
      imgURLs:[],
    }
  },
  methods:{
    async fetchAndRenderImages() {
      try {
        const response = await fetch(`http://${ipAddress}/dashboard-result`);
        if (response.ok) {
          const zipData = await response.arrayBuffer();
          const zip = await JSZip.loadAsync(zipData);
          const imageUrls = [];
          await Promise.all(
              Object.values(zip.files).map(async (file) => {
                const blobData = await file.async('blob');
                const imageUrl = URL.createObjectURL(blobData);
                imageUrls.push(imageUrl);
              })
          );

          this.imgURLs = imageUrls;
        } else {
          console.error('获取图片失败');
        }
      } catch (error) {
        console.error('获取图片失败：', error);
      }
    }
  },
  async mounted() {
    await this.fetchAndRenderImages();
    console.log(this.imgURLs);
  }
}
</script>

<style scoped>
@import "@/components/stylesheet/result-dashboard.css";
</style>