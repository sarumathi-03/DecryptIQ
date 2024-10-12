<template>
  <div id="app" :class="{ 'nav-collapsed': !isNavOpen }">
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <span v-if="isNavOpen">DecryptIQ</span>
          <span v-else>IQ</span>
        </div>
        <div class="nav-toggle" @click="toggleNav" :title="isNavOpen ? 'Collapse menu' : 'Expand menu'">
          <i class="fas fa-bars"></i>
        </div>
      </div>
      <nav>
        <router-link to="/" exact title="Home">
          <i class="fas fa-home"></i>
          <span v-if="isNavOpen">Home</span>
        </router-link>
        <router-link to="/about" title="About">
          <i class="fas fa-info-circle"></i>
          <span v-if="isNavOpen">About</span>
        </router-link>
        <router-link to="/faq" title="FAQ">
          <i class="fas fa-question-circle"></i>
          <span v-if="isNavOpen">FAQ</span>
        </router-link>
        <router-link to="/contact" title="Contact">
          <i class="fas fa-envelope"></i>
          <span v-if="isNavOpen">Contact</span>
        </router-link>
      </nav>
    </aside>

    <main class="content">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isNavOpen: true
    }
  },
  methods: {
    toggleNav() {
      this.isNavOpen = !this.isNavOpen;
    }
  }
}
</script>

<style>
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css');

body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  background-color: #7b68ee;
}

#app {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  background-color: #7986cb;
  color: white;
  padding: 15px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
  width: 200px;
}

#app.nav-collapsed .sidebar {
  width: 50px;
  padding: 15px 5px;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.logo {
  font-size: 1.2rem;
  font-weight: bold;
  transition: all 0.3s ease;
}

#app.nav-collapsed .logo {
  font-size: 1rem;
}

.nav-toggle {
  cursor: pointer;
  padding: 5px;
  border-radius: 5px;
  background-color: rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  transition: all 0.3s ease;
}

.nav-toggle:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.sidebar nav {
  display: flex;
  flex-direction: column;
}

.sidebar a {
  color: white;
  text-decoration: none;
  padding: 10px;
  margin-bottom: 5px;
  border-radius: 5px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.sidebar a i {
  margin-right: 10px;
  width: 20px;
  text-align: center;
}

#app.nav-collapsed .sidebar a {
  justify-content: center;
  padding: 10px 0;
}

#app.nav-collapsed .sidebar a i {
  margin-right: 0;
}

.sidebar a:hover,
.sidebar a.router-link-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.content {
  flex-grow: 1;
  padding: 20px;
  transition: margin-left 0.3s ease;
}

#app.nav-collapsed .content {
  margin-left: 60px;
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    z-index: 1000;
  }

  #app.nav-collapsed .sidebar {
    transform: translateX(-100%);
  }

  .content {
    margin-left: 0;
    width: 100%;
  }

  #app.nav-collapsed .content {
    margin-left: 0;
  }

  .nav-toggle {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 1001;
    background-color: #7986cb;
  }

  #app.nav-collapsed .nav-toggle {
    left: 10px;
  }
}
</style>