<template>
  <div class="kpi-card">
    <h3>{{ title }}</h3>
    <p>{{ value }}</p>
  </div>
</template>

<script>
export default {
  name: 'KPICard',
  props: {
    title: String,
    value: [Number, String]
  }
}
</script>

<style scoped>
.kpi-card {
  background-color: white;
  border-radius: 8px;
  padding: 0.75rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: center;
  width: 100%;
}

h3 {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}

p {
  margin: 0.25rem 0 0;
  font-size: 1.2rem;
  font-weight: bold;
  color: #42b983;
}
</style>