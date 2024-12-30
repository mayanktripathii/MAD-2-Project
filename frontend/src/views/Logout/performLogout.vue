<template>
  <div>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark">
      <!-- Logo/Title -->
      <a class="navbar-brand" href="#">
        <i class="fas fa-tachometer-alt"></i> {{ DashboardTitle }}
      </a>

      <!-- Navbar Toggle (for mobile) -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- Navbar Links (right aligned) -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <button class="btn btn-outline-light" @click="performLogout">
              <i class="fas fa-sign-out-alt"></i> Logout
            </button>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>
  
  <script>
  import { mapActions } from 'vuex';
  import axios from 'axios';
  
  export default {
    props: {
      DashboardTitle: {
        type: String,
        required: true
      }
    },
    methods: {
      ...mapActions(['logout', 'setError', 'clearMessages']),
      
      async performLogout() {
        try {
          // Trigger the backend logout API
          await axios.post('http://localhost:5000/logout');
  
          // Call Vuex logout action
          await this.logout();
          
          // Clear any previous messages
          this.clearMessages();
          
          // Redirect to the home page
          this.$router.push('/').then(() => {
            // Optionally clear messages on redirect
            this.clearMessages();
          });
        } catch (error) {
          console.error("Logout failed:", error);
          this.setError("Logout failed. Please try again.");
        }
      }
    }
  };
  </script>

<style scoped>
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