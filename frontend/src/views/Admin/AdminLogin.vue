<template>
    <div id="app">
      <!-- Navbar -->
      <nav class="navbar">
        <div class="logo">Sponsorly: Crafting Connections</div>
        <router-link to="/">Home</router-link>
        <router-link to="/signup">Signup</router-link>
        <span v-if="userRole === 'influencer'">
          <router-link to="/influencer-dashboard">Influencer Dashboard</router-link>
        </span>
        <span v-if="userRole === 'sponsor'">
          <router-link to="/sponsor-dashboard">Sponsor Dashboard</router-link>
        </span>
        <router-link to="/login">Login</router-link>
      </nav>
  
      <!-- Login Form -->
      <div class="wrapper">
        <h2>Admin Login</h2>
        <form @submit.prevent="login">
          <!-- Username Field -->
          <div class="input-box">
            <input 
              type="text" 
              v-model="username" 
              placeholder="Enter your username" 
              required 
            />
          </div>
  
          <!-- Password Field -->
          <div class="input-box">
            <input 
              :type="showPassword ? 'text' : 'password'" 
              v-model="password" 
              placeholder="Enter your password" 
              required 
            />
          </div>
  
          <!-- Submit Button -->
          <div class="input-box button">
            <input type="submit" value="Login" :disabled="!isFormValid" />
          </div>
  
          <!-- Error Message -->
          <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
  
          <!-- Signup Link -->
          <div class="text">
            <h3>Don't have an account? <router-link to="/signup">Sign up now</router-link></h3>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapActions } from 'vuex';
  
  export default {
    data() {
      return {
        username: '',
        password: '',
        showPassword: false,
        errorMessage: '',
      };
    },
    computed: {
      isFormValid() {
        return this.username && this.password;
      },
    },
    methods: {
      ...mapActions(['login']),
  
      async login() {
        try {
          const response = await axios.post('http://127.0.0.1:5000/admin/login', {
            username: this.username,
            password: this.password,
          });
  
          // Extract token and role from the response
          const { token, role } = response.data;
  
          // Update Vuex store with token and role
          this.$store.dispatch('login', { token, role });
  
          // Redirect to the appropriate dashboard
          if (role === 'admin') {
            this.$router.push('/admin/dashboard');
          } else {
            // Handle other roles if needed
          }
        } catch (error) {
          console.error('Login error:', error);
          this.errorMessage = error.response?.data?.message || 'Login failed';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  @import url("https://fonts.googleapis.com/css?family=Poppins:400,500,600,700&display=swap");
  
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Poppins", sans-serif;
  }
  
  body, html {
    height: 100%;
    margin: 0;
  }
  
  body {
    background: #4070f4;
  }
  
  .wrapper {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    max-width: 430px;
    width: 100%;
    background: #fff;
    padding: 34px;
    border-radius: 6px;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
  }
  
  .wrapper h2 {
    font-size: 22px;
    font-weight: 600;
    color: #333;
    position: relative;
  }
  
  .wrapper h2::before {
    content: "";
    position: absolute;
    left: 0;
    bottom: 0;
    height: 3px;
    width: 28px;
    border-radius: 12px;
    background: #4070f4;
  }
  
  .wrapper form {
    margin-top: 30px;
  }
  
  .wrapper form .input-box {
    height: 52px;
    margin: 18px 0;
  }
  
  form .input-box input {
    height: 100%;
    width: 100%;
    outline: none;
    padding: 0 15px;
    font-size: 17px;
    font-weight: 400;
    color: #333;
    border: 1.5px solid #c7bebe;
    border-bottom-width: 2.5px;
    border-radius: 6px;
    transition: all 0.3s ease;
  }
  
  .input-box input:focus,
  .input-box input:valid {
    border-color: #4070f4;
  }
  
  .input-box.button input {
    color: #fff;
    letter-spacing: 1px;
    border: none;
    background: #4070f4;
    cursor: pointer;
  }
  
  .input-box.button input:hover {
    background: #0e4bf1;
  }
  
  form .text h3 {
    color: #333;
    width: 100%;
    text-align: center;
  }
  
  form .text h3 a {
    color: #4070f4;
    text-decoration: none;
  }
  
  form .text h3 a:hover {
    text-decoration: underline;
  }
  
  .error-message {
    margin-top: 15px;
    color: red;
    text-align: center;
  }
  
  #app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
  }
  
  /* Navbar styling */
  .navbar {
    position: fixed;
    top: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #ff7c01; /* Fully opaque color */
    padding: 15px 30px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    z-index: 1000;
  }
  
  nav a {
    font-weight: bold;
    color: #00060b;
    margin: 0 15px;
    text-decoration: none;
    transition: color 0.3s ease;
  }
  
  nav a:hover {
    color: #fdfdfd;
    text-decoration: underline;
  }
  
  .logo {
    font-size: 1.5em;
    font-weight: bold;
    color: #00060b;
    margin-right: auto;
  }
  
  @media (max-width: 600px) {
    .navbar {
      flex-direction: column;
      padding: 10px;
    }
  
    nav a {
      margin: 5px 0;
    }
  }
  </style>
  