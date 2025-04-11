<template>
  <div class="receiver-container">
    <div class="title-text">时序预测模型数据分析与可视化</div>
    <div class="loading-container" v-if="loading">
      <a-spin :loading="loading" :size="64">
        <template #tip>
          <div :style="{ color: '#0cc0ff' }">数据正在预测中...</div>
        </template>
        <template #icon>
          <img src="@/assets/loading.svg" />
        </template>
      </a-spin>
      <a-progress :percent="fakeProgressPercent" color="#0cc0ff" :style="{ width: '50%' }" />
    </div>
    <div class="upload-container" v-if="!loading">
      <el-upload
        class="upload-area"
        drag
        accept="text/csv"
        action="#"
        :auto-upload="false"
        :show-file-list="false"
        :on-change="handleFileChange"
      >
        <div v-if="!isUploading && !csvFilename">
          <el-icon class="el-icon--upload" :size="256"><upload-filled /></el-icon>
          <div class="el-upload__text">拖拽文件或点击上传文件进行预测</div>
        </div>
        <div v-else-if="isUploading" class="progress-container">
          <div class="upload-progress-text">
            上传中...
            <div style="width: 3rem; margin-left: 1rem">{{ Math.floor(progressPercentage) }}</div>
            %
          </div>
          <el-progress :percentage="progressPercentage" :stroke-width="10" :show-text="false" />
        </div>
        <div v-else class="csv-file container-text">
          <img src="@/assets/csv-icon.svg" />
          {{ csvFilename }}
        </div>
      </el-upload>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import axios from 'axios'
import { useDataStore } from '@/stores/store'
import { UploadFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElLoading, ElMessage } from 'element-plus'
import { color } from 'echarts'

const dataStore = useDataStore()
const router = useRouter()

const loading = ref(false)

axios.defaults.baseURL = 'http://127.0.0.1:5000'
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'

const csvFilename = ref('')
const isUploading = ref(false)
const progressPercentage = ref(0)
let progressInterval = null
var fakeProgressInterval = null

// 清理进度条定时器
onUnmounted(() => {
  if (progressInterval) clearInterval(progressInterval)
})

// 导航到可视化页面
const navigateToVision = () => {
  router.push('/vision')
}

// 启动虚假进度显示
const startFakeProgress = () => {
  isUploading.value = true
  progressPercentage.value = 0.0

  // 创建匀速进度，在2秒内完成到95%
  const totalSteps = 20 // 40个步骤，每步50ms，总共1000ms
  const incrementPerStep = 95 / totalSteps

  progressInterval = setInterval(() => {
    if (progressPercentage.value < 95) {
      progressPercentage.value += incrementPerStep
    } else {
      clearInterval(progressInterval)
    }
  }, 50)
}

// 处理文件上传逻辑
const handleFileChange = async (file) => {
  if (!file || file.raw.type !== 'text/csv') {
    ElMessage.error('请上传CSV格式的文件')
    return
  }

  try {
    // 1. 启动进度条动画
    startFakeProgress()

    // 2. 准备上传数据
    const formData = new FormData()
    formData.append('csvFile', file.raw)

    // 3. 等待进度条至少显示2秒
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // 4. 发送请求
    const response = await axios.post('http://127.0.0.1:5000/process-csv', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })

    // 5. 处理响应
    if (response.status === 200) {
      // 进度条完成
      progressPercentage.value = 100

      // 处理数据
      const data = response.data
      csvFilename.value = data.csvFilename
      dataStore.setSharedData(data)

      // 延迟一下，让用户看到100%进度
      await new Promise((resolve) => setTimeout(resolve, 500))
      isUploading.value = false

      // const loadingInstance = ElLoading.service({
      //   lock: true,
      //   fullscreen: true,
      //   background: 'rgba(0, 0, 0, 0.7)',
      //   text: '正在预测/模型运行中',
      // })
      // setTimeout(() => {
      //   loadingInstance.close()
      //   navigateToVision()
      // }, 20000)
      //
      loading.value = true
      loadingProgress()
    } else {
      handleUploadError('处理CSV文件时出错')
    }
  } catch (error) {
    handleUploadError(`网络错误: ${error.message}`)
  }
}

// 处理上传错误
const handleUploadError = (message) => {
  if (progressInterval) clearInterval(progressInterval)
  isUploading.value = false
  progressPercentage.value = 0
  ElMessage.error(message)
  console.error(message)
}

// 虚拟模型运行进度条
const fakeProgressPercent = ref(0)
const loadingProgress = () => {
  fakeProgressInterval = setInterval(() => {
    fakeProgressPercent.value = Math.min(
      100,
      Math.round((fakeProgressPercent.value + 0.01) * 100) / 100,
    )
    if (fakeProgressPercent.value >= 1) {
      clearInterval(fakeProgressInterval)
      loading.value = false
      navigateToVision()
    }
  }, 100)
}
</script>

<style scoped>
.overlay {
  background-color: red;
  width: 100vw;
  height: 100vh;
  z-index: 999;
}

.receiver-container {
  width: 100vw;
  height: 100vh;
  background-color: #0f1621;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.title-text {
  color: #0cc0ff;
  font-family: 'Orbitron', sans-serif;
  font-size: 48px;
  font-weight: bolder;
  margin-bottom: 5vh;
  text-align: center;
  text-shadow: 0 0 10px rgba(12, 192, 255, 0.5);
}

.loading-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 50vh;
}

.container-text {
  color: #0cc0ff;
  font-family: 'Orbitron', sans-serif;
  font-size: 30px;
  font-weight: 900;
  text-align: center;
}

.upload-container {
  width: 95vw;
  height: 50vh;
}

.upload-area {
  height: 100%;
  width: 100%;
}

.upload-area :deep(.el-upload) {
  width: 100%;
  height: 100%;
}

.upload-area :deep(.el-upload-dragger) {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px dashed #0cc0ff;
  background-color: transparent;
}

.csv-file {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
}

.progress-container {
  width: 80%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.upload-progress-text {
  display: flex;
  justify-content: center;
  align-items: center;
  color: #0cc0ff;
  font-family: 'Orbitron', sans-serif;
  font-size: 24px;
  margin-bottom: 20px;
}

:deep(.el-progress-bar__outer) {
  background-color: rgba(12, 192, 255, 0.2) !important;
}

:deep(.el-progress-bar__inner) {
  background-color: #0cc0ff !important;
}

.el-icon--upload {
  font-size: 48px;
  color: #ffffff;
  margin-bottom: 16px;
}

.el-upload__text {
  color: #ffffff;
  font-size: 25px;
}
</style>
