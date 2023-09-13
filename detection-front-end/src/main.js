import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router';

import App from './App.vue';
import ElementPlus from 'element-plus';
import zhCn from 'element-plus/es/locale/lang/zh-cn';
import 'element-plus/dist/index.css';
import * as ElementPlusIconsVue from '@element-plus/icons-vue';
import "bootstrap-icons/font/bootstrap-icons.css";
import LandingPage from "@/components/LandingPage.vue";
import SingleQuestionnaire from "@/components/SingleQuestionnaire.vue";
import CompleteStep from "@/components/CompleteStep.vue";
import Step3MicTest from "@/components/Step3MicTest.vue";
import Step3MainTest from "@/components/Step3MainTest.vue";
import Step3General from "@/components/Step3General.vue";
import Step1Questionnaire from "@/components/Step1Questionnaire.vue";
import Step2Watch from "@/components/Step2Watch.vue";
import Step4Describe from "@/components/Step4Describe.vue";
import Step5Interview from "@/components/Step5Interview.vue";
import CompleteAll from "@/components/CompleteAll.vue";
import CompleteSingle from "@/components/CompleteSingle.vue";
import SingleWatch from "@/components/SingleWatch.vue";
import ResultDashboard from "@/components/ResultDashboard.vue";
import ResultPage from "@/components/ResultPage.vue";
import ResizedStep1 from "@/components/ResizedStep1.vue";
import ResizedStep2 from "@/components/ResizedStep2.vue";
import ResizedLandingPage from "@/components/ResizedLandingPage.vue";

const myRouter = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'landing-page',
            component: ResizedLandingPage
        },
        {
            path: '/index',
            name: 'home-page',
            component: LandingPage
        },
        {
            path: '/questionnaire',
            name: 'questionnaire',
            component: SingleQuestionnaire,
        },
        {
            path: '/2_watch',
            name: '2-watch',
            component: Step2Watch,
        },
        {
            path: '/watch',
            name: 'watch',
            component: SingleWatch,
        },
        {
            path: '/1_questionnaire',
            name: '1-questionnaire',
            component: Step1Questionnaire,
        },
        {
            path: '/4_describe',
            name: '4-describe',
            component: Step4Describe,
        },
        {
            path: '/5_interview',
            name: '5-interview',
            component: Step5Interview,
        },
        {
            path: '/step_complete',
            name: 'step-complete',
            component: CompleteStep,
        },
        {
            path: '/all_complete',
            name: '/all-complete',
            component: CompleteAll,
        },
        {
            path: '/single_complete',
            name: 'single-complete',
            component: CompleteSingle,
        },
        {
            path: '/result_dashboard',
            name: 'result-dashboard',
            component: ResultDashboard,
        },
        {
            path:'/result',
            name: 'result',
            component: ResultPage,
        },
        {
            path: '/1',
            name: 'resized-step1',
            component: ResizedStep1,
        },
        {
            path: '/2',
            name: 'resized-step2',
            component: ResizedStep2,
        },

        {
            path: '/3_read',
            name: 'read',
            component: Step3General,
            children:[
                {
                    path: '',
                    name: 'mic-test',
                    component: Step3MicTest,
                },
                {
                    path: 'main_test',
                    name: 'main-test',
                    component: Step3MainTest,
                }
            ]
        }
    ]
})

const myApp = createApp(App)

myApp.use(myRouter)

myApp.mount('#app')

myApp.use(ElementPlus, {
    locale: zhCn,
})

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    myApp.component(key, component)
}
