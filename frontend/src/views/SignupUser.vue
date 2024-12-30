<template>

<div id="app">
    
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
    </div>


    <div class="wrapper">
      <h2>Signup</h2>
      <form @submit.prevent="SignupUser">
        <div class="input-box">
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            placeholder="Enter your username" 
            required 
          />
        </div>
        <div class="input-box">
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            placeholder="Enter your email" 
            required 
          />
        </div>
        <div class="input-box">
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="Create password" 
            required 
          />
        </div>
        <div class="policy">
          <input 
            type="radio" 
            id="influencer" 
            value="influencer" 
            v-model="role" 
            required 
          />
          <label for="influencer">Influencer</label>
          <input 
            type="radio" 
            id="sponsor" 
            value="sponsor" 
            v-model="role" 
            required 
          />
          <label for="sponsor">Sponsor</label>
        </div>
        <div class="input-box button">
          <input type="submit" value="Sign Up" />
        </div>
        <div class="text">
          <h3>Already have an account? <router-link to="/login">Login now</router-link></h3>
        </div>
      </form>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        username: "",
        email: "",
        password: "",
        role: "",
        errorMessage: "",
      };
    },
    methods: {
      async SignupUser() {
        try {
          await axios.post("http://127.0.0.1:5000/api/signup", {
            username: this.username,
            email: this.email,
            password: this.password,
            role: this.role,
          });
          this.$router.push("/");
        } catch (error) {
          this.errorMessage = error.response
            ? error.response.data.message
            : "Signup failed. Please try again.";
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
  display: flex;
  align-items: center;
  justify-content: center;
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
  position: relative;
  font-size: 22px;
  font-weight: 600;
  color: #333;
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

form .policy {
  display: flex;
  align-items: center;
}

form .policy input[type="radio"] {
  margin-right: 10px;
}

form .policy label {
  margin-right: 20px;
  font-size: 14px;
  font-weight: 500;
  color: #707070;
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

/* Fixed navbar styling with solid color */
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
  