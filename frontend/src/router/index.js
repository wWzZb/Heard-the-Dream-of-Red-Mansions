import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import VoiceCloneUploader from '../components/VoiceCloneUploader.vue'
import CloneFrom from '@/components/CloneFrom.vue'
import Mainpage from '../views/mainpage.vue'
import RedMansions from '@/views/RedMansions.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/upload/:upload_id',
      name: 'VoiceCloneUploader',
      component: VoiceCloneUploader,
    },
    {
      path: '/mainpage',
      name: 'mainpage',
      component: Mainpage,
    },
    {
      path: '/RedMansions',
      name: 'RedMansions',
      component: RedMansions,
    },
    {
      path: '/clonefrom',
      name: 'clonefrom',
      component: CloneFrom

    },
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue'),
    // },
  ],
})

export default router
