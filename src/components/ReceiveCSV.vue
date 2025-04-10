<template>
  <div class="receiver-container">
    <div class="drop-area" @dragover.prevent @drop="handleDrop">
      <div v-if="csvFilename" class="csv-file">
        <img src="@/assets/csv-icon.svg" />
        {{ csvFilename }}
      </div>
      <text v-else>请将 CSV 文件拖拽到此处</text>
    </div>

    <div class="ouput-container">
      <div class="file-show">
        <text v-if="npyFiles.length < 1">这里将会展示输出文件</text>
        <div v-else class="file-list">
          <div v-for="(file, index) in npyFiles" :key="index">
            <a :href="file.url" download>
              <div class="file-item">
                <img src="@/assets/npy-icon.svg" />
                {{ file.name }}
              </div>
            </a>
          </div>
        </div>
      </div>

      <div class="tech-container">
        <div class="tech-header">NPY 数据可视化分析</div>
        <div ref="chartContainer" class="chart-container"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted, render } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts' // 导入 ECharts

axios.defaults.baseURL = 'http://127.0.0.1:5000'
axios.defaults.headers.common['Access-Control-Allow-Origin'] = '*'

// 创建DOM引用和图表实例引用
const chartContainer = ref(null)
const chart = ref(null)

// 获取数据的方法
const fetchData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5001/plot')
    if (response.status !== 200) {
      throw new Error('获取数据失败')
    }
    const data = response.data
    console.log(JSON.stringify(data))
    // console.log(data.length)
    renderChart(data)
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

const generateSeriesList = (data) => {
  // 科技风配色方案数组
  const colorSchemes = [
    { start: '#0cc0ff', end: '#5653ff', shadow: '#0cc0ff' }, // 蓝色系
    { start: '#00ffcc', end: '#00ccaa', shadow: '#00ffcc' }, // 青色系
    { start: '#c000ff', end: '#8a00cc', shadow: '#c000ff' }, // 紫色系
    { start: '#00ff66', end: '#00cc44', shadow: '#00ff66' }, // 绿色系
    { start: '#ff9900', end: '#cc7700', shadow: '#ff9900' }, // 橙色系
    { start: '#ff00cc', end: '#cc0099', shadow: '#ff00cc' }, // 粉色系
    { start: '#ffcc00', end: '#cc9900', shadow: '#ffcc00' }, // 黄色系
  ]

  const seriesList = []
  for (let i = 0; i < 7; i++) {
    seriesList.push({
      name: `时序${i + 1}`,
      type: 'line',
      data: data.map((item, index) => [index, item[i]]),
      symbol: 'none',
      lineStyle: {
        width: 2,
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: colorSchemes[i].start },
          { offset: 1, color: colorSchemes[i].end },
        ]),
        shadowColor: '#0cc0ff',
        shadowBlur: 5,
      },
      smooth: true,
    })
  }
  return seriesList
}

// 修改 renderChart 函数中的坐标轴配置
const renderChart = (data) => {
  // 确保容器存在
  if (!chartContainer.value) return

  // 初始化ECharts实例
  chart.value = echarts.init(chartContainer.value)

  // 科技风格配置
  const option = {
    backgroundColor: '#0f1621',
    title: {
      text: 'NPY 数据波形分析',
      left: 'center',
      textStyle: {
        color: '#0cc0ff',
        fontSize: 20,
        fontFamily: '"Orbitron", sans-serif',
        fontWeight: 'bold',
      },
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(15, 22, 33, 0.7)',
      borderColor: '#0cc0ff',
      textStyle: { color: '#fff' },
      axisPointer: {
        type: 'cross',
        lineStyle: { color: '#0cc0ff', type: 'dashed' },
      },
      formatter: function (params) {
        return params
          .map((item) => {
            return `${item.seriesName}: (${item.value[0].toFixed(3)}, ${item.value[1].toFixed(3)})`
          })
          .join('<br/>')
      },
    },
    grid: {
      left: '5%',
      right: '5%',
      bottom: '8%',
      top: '15%',
      containLabel: true,
      show: true,
      borderColor: 'rgba(12, 192, 255, 0.1)',
      backgroundColor: 'rgba(12, 192, 255, 0.02)',
    },
    xAxis: {
      type: 'value',
      min: 'dataMin',
      max: 'dataMax',
      splitLine: {
        show: true,
        lineStyle: { color: 'rgba(12, 192, 255, 0.1)', type: 'dashed' },
      },
      axisLine: { lineStyle: { color: '#0cc0ff' } },
      axisLabel: {
        color: '#7adbff',
        formatter: (value) => value.toFixed(0),
      },
      name: 'X轴',
      nameTextStyle: { color: '#0cc0ff' },
    },
    yAxis: {
      type: 'value',
      min: 'dataMin',
      max: 'dataMax',
      splitLine: {
        lineStyle: { color: 'rgba(12, 192, 255, 0.1)', type: 'dashed' },
      },
      axisLine: { lineStyle: { color: '#0cc0ff' } },
      axisLabel: {
        color: '#7adbff',
        formatter: (value) => value.toFixed(1),
      },
      name: 'Y轴',
      nameTextStyle: { color: '#0cc0ff' },
    },
    series: generateSeriesList(data),
    animation: true,
    animationDuration: 1000,
    animationEasing: 'cubicOut',
  }

  // 渲染图表
  chart.value.setOption(option)

  // 添加窗口调整大小的监听器
  window.addEventListener('resize', handleResize)
}

// 处理窗口大小调整
const handleResize = () => {
  if (chart.value) {
    chart.value.resize()
  }
}

// 组件卸载前清理
onUnmounted(() => {
  if (chart.value) {
    chart.value.dispose()
  }
  window.removeEventListener('resize', handleResize)
})

const csvFilename = ref('')
const npyFiles = ref([])

const handleDrop = async (event) => {
  event.preventDefault()
  const files = event.dataTransfer.files
  if (files.length > 0 && files[0].type === 'text/csv') {
    const formData = new FormData()
    formData.append('csvFile', files[0])

    try {
      const response = await axios.post('http://127.0.0.1:5000/process-csv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      if (response.status === 200) {
        const data = response.data
        csvFilename.value = data.csvFilename
        npyFiles.value = data.files.map((file) => ({
          name: file,
          url: `/download/${file}`,
        }))
      } else {
        console.error('处理 CSV 文件时出错')
      }

      // 重新获取数据并渲染图表
      console.log('重新获取数据并渲染图表')
      fetchData()
    } catch (error) {
      console.error('网络错误:', error)
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&display=swap');

.ouput-container {
  width: 65%;
  height: 95%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.file-show {
  width: 100%;
  height: 15%;
  border: 2px dashed #0cc0ff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0cc0ff;
  font-family: 'Orbitron', sans-serif;
  font-size: 20px;
  text-align: center;
}

.tech-container {
  width: 100%;
  padding: 20px;
  background-color: #0f1621;
  border-radius: 8px;
  box-shadow:
    0 0 20px rgba(12, 192, 255, 0.2),
    0 0 30px rgba(12, 192, 255, 0.1) inset;
  border: 1px solid rgba(12, 192, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.tech-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #0cc0ff);
  animation: scan 4s linear infinite;
}

@keyframes scan {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.tech-header {
  color: #0cc0ff;
  font-family: 'Orbitron', sans-serif;
  font-size: 22px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 10px;
  text-shadow: 0 0 10px rgba(12, 192, 255, 0.5);
  letter-spacing: 2px;
}

.chart-container {
  width: 950px;
  height: 600px;
  margin: 0 auto;
  position: relative;
}

/* 添加科技风装饰角 */
.tech-container::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 30px;
  height: 30px;
  border-top: 2px solid #0cc0ff;
  border-right: 2px solid #0cc0ff;
}

.tech-container::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 30px;
  height: 30px;
  border-bottom: 2px solid #0cc0ff;
  border-left: 2px solid #0cc0ff;
  z-index: 1;
}

.receiver-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background-color: #0f1621;
}

.drop-area {
  display: flex;
  justify-content: center;
  align-items: center;
  border: 2px dashed #0cc0ff;
  text-align: center;
  width: 30%;
  height: 95%;
}

.file-list {
  display: flex;
  align-items: center;
  justify-content: space-around;
  width: 100%;
  height: 100%;
}

.csv-file {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
}

.file-item {
  display: flex;
  align-items: center;
  flex-direction: column;
  justify-content: center;
}
.file-item:hover {
  background-color: rgba(12, 192, 255, 0.3);
}
</style>
