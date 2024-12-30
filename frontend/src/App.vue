<template>
  <div id="app">
    

    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>

export default {
  name: 'App',
  data() {
    return {
      userRole: localStorage.getItem('userRole') || '',
    };
  },
};
</script>

<style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}



.logo {
  font-size: 1.5em;
  font-weight: bold;
  color: #00060b;
  margin-right: auto;
}






</style>
