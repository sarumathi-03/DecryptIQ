<template>
    <div class="chart">
      <h3>Bigram Frequency Analysis</h3>
      <canvas ref="chartCanvas"></canvas>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, watch } from 'vue'
  import Chart from 'chart.js/auto'
  
  export default {
    name: 'BigramAnalysisChart',
    props: {
      bigramFrequencies: {
        type: Object,
        required: true
      }
    },
    setup(props) {
      const chartCanvas = ref(null)
      let chart = null
  
      const createChart = () => {
        const ctx = chartCanvas.value.getContext('2d')
        const sortedFreq = Object.entries(props.bigramFrequencies)
          .sort(([,a], [,b]) => b - a)
          .slice(0, 15)
        
        chart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: sortedFreq.map(([bigram]) => bigram),
            datasets: [{
              label: 'Bigram Frequency',
              data: sortedFreq.map(([,freq]) => freq),
              backgroundColor: 'rgba(54, 162, 235, 0.6)'
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
                    return value.toFixed(3)
                  }
                }
              }
            }
          }
        })
      }
  
      const updateChart = () => {
        const sortedFreq = Object.entries(props.bigramFrequencies)
          .sort(([,a], [,b]) => b - a)
          .slice(0, 15)
        
        chart.data.labels = sortedFreq.map(([bigram]) => bigram)
        chart.data.datasets[0].data = sortedFreq.map(([,freq]) => freq)
        chart.update()
      }
  
      onMounted(() => {
        createChart()
      })
  
      watch(() => props.bigramFrequencies, updateChart, { deep: true })
  
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