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
      <!-- <a-upload draggable accept=".csv" :custom-request="handleFileChange" :file-list="testList"/> -->
      <a-upload action="/" :file-list="testList" />
      {{ testList }}
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import axios from 'axios'
import { useDataStore } from '@/stores/store'
import { useRouter } from 'vue-router'
import test from 'node:test'

const testList = ref([])

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

// 处理文件上传逻辑
const handleFileChange = async (option) => {
  const { onProgress, onError, onSuccess, fileItem, name } = option
  console.log(JSON.stringify(fileItem))
  console.log(`文件名: ${name}`)
  console.log(testList.value)
  try {
    // 2. 准备上传数据
    const formData = new FormData()
    formData.append('csvFile', fileItem.file.raw)

    // 4. 发送请求
    const response = await axios.post('/process-csv', formData, {
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

      loading.value = true
      loadingProgress()
    } else {
      console.log('上传失败')
    }
  } catch (error) {
    console.log(`上传失败: ${error.message}`)
  }
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
</style>
