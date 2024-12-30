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
  
      <!-- Registration Form -->
      <div class="wrapper">
        <h2>Sponsor Registration</h2>
        <form @submit.prevent="register">
          <div class="form-row">
            <!-- Left Column (Fields) -->
            <div class="left-column">
              <div class="input-box">
                <input
                  type="text"
                  v-model="username"
                  placeholder="Username"
                  required
                />
              </div>
              <div class="input-box">
                <input
                  type="email"
                  v-model="email"
                  placeholder="Email Address"
                  required
                />
              </div>
              <div class="input-box">
                <input
                  type="text"
                  v-model="company_name"
                  placeholder="Company Name"
                  required
                />
              </div>
              <div class="input-box">
                <input
                  type="text"
                  v-model="industry"
                  placeholder="Industry"
                  required
                />
              </div>
            </div>
  
            <!-- Right Column (Fields) -->
            <div class="right-column">
              <div class="input-box">
                <input
                  type="number"
                  v-model="budget"
                  placeholder="Budget"
                  min="0"
                  required
                />
              </div>
              <div class="input-box">
                <input
                  :type="showPassword ? 'text' : 'password'"
                  v-model="password"
                  placeholder="Password"
                  required
                />
              </div>
            </div>
          </div>
  
          <!-- Submit Button -->
          <div class="input-box button">
            <input type="submit" value="Register" :disabled="!isFormValid" />
          </div>
  
          <!-- Error and Success Message -->
          <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
          <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
        </form>
      </div>
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
        company_name: "",
        industry: "",
        budget: "",
        errorMessage: "",
        successMessage: "",
        showPassword: false,
      };
    },
    computed: {
      isFormValid() {
        return (
          this.username &&
          this.password &&
          this.email &&
          this.company_name &&
          this.industry &&
          this.budget
        );
      },
    },
    methods: {
      async register() {
        try {
          await axios.post("/sponsor/register", {
            username: this.username,
            email: this.email,
            password: this.password,
            company_name: this.company_name,
            industry: this.industry,
            budget: this.budget,
          });
          this.successMessage =
            "Registration successful! Redirecting to Login page...";
          this.errorMessage = ""; // Clear any previous error messages
          setTimeout(() => {
            this.$router.push("/sponsor/login");
          }, 2000);
        } catch (error) {
          this.errorMessage =
            error.response.data.message || "Registration failed";
          this.successMessage = ""; // Clear any previous success message
        }
      },
    },
  };
  </script>
  
  <style scoped>
  @import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap");
  
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: "Poppins", sans-serif;
  }
  
  body,
  html {
    height: 100%;
    margin: 0;
    background: #4070f4;
  }
  
  .wrapper {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 80%;
    max-width: 800px;
    background: #fff;
    padding: 34px;
    border-radius: 6px;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
  }
  
  .wrapper h2 {
    font-size: 22px;
    font-weight: 600;
    color: #333;
    margin-bottom: 30px;
    text-align: center;
  }
  
  .wrapper form {
    margin-top: 20px;
  }
  
  .form-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
  }
  
  .left-column,
  .right-column {
    width: 48%;
  }
  
  .input-box {
    width: 100%;
    margin-bottom: 18px;
  }
  
  .input-box input {
    width: 100%;
    padding: 15px;
    font-size: 17px;
    border: 1.5px solid #c7bebe;
    border-radius: 6px;
    transition: all 0.3s ease;
    color: #333;
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
  
  .error-message {
    margin-top: 15px;
    color: red;
    text-align: center;
  }
  
  .success-message {
    margin-top: 15px;
    color: green;
    text-align: center;
  }
  
  .navbar {
    position: fixed;
    top: 0;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #ff7c01;
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
  
  @media (max-width: 768px) {
    .form-row {
      flex-direction: column;
      align-items: center;
    }
  
    .left-column,
    .right-column {
      width: 100%;
    }
  
    .wrapper {
      width: 90%;
      padding: 20px;
    }
  }
  </style>
  