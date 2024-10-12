<template>
    <div class="modal-overlay" @click="$emit('close')">
      <div class="modal-content" @click.stop>
        <h2>Algorithm Prediction Results</h2>
        <div class="prediction-chart">
          <canvas ref="chartCanvas"></canvas>
        </div>
        <div class="prediction-text">
          <p>Most likely algorithm: <strong>{{ mostLikelyAlgorithm }}</strong></p>
        </div>
        <button @click="$emit('close')">Close</button>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted, watch, computed } from 'vue'
  import Chart from 'chart.js/auto'
  
  export default {
    name: 'PredictionModal',
    props: {
      prediction: {
        type: Object,
        required: true
      }
    },
    setup(props) {
      const chartCanvas = ref(null)
      let chart = null
  
      const mostLikelyAlgorithm = computed(() => {
        if (!props.prediction || !props.prediction.probabilities) return 'N/A';
        const entries = Object.entries(props.prediction.probabilities);
        return entries.reduce((a, b) => a[1] > b[1] ? a : b)[0];
      });
  
      const createChart = () => {
        if (!props.prediction || !props.prediction.probabilities) return;
  
        const ctx = chartCanvas.value.getContext('2d')
        const algorithms = Object.keys(props.prediction.probabilities);
        const probabilities = Object.values(props.prediction.probabilities);
  
        chart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: algorithms,
            datasets: [{
              label: 'Probability',
              data: probabilities,
              backgroundColor: [
                'rgba(255, 99, 132, 0.6)',
                'rgba(54, 162, 235, 0.6)',
                'rgba(255, 206, 86, 0.6)'
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                max: 1
              }
            }
          }
        })
      }
  
      onMounted(() => {
        createChart()
      })
  
      watch(() => props.prediction, () => {
        if (chart) {
          chart.destroy()
        }
        createChart()
      })
  
      return { chartCanvas, mostLikelyAlgorithm }
    }
  }
  </script>
  
  <style scoped>
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
  }
  
  .modal-content {
    background-color: white;
    padding: 2rem;
    border-radius: 8px;
    width: 80%;
    max-width: 600px;
  }
  
  .prediction-chart {
    height: 300px;
    margin-bottom: 1rem;
  }
  
  .prediction-text {
    margin-bottom: 1rem;
    text-align: center;
  }
  
  button {
    padding: 0.5rem 1rem;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #3aa876;
  }
  </style>