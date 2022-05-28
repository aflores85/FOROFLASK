import {createRouter, createWebHistory} from "vue-router";
import testComp from '../components/testComp.vue';
let routes = [{path:'/',name:'home',component:testComp}];
let router = createRouter({history:createWebHistory(process.env.BASE_URL),routes});
export default router;
