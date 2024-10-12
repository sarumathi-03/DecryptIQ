<template>
    <div class="chart">
      <h3>Type Ratio</h3>
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, watch } from 'vue'
  import Chart from 'chart.js/auto'
  
  export default {
    name: 'TypeRatioChart',
    props: {
      alphaCount: Number,
      numCount: Number,
      specialCount: Number
    },
    setup(props) {
      const chartCanvas = ref(null)
      let chart = null
  
      const createChart = () => {
        const ctx = chartCanvas.value.getContext('2d')
        chart = new Chart(ctx, {
          type: 'pie',
          data: {
            labels: ['Alphabets', 'Numbers', 'Special Characters'],
            datasets: [{
              data: [props.alphaCount, props.numCount, props.specialCount],
              backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        })
      }
  
      const updateChart = () => {
        chart.data.datasets[0].data = [props.alphaCount, props.numCount, props.specialCount]
        chart.update()
      }
  
      onMounted(() => {
        createChart()
      })
  
      watch([() => props.alphaCount, () => props.numCount, () => props.specialCount], updateChart)
  
      return { chartCanvas }
    }
  }
  </script>
  
  <style scoped>
  .chart {
    width: 100%;
    height: 100%;
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