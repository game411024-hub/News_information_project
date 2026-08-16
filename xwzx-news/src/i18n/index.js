import { createI18n } from 'vue-i18n';
import zhCN from './locales/zh-CN.js';
import enUS from './locales/en-US.js';

// 创建i18n实例
export function setupI18n() {
  // 在创建i18n实例前获取语言设置
  const savedLanguage = localStorage.getItem('language') || 'zh-CN';
  
  const i18n = createI18n({
    legacy: false, // 使用组合式API
    locale: savedLanguage,
    fallbackLocale: 'zh-CN',
    messages: {
      'zh-CN': zhCN,
      'en-US': enUS
    }
  });
  
  return i18n;
}

// 动态切换语言
export function setI18nLanguage(i18n, locale) {
  if (i18n.mode === 'legacy') {
    i18n.global.locale = locale;
  } else {
    i18n.global.locale.value = locale;
  }
  document.querySelector('html').setAttribute('lang', locale);
}