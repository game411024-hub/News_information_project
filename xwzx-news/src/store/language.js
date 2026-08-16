import { defineStore } from 'pinia';

export const useLanguageStore = defineStore('language', {
  state: () => ({
    currentLanguage: localStorage.getItem('language') || 'zh-CN', // 默认中文
  }),
  
  getters: {
    getCurrentLanguage: (state) => state.currentLanguage,
  },
  
  actions: {
    setLanguage(language) {
      this.currentLanguage = language;
      localStorage.setItem('language', language);
    },
  }
});