import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
// 引入插件
import 'lib-flexible/flexible.js'

import './mock/index.js'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
