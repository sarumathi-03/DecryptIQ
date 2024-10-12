<template>
  <div class="home-page">
    <h1>Your Cipher's Analysis</h1>
    <div class="content-wrapper">
      <div class="left-column">
        <div class="input-section">
          <textarea v-model="cipherText" @input="updateAnalysis" placeholder="Enter your cipher text here..."></textarea>
          <div class="button-container">
            <button @click="predictAlgorithm" :disabled="isPredicting">
              {{ isPredicting ? 'Predicting...' : 'Predict Algorithm' }}
            </button>
          </div>
        </div>
        <div class="kpi-section">
          <KPICard title="Cipher Length" :value="cipherLength" />
          <KPICard title="Entropy" :value="entropy.toFixed(2)" />
          <KPICard title="Special Characters" :value="specialCharCount" />
          <KPICard title="Chi-Square" :value="chiSquare.toFixed(2)" />
          <KPICard title="IC" :value="indexOfCoincidence.toFixed(4)" />
        </div>
      </div>
      <div class="right-column">
        <div class="charts-section">
          <div class="chart-container">
            <CharacterDistributionChart :char-counts="charCounts" />
          </div>
          <div class="chart-container">
            <TypeRatioChart :alpha-count="alphaCount" :num-count="numCount" :special-count="specialCharCount" />
          </div>
          <div class="chart-container">
            <FrequencyAnalysisChart :char-frequencies="charFrequencies" />
          </div>
          <div class="chart-container">
            <BigramAnalysisChart :bigram-frequencies="bigramFrequencies" />
          </div>
        </div>
      </div>
    </div>
    <PredictionModal v-if="showPredictionModal" :prediction="predictionResult" @close="showPredictionModal = false" />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import KPICard from './KPICard.vue'
import CharacterDistributionChart from './CharacterDistributionChart.vue'
import TypeRatioChart from './TypeRatioChart.vue'
import FrequencyAnalysisChart from './FrequencyAnalysisChart.vue'
import BigramAnalysisChart from './BigramAnalysisChart.vue'
import PredictionModal from './PredictionModal.vue'

export default {
  name: 'HomePage',
  components: {
    KPICard,
    CharacterDistributionChart,
    TypeRatioChart,
    FrequencyAnalysisChart,
    BigramAnalysisChart,
    PredictionModal
  },
  setup() {
    const cipherText = ref('')
    const charCounts = ref({})
    const charFrequencies = ref({})
    const bigramFrequencies = ref({})
    const isPredicting = ref(false)
    const predictionResult = ref(null)
    const showPredictionModal = ref(false)

    const cipherLength = computed(() => cipherText.value.length)
    const entropy = computed(() => calculateEntropy(charFrequencies.value))
    const specialCharCount = computed(() => countSpecialChars(cipherText.value))
    const alphaCount = computed(() => cipherText.value.replace(/[^a-zA-Z]/g, '').length)
    const numCount = computed(() => cipherText.value.replace(/[^0-9]/g, '').length)
    const chiSquare = computed(() => calculateChiSquare(charFrequencies.value))
    const indexOfCoincidence = computed(() => calculateIC(charCounts.value, cipherLength.value))

    function updateAnalysis() {
      updateCharCounts()
      updateCharFrequencies()
      updateBigramFrequencies()
    }

    function updateCharCounts() {
      charCounts.value = {}
      for (let char of cipherText.value) {
        charCounts.value[char] = (charCounts.value[char] || 0) + 1
      }
    }

    function updateCharFrequencies() {
      const total = cipherText.value.length
      charFrequencies.value = Object.fromEntries(
        Object.entries(charCounts.value).map(([char, count]) => [char, count / total])
      )
    }

    function updateBigramFrequencies() {
      const bigrams = {}
      for (let i = 0; i < cipherText.value.length - 1; i++) {
        const bigram = cipherText.value.slice(i, i + 2)
        bigrams[bigram] = (bigrams[bigram] || 0) + 1
      }
      const total = Object.values(bigrams).reduce((sum, count) => sum + count, 0)
      bigramFrequencies.value = Object.fromEntries(
        Object.entries(bigrams).map(([bigram, count]) => [bigram, count / total])
      )
    }

    function calculateEntropy(frequencies) {
      return -Object.values(frequencies).reduce((sum, freq) => sum + freq * Math.log2(freq || 1), 0)
    }

    function countSpecialChars(text) {
      return text.replace(/[a-zA-Z0-9\s]/g, '').length
    }

    function calculateChiSquare(frequencies) {
      const expectedFreq = 1 / 26 // Assuming English alphabet
      return Object.values(frequencies).reduce((sum, freq) => {
        const diff = freq - expectedFreq
        return sum + (diff * diff) / expectedFreq
      }, 0)
    }

    function calculateIC(counts, total) {
      if (total <= 1) return 0
      const sum = Object.values(counts).reduce((acc, count) => acc + count * (count - 1), 0)
      return sum / (total * (total - 1))
    }

    async function predictAlgorithm() {
      if (!cipherText.value.trim()) return;
      
      isPredicting.value = true;
      const url = 'http://127.0.0.1:5000/predict';
      const data = { cipher_text: cipherText.value };
      const headers = { 'Content-Type': 'application/json' };

      try {
        const response = await axios.post(url, data, { headers });
        console.log('Response:', response.data);
        predictionResult.value = response.data;
        showPredictionModal.value = true;
      } catch (error) {
        console.error('Prediction error:', error);
        predictionResult.value = null;
      } finally {
        isPredicting.value = false;
      }
    }

    onMounted(() => {
      updateAnalysis()
    })

    return {
      cipherText,
      cipherLength,
      entropy,
      specialCharCount,
      alphaCount,
      numCount,
      charCounts,
      charFrequencies,
      bigramFrequencies,
      chiSquare,
      indexOfCoincidence,
      updateAnalysis,
      predictAlgorithm,
      isPredicting,
      predictionResult,
      showPredictionModal
    }
  }
}
</script>

<style scoped>
.home-page {
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  padding: 1rem;
  height: calc(100vh - 2rem);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

h1 {
  margin-top: 0;
  margin-bottom: 1rem;
  color: #333;
  text-align: center;
}

.content-wrapper {
  display: flex;
  gap: 2rem;
  height: calc(100% - 3rem);
  overflow-y: auto;
  padding-bottom: 1rem;
}

.left-column {
  width: 300px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

textarea {
  width: 100%;
  height: 150px;
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
  resize: vertical;
}

.button-container {
  display: flex;
  justify-content: center;
}

button {
  padding: 0.5rem 1rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.kpi-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  align-items: center;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  gap: 1rem;
  height: 100%;
}

.chart-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  aspect-ratio: 4 / 3;
}

@media (max-width: 1200px) {
  .content-wrapper {
    flex-direction: column;
  }

  .left-column {
    width: 100%;
  }

  .charts-section {
    grid-template-columns: 1fr;
    grid-template-rows: repeat(4, 1fr);
  }

  .chart-container {
    aspect-ratio: auto;
    height: 300px;
  }
}

@media (max-width: 768px) {
  .kpi-section {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
  }

  .kpi-section > * {
    width: calc(50% - 0.5rem);
  }
}
</style>
