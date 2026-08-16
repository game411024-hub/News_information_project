import { defineStore } from 'pinia';
import axios from 'axios';
import { apiConfig } from '../config/api';

export const useUserStore = defineStore('user', {
  state: () => ({
    userInfo: null,
    token: '',
    isLogin: false,
    userBio: '这是我的个人简介'
  }),
  
  getters: {
    getUserInfo: (state) => state.userInfo,
    getToken: (state) => state.token,
    getLoginStatus: (state) => state.isLogin,
    getUserBio: (state) => state.userInfo?.bio || state.userBio
  },
  
  actions: {
    async login(userData) {
      try {
        // 发送登录请求
        const response = await axios.post(`${apiConfig.baseURL}/api/user/login`, {
          username: userData.username,
          password: userData.password
        });
        
        // 检查响应状态
        if (response.data && response.data.code === 200) {
          // 登录成功
          const userInfo = response.data.data.userInfo;
          const token = response.data.data.token;
          
          this.userInfo = userInfo;
          this.token = token;
          this.isLogin = true;
          
          return {
            success: true,
            message: '登录成功'
          };
        } else {
          // 登录失败
          return {
            success: false,
            message: response.data.message || '登录失败'
          };
        }
      } catch (error) {
        console.error('登录请求失败:', error);
        return {
          success: false,
          message: error.response?.data?.message || '登录请求失败，请稍后再试'
        };
      }
    },
    
    async register(userData) {
      try {
        // 发送注册请求
        const response = await axios.post(`${apiConfig.baseURL}/api/user/register`, {
          username: userData.username,
          password: userData.password
        });
        
        // 检查响应状态
        if (response.data && response.data.code === 200) {
          // 注册成功，自动登录
          const userInfo = response.data.data.userInfo;
          const token = response.data.data.token;
          
          this.userInfo = userInfo;
          this.token = token;
          this.isLogin = true;
          
          return {
            success: true,
            message: '注册成功'
          };
        } else {
          // 注册失败
          return {
            success: false,
            message: response.data.message || '注册失败'
          };
        }
      } catch (error) {
        console.error('注册请求失败:', error);
        return {
          success: false,
          message: error.response?.data?.message || '注册请求失败，请稍后再试'
        };
      }
    },
    
    logout() {
      this.userInfo = null;
      this.token = '';
      this.isLogin = false;
    },
    
    // 获取用户信息
    async getUserInfoDetail() {
      try {
        // 检查是否有token
        if (!this.token) {
          return {
            success: false,
            message: '未登录'
          };
        }
        
        // 发送获取用户信息请求
        const response = await axios.get(`${apiConfig.baseURL}/api/user/info`, {
          headers: {
            // Authorization: `Bearer ${this.token}`
            Authorization: this.token
          }
        });
        
        // 检查响应状态
        if (response.data && response.data.code === 200) {
          // 更新用户信息
          this.userInfo = response.data.data;
          
          return {
            success: true,
            message: '获取用户信息成功',
            data: response.data.data
          };
        } else {
          return {
            success: false,
            message: response.data.message || '获取用户信息失败'
          };
        }
      } catch (error) {
        console.error('获取用户信息请求失败:', error);
        return {
          success: false,
          message: error.response?.data?.message || '获取用户信息请求失败，请稍后再试'
        };
      }
    },
    
    // 更新个人简介
    async updateUserBio(bio) {
      try {
        // 检查是否有token
        if (!this.token) {
          return {
            success: false,
            message: '未登录'
          };
        }
        
        // 发送更新个人简介请求
        const response = await axios.put(`${apiConfig.baseURL}/api/user/update`, 
          { bio },
          {
            headers: {
              Authorization: this.token
            }
          }
        );
        
        // 检查响应状态
        if (response.data && response.data.code === 200) {
          // 更新本地用户简介
          this.userInfo.bio = bio;
          
          return {
            success: true,
            message: '更新个人简介成功'
          };
        } else {
          return {
            success: false,
            message: response.data.message || '更新个人简介失败'
          };
        }
      } catch (error) {
        console.error('更新个人简介请求失败:', error);
        return {
          success: false,
          message: error.response?.data?.message || '更新个人简介请求失败，请稍后再试'
        };
      }
    },
    
    // 修改密码
    async updatePassword(oldPassword, newPassword) {
      try {
        // 检查是否有token
        if (!this.token) {
          return {
            success: false,
            message: '未登录'
          };
        }
        
        // 发送修改密码请求
        const response = await axios.put(`${apiConfig.baseURL}/api/user/password`, 
          { 
            oldPassword,
            newPassword 
          },
          {
            headers: {
              Authorization: this.token
            }
          }
        );
        
        // 检查响应状态
        if (response.data && response.data.code === 200) {
          return {
            success: true,
            message: '密码修改成功'
          };
        } else {
          return {
            success: false,
            message: response.data.message || '密码修改失败'
          };
        }
      } catch (error) {
        console.error('修改密码请求失败:', error);
        return {
          success: false,
          message: error.response?.data?.message || '修改密码请求失败，请稍后再试'
        };
      }
    }
  },
  
  // 添加持久化配置
  persist: {
    enabled: true,
    strategies: [
      {
        key: 'user-store',
        storage: localStorage
      }
    ]
  }
});