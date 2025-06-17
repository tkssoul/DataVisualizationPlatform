import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  base: '/DataVisualizationPlatform/',
  plugins: [
    vue(),
    vueJsx(),
    vueDevTools(),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  build: {
    outDir: 'docs',
    rollupOptions: {
      output: {
        manualChunks(id: string) {
          if (id.includes('node_modules')) {
            // 将 Element Plus 单独打包
            if (id.includes('element-plus')) {
              return 'element-plus'
            }
            // 将 ECharts 和其核心依赖 ZRender 单独打包
            if (id.includes('echarts') || id.includes('zrender')) {
              return 'echarts-vendor'
            }
            // 将 Vue Router 单独打包
            if (id.includes('vue-router')) {
              return 'vue-router'
            }
            // 将 Vue 核心库 (vue, @vue/runtime-dom 等) 单独打包
            // 这个判断应该在 vue-router 之后，以避免 vue-router 被错误地归入 vue-core
            if (id.includes('/vue/') || id.includes('/@vue/')) {
              return 'vue-core'
            }
          }
        },
      },
    },
  },
})
