<template>
    <div class="chart">
      <h3>Character Distribution</h3>
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, watch } from 'vue'
  import Chart from 'chart.js/auto'
  
  export default {
    name: 'CharacterDistributionChart',
    props: {
      charCounts: {
        type: Object,
        required: true
      }
    },
    setup(props) {
      const chartCanvas = ref(null)
      let chart = null
  
      const createChart = () => {
        const ctx = chartCanvas.value.getContext('2d')
        chart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: Object.keys(props.charCounts),
            datasets: [{
              label: 'Character Count',
              data: Object.values(props.charCounts),
              backgroundColor: 'rgba(75, 192, 192, 0.6)'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        })
      }
  
      const updateChart = () => {
        chart.data.labels = Object.keys(props.charCounts)
        chart.data.datasets[0].data = Object.values(props.charCounts)
        chart.update()
      }
  
      onMounted(() => {
        createChart()
      })
  
      watch(() => props.charCounts, updateChart, { deep: true })
  
      return { chartCanvas }
    }
  }
  </script>
  
  <style scoped>
  .chart {
    width: 100%;
    height: 100%;
    min-height: 200px; /* Add this line */
    display: flex;
    flex-direction: column;
  }
  
  h3 {
    margin-top: 0;
    margin-bottom: 0.5rem;
    font-size: 1rem;
  }
  
  canvas {
    flex: 1;
    width: 100% !important;
    height: calc(100% - 1.5rem) !important;
  }
  </style>