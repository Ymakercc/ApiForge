<script setup lang="ts">
const stats = [
  { label: '接口总数', value: 0, icon: 'Grid', color: '#409eff' },
  { label: '今日调用', value: 0, icon: 'TrendCharts', color: '#67c23a' },
  { label: '错误次数', value: 0, icon: 'Warning', color: '#f56c6c' },
  { label: 'Skill 数量', value: 0, icon: 'MagicStick', color: '#e6a23c' },
]
</script>

<template>
  <div>
    <el-row :gutter="16">
      <el-col v-for="stat in stats" :key="stat.label" :span="6">
        <el-card shadow="never" class="stat-card">
          <div class="stat-inner">
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
            <el-icon :size="40" :style="{ color: stat.color }">
              <component :is="stat.icon" />
            </el-icon>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top: 16px;">
      <el-col :span="24">
        <el-card shadow="never" header="近期调用趋势">
          <div class="placeholder-chart">
            <el-empty description="暂无数据" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.stat-card {
  border-radius: 8px;
}

.stat-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #303133;
  line-height: 1;
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 8px;
}

.placeholder-chart {
  height: 240px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
