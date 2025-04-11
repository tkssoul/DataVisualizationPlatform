<template>
    <div class="loading-container">
        <div class="loading-spinner">
            <div class="spinner"></div>
        </div>
        <p class="loading-text">{{ loadingText }}</p>
    </div>
</template>

<script>
export default {
    name: 'Loading',
    props: {
        loadingText: {
            type: String,
            default: '正在预测/模型运行中'
        }
    }
}
</script>

<style scoped>
.loading-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    background-color: rgba(255, 255, 255, 0.8);
    z-index: 999;
}

.loading-spinner {
    margin-bottom: 16px;
}

.spinner {
    width: 50px;
    height: 50px;
    border: 4px solid rgba(0, 0, 0, 0.1);
    border-radius: 50%;
    border-top: 4px solid #1976d2;
    animation: spin 1s linear infinite;
}

.loading-text {
    font-size: 16px;
    color: #333;
    margin: 0;
    font-weight: 500;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>