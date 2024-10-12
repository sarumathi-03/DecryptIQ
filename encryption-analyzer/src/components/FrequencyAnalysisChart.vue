<template>
    <div class="chart">
      <h3>Character Frequency Analysis</h3>
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, watch } from 'vue'
  import Chart from 'chart.js/auto'
  
  export default {
    name: 'FrequencyAnalysisChart',
    props: {
      charFrequencies: {
        type: Object,
        required: true
      }
    },
    setup(props) {
      const chartCanvas = ref(null)
      let chart = null
  
      const createChart = () => {
        const ctx = chartCanvas.value.getContext('2d')
        const sortedFreq = Object.entries(props.charFrequencies)
          .sort(([,a], [,b]) => b - a)
          .slice(0, 10)
        
        chart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: sortedFreq.map(([char]) => char),
            datasets: [{
              label: 'Character Frequency',
              data: sortedFreq.map(([,freq]) => freq),
              backgroundColor: 'rgba(255, 99, 132, 0.6)'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  callback: function(value) {
                    return value.toFixed(2)
                  }
                }
              }
            }
          }
        })
      }
  
      const updateChart = () => {
        const sortedFreq = Object.entries(props.charFrequencies)
          .sort(([,a], [,b]) => b - a)
          .slice(0, 10)
        
        chart.data.labels = sortedFreq.map(([char]) => char)
        chart.data.datasets[0].data = sortedFreq.map(([,freq]) => freq)
        chart.update()
      }
  
      onMounted(() => {
        createChart()
      })
  
      watch(() => props.charFrequencies, updateChart, { deep: true })
  
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