import { createPinia } from 'pinia'
import { createPersistedState } from 'pinia-plugin-persistedstate'

const pinia = createPinia()

// 添加持久化插件
pinia.use(createPersistedState({
  storage: localStorage
}))

export default pinia