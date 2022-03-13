import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
    {
        path: '/',
        component: () => import('../views/Uploader.vue')
    },
    {
        path: '/imageList',
        component: () => import('../views/ImageList.vue')
    },
    {
        path: '/settings',
        component: () => import('../views/Settings.vue')
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
})

export default router