<template>
  <div class="history-container">
    <van-nav-bar
      title="浏览历史"
      left-text="返回"
      left-arrow
      @click-left="onClickLeft"
      right-text="清空"
      @click-right="onClickClear"
      fixed
    />
    
    <div class="history-list" v-if="historyStore.getHistory.length">
      <div class="history-item" v-for="item in historyStore.getHistory" :key="item.id">
        <van-cell @click="goToNewsDetail(item.id)" :border="false">
          <template #title>
            <div class="news-item">
              <div class="news-image" v-if="item.image">
                <img :src="item.image" :alt="item.title">
              </div>
              <div class="news-info">
                <div class="news-title">{{ item.title }}</div>
                <div class="news-meta">
                  <span>{{ item.author }}</span>
                  <span>{{ item.publishTime }}</span>
                  <span>浏览时间: {{ item.viewTime }}</span>
                </div>
              </div>
            </div>
          </template>
        </van-cell>
        <van-button 
          class="delete-btn" 
          type="danger" 
          size="mini" 
          icon="cross"
          @click="confirmDelete(item.id)"
        ></van-button>
      </div>
    </div>
    
    <van-empty v-else description="暂无浏览历史" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useHistoryStore } from '../store/modules/history';
import { showDialog } from 'vant';

const router = useRouter();
const historyStore = useHistoryStore();

// 返回上一页
const onClickLeft = () => {
  router.back();
};

// 跳转到新闻详情
const goToNewsDetail = (id) => {
  router.push(`/news/detail/${id}`);
};

// 删除单条历史记录
const removeHistory = async (id) => {
  try {
    const result = await historyStore.removeHistoryApi(id);
    console.log('删除单条历史记录结果:', result);
    
    // 如果API请求失败且不是本地操作，则显示错误提示
    if (!result.success && !result.isLocal) {
      showDialog({
        title: '提示',
        message: result.message || '删除失败，请稍后重试',
      });
    }
  } catch (error) {
    console.error('删除历史记录失败:', error);
    // 出错时仍然尝试本地删除
    // historyStore.removeHistory(id);
  }
};

// 确认删除
const confirmDelete = (id) => {
  showDialog({
    title: '提示',
    message: '确定要删除这条浏览记录吗？',
    showCancelButton: true,
  }).then((action) => {
    if (action === 'confirm') {
      removeHistory(id);
    }
  });
};

// 清空历史记录
const onClickClear = async () => {
  showDialog({
    title: '提示',
    message: '确定要清空所有浏览历史吗？',
    showCancelButton: true,
  }).then(async (action) => {
    if (action === 'confirm') {
      try {
        const result = await historyStore.clearHistoryApi();
        console.log('清空历史记录结果:', result);
        
        // 如果API请求失败且不是本地操作，则显示错误提示
        if (!result.success && !result.isLocal) {
          showDialog({
            title: '提示',
            message: result.message || '清空失败，请稍后重试',
          });
        }
      } catch (error) {
        console.error('清空历史记录失败:', error);
        // 出错时仍然尝试本地清空
        // historyStore.clearHistory();
      }
    }
  });
};

// 组件挂载时加载历史记录
onMounted(async () => {
  // 先尝试从API获取浏览历史
  try {
    const result = await historyStore.getHistoryListApi();
    console.log('浏览历史页面：API获取结果', result);
    
    // 如果API请求失败或用户未登录，则从本地加载
    if (!result || !result.success) {
      historyStore.loadHistory();
    }
  } catch (error) {
    console.error('浏览历史页面：API请求异常', error);
    // 出错时从本地加载
    historyStore.loadHistory();
  }
});
</script>

<style scoped>
.history-container {
  padding-top: 46px;
  padding-bottom: 20px;
  background-color: #f7f8fa;
  min-height: 100vh;
}

.history-list {
  padding: 10px;
}

.news-item {
  display: flex;
  padding: 10px 0;
}

.news-image {
  width: 120px;
  height: 80px;
  margin-right: 12px;
  flex-shrink: 0;
}

.news-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 4px;
}

.news-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.news-title {
  font-size: 16px;
  font-weight: bold;
  line-height: 1.4;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.news-meta {
  font-size: 12px;
  color: #999;
  display: flex;
  flex-wrap: wrap;
}

.news-meta span {
  margin-right: 10px;
}

.delete-button {
  width: 20px;
  height: 20px;
  background-color: #ee0a24;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 10px;
}

.delete-btn {
  height: 100%;
  width: 65px;
}

.van-swipe-cell {
  margin-bottom: 8px;
}

.history-item {
  position: relative;
  margin-bottom: 10px;
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.delete-btn {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  z-index: 10;
  width: 24px;
  height: 24px;
  padding: 0;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.delete-icon {
  position: absolute;
  top: 50%;
  right: 15px;
  transform: translateY(-50%);
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f2f3f5;
  border-radius: 50%;
  z-index: 2;
}
</style>