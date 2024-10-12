<template>
  <div class="about">
    <h2>About DecryptIQ</h2>
    <p>DecryptIQ is a cutting-edge platform designed to analyze and predict encryption algorithms used in various ciphers. Our advanced machine learning models and cryptographic expertise allow us to provide real-time insights into the nature of encrypted text.</p>
    <h3>Our Mission</h3>
    <p>To empower cybersecurity professionals, researchers, and enthusiasts with tools to better understand and analyze encrypted communications.</p>
    <h3>How It Works</h3>
    <ol>
      <li>Input your cipher text into our analysis tool.</li>
      <li>Our system performs real-time analysis, providing instant feedback on various metrics.</li>
      <li>Use the "Predict Algorithm" feature to get an educated guess on the encryption method used.</li>
    </ol>
  </div>
</template>

<script>
export default {
  name: 'AboutPage'
}
</script>

<style scoped>
.about {
  max-width: 800px;
  margin: 0 auto;
  text-align: left;
}

h2, h3 {
  color: #42b983;
}

ol {
  padding-left: 20px;
}

li {
  margin-bottom: 10px;
}
</style>