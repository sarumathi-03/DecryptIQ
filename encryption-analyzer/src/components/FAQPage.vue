<template>
  <div class="faq">
    <h2>Frequently Asked Questions</h2>
    <div v-for="(item, index) in faqItems" :key="index" class="faq-item">
      <h3>{{ item.question }}</h3>
      <p>{{ item.answer }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FAQPage',
  data() {
    return {
      faqItems: [
        {
          question: "What types of ciphers can DecryptIQ analyze?",
          answer: "DecryptIQ can analyze a wide range of classical and modern ciphers, including substitution ciphers, transposition ciphers, and many symmetric encryption algorithms."
        },
        {
          question: "How accurate is the algorithm prediction?",
          answer: "Our algorithm prediction is based on advanced machine learning models and cryptographic patterns. While it's highly accurate for many common ciphers, it's important to note that it provides an educated guess rather than a definitive answer."
        },
        {
          question: "Can DecryptIQ decrypt my cipher?",
          answer: "DecryptIQ is designed to analyze and predict the encryption algorithm, not to decrypt the cipher itself. Decryption would require the correct key, which is not part of our service."
        },
        {
          question: "Is my data safe when using DecryptIQ?",
          answer: "We take data privacy very seriously. All analyses are performed in real-time and we do not store any of the cipher text you input. Our service runs entirely in your browser, ensuring your data never leaves your device."
        }
      ]
    }
  }
}
</script>

<style scoped>
.faq {
  max-width: 800px;
  margin: 0 auto;
  text-align: left;
}

.faq-item {
  margin-bottom: 20px;
  border-bottom: 1px solid #eee;
  padding-bottom: 20px;
}

h2 {
  color: #42b983;
}

h3 {
  color: #2c3e50;
}
</style>