<template>
  <div class="chart">
    <h3>Entropy Over Time</h3>
    <canvas ref="entropyChart"></canvas>
  </div>
</template>

<script>
import { Chart, LineController, LineElement, PointElement, LinearScale, TimeScale, Tooltip } from 'chart.js'
import { ref, onMounted, watch } from 'vue'
import 'chartjs-adapter-date-fns'

Chart.register(LineController, LineElement, PointElement, LinearScale, TimeScale, Tooltip)

export default {
  name: 'EntropyOverTimeChart',
  props: {
    entropyHistory: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const entropyChart = ref(null)
    let chart = null

    const createChart = () => {
      const ctx = entropyChart.value.getContext('2d')
      chart = new Chart(ctx, {
        type: 'line',
        data: {
          datasets: [{
            label: 'Entropy',
            data: props.entropyHistory.map(item => ({x: new Date(item.time), y: item.entropy})),
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
          }]
        },
        options: {
          responsive: true,
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'second'
              }
            },
            y: {
              beginAtZero: true
            }
          }
        }
      })
    }

    const updateChart = () => {
      if (chart) {
        chart.data.datasets[0].data = props.entropyHistory.map(item => ({x: new Date(item.time), y: item.entropy}))
        chart.update()
      }
    }

    onMounted(() => {
      if (props.entropyHistory.length > 0) {
        createChart()
      }
    })

    watch(() => props.entropyHistory, (newValue) => {
      if (newValue.length > 0) {
        if (!chart) {
          createChart()
        } else {
          updateChart()
        }
      }
    }, { deep: true })

    return { entropyChart }
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