import { defineStore } from 'pinia';
import axios from 'axios';
import { useUserStore } from '../user';
import { apiConfig } from '../../config/api';

export const useHistoryStore = defineStore('history', {
  state: () => ({
    history: [],
  }),
  
  getters: {
    getHistory: (state) => state.history,
  },
  
  actions: {
    // 添加浏览历史 - API请求
    async addHistoryApi(newsId) {
      const userStore = useUserStore();
      
      // 检查用户是否登录
      if (!userStore.getLoginStatus) {
        return { success: false, message: '请先登录' };
      }
      
      try {
        const response = await axios.post(`${apiConfig.baseURL}/api/history/add`, 
          { newsId },
          { 
            headers: { 
              Authorization: userStore.token 
            } 
          }
        );
        
        if (response.data.code === 200) {
          return { success: true, data: response.data.data };
        } else {
          return { success: false, message: response.data.message || '添加浏览历史失败' };
        }
      } catch (error) {
        console.error('添加浏览历史请求失败:', error);
        return { success: false, message: '网络请求失败' };
      }
    },
    
    // 添加浏览历史 - 本地
    addHistory(news) {
      // 检查是否已存在相同ID的新闻
      const existingIndex = this.history.findIndex(item => item.id === news.id);
      
      // 如果已存在，先删除旧记录
      if (existingIndex !== -1) {
        this.history.splice(existingIndex, 1);
      }
      
      // 添加到历史记录的最前面（最新浏览的在最前面）
      this.history.unshift({
        ...news,
        viewTime: new Date().toLocaleString()
      });
      
      // 限制历史记录数量，最多保存50条
      if (this.history.length > 50) {
        this.history.pop();
      }
      
      // 保存到本地存储
      this.saveHistory();
    },
    
    // 清空浏览历史
    clearHistory() {
      this.history = [];
      this.saveHistory();
    },
    
    // 清空浏览历史 - API请求
    async clearHistoryApi() {
      const userStore = useUserStore();
      
      // 检查用户是否登录
      if (!userStore.getLoginStatus) {
        console.log('清空浏览历史API：用户未登录，使用本地操作');
        this.clearHistory();
        return { success: true, isLocal: true };
      }
      
      try {
        console.log('清空浏览历史API：开始请求');
        const response = await axios.delete(`${apiConfig.baseURL}/api/history/clear`, { 
          headers: { 
            Authorization: userStore.token 
          } 
        });
        
        if (response.data.code === 200) {
          console.log('清空浏览历史API：清空成功');
          // 更新本地历史记录
          this.clearHistory();
          return { success: true };
        } else {
          console.error('清空浏览历史API：请求失败', response.data.message);
          return { success: false, message: response.data.message || '清空浏览历史失败' };
        }
      } catch (error) {
        console.error('清空浏览历史API：请求异常', error);
        return { success: false, message: '网络请求失败' };
      }
    },
    
    // 删除单条浏览历史
    removeHistory(id) {
      this.history = this.history.filter(item => item.id !== id);
      this.saveHistory();
    },
    
    // 删除单条浏览历史 - API请求
    async removeHistoryApi(id) {
      const userStore = useUserStore();
      
      // 检查用户是否登录
      if (!userStore.getLoginStatus) {
        console.log('删除浏览历史API：用户未登录，使用本地操作');
        this.removeHistory(id);
        return { success: true, isLocal: true };
      }
      
      try {
        console.log('删除浏览历史API：开始请求', id);
        const response = await axios.delete(`${apiConfig.baseURL}/api/history/delete/${id}`, { 
          headers: { 
            Authorization: userStore.token 
          } 
        });
        
        if (response.data.code === 200) {
          console.log('删除浏览历史API：删除成功');
          // 更新本地历史记录
          this.removeHistory(id);
          return { success: true };
        } else {
          console.error('删除浏览历史API：请求失败', response.data.message);
          return { success: false, message: response.data.message || '删除浏览历史失败' };
        }
      } catch (error) {
        console.error('删除浏览历史API：请求异常', error);
        return { success: false, message: '网络请求失败' };
      }
    },
    
    // 保存到本地存储
    saveHistory() {
      localStorage.setItem('news_history', JSON.stringify(this.history));
    },
    
    // 从本地存储加载
    loadHistory() {
      const savedHistory = localStorage.getItem('news_history');
      if (savedHistory) {
        this.history = JSON.parse(savedHistory);
      }
    },
    
    // 获取浏览历史 - API请求
    async getHistoryListApi() {
      const userStore = useUserStore();
      
      // 检查用户是否登录
      if (!userStore.getLoginStatus) {
        console.log('获取浏览历史API：用户未登录，使用本地数据');
        return { success: false, message: '请先登录', isLocal: true };
      }
      
      try {
        console.log('获取浏览历史API：开始请求');
        const response = await axios.get(`${apiConfig.baseURL}/api/history/list`, { 
          headers: { 
            Authorization: userStore.token 
          } 
        });
        
        if (response.data.code === 200) {
          // 正确获取list数组
          const historyList = response.data.data.list || [];
          // console.log(`获取浏览历史API：成功获取${historyList.length}条记录`, response.data.data);
          // 更新本地历史记录
          this.history = historyList;
          // 保存到本地存储
          this.saveHistory();
          return { success: true, data: historyList };
        } else {
          // console.error('获取浏览历史API：请求失败', response.data.message);
          return { success: false, message: response.data.message || '获取浏览历史失败' };
        }
      } catch (error) {
        // console.error('获取浏览历史API：请求异常', error);
        return { success: false, message: '网络请求失败' };
      }
    },
  },
});