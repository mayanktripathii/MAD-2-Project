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

  <div class="container">
    <!-- Header Section -->
    <header class="header">
      <div class="header-content text-center">
        <h1>Influencer Engagement and Sponsorship Coordination Platform</h1>
        <p>Connecting Sponsors and Influencers for Successful Campaigns</p>
        <div class="header-buttons">
          <router-link to="/influencer/login" class="btn btn-primary">Influencer-Login</router-link>
          <router-link to="/sponsor/login" class="btn btn-secondary">Sponsor-Login</router-link>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <div class="row">
      <!-- Influencer Login and Register -->
      <div class="col-md-4">
        <div class="card">
          <img src="/static/influencer login.jpeg" class="card-img-top" alt="Influencer Login and Register">
          <div class="card-body">
            <h5 class="card-title">Influencer Login & Register</h5>
            <p class="card-text">Join our platform to receive ad requests and collaborate with sponsors.</p>
            <!--<a href="/influencer_login" class="btn btn-primary">Login as Influencer</a>-->
            <a href="/influencer/register" class="btn btn-secondary mt-2">Register now as Influencer!</a>
          </div>
        </div>
      </div>

      <!-- Admin Login -->
      <div class="col-md-4">
        <div class="card">
          <img src="/static/admin.jpeg" class="card-img-top" alt="Admin Login">
          <div class="card-body">
            <h5 class="card-title">Admin Login</h5>
            <p class="card-text">Monitor and manage users, campaigns, and ad requests.</p>
            <a href="/admin/login" class="btn btn-primary">Login as Admin</a>
          </div>
        </div>
      </div>

      <!-- Sponsor Login and Register -->
      <div class="col-md-4">
        <div class="card">
          <img src="/static/sponsor login.jpeg" class="card-img-top" alt="Sponsor Login and Register">
          <div class="card-body">
            <h5 class="card-title">Sponsor Login & Register</h5>
            <p class="card-text">Create campaigns and find the right influencers for your products and services.</p>
            <!--<a href="/sponsor_login" class="btn btn-primary">Login as Sponsor</a>-->
            <a href="/sponsor/register" class="btn btn-secondary mt-2">Register now as Sponsor!</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
body {
  background-color: #f8f9fa; /* Light background for the body */
}

.header-buttons {
  margin-top: 20px; /* Space between text and buttons */
}

.header-buttons .btn {
  margin: 0 10px; /* Horizontal space between buttons */
}



.header {
  background-image: url('C:\Users\Mayank Tripathi\OneDrive\Desktop\MAD-2 Project\frontend\public\static\header-background.jpg'); /* Add a background image */
  background-size: cover; /* Cover the entire header */
  background-position: center; /* Center the background image */
  color: white;
  padding: 60px 20px; /* Padding for header */
  text-align: center; /* Center text */
  position: relative; /* Position relative for overlay */
  border-radius: 15px; /* Add rounded edges */
  overflow: hidden; /* Ensure the corners are rounded */
  margin: 20px; /* Optional: adds some space around the header */
}

.header:before {
  content: ""; /* Create a pseudo-element */
  position: absolute; /* Position it absolutely */
  top: 0; /* Align to the top */
  left: 0; /* Align to the left */
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  background-color: rgba(0, 0, 0, 0.5); /* Dark overlay */
  z-index: 1; /* Ensure it stays behind the text */
}

.header-content {
  position: relative; /* Position relative for text layering */
  z-index: 2; /* Ensure text stays above the overlay */
}

.header-buttons {
  margin-top: 20px; /* Space between text and buttons */
}

.row {
  justify-content: center; /* Center the cards in the row */
}

.card {
  margin-top: 20px;
  min-height: 430px;
  border: none; /* Remove default border */
  border-radius: 10px; /* Rounded corners for cards */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
  transition: transform 0.3s; /* Animation for hover effect */
}

.card:hover {
  transform: scale(1.05); /* Scale effect on hover */
}

.card img {
  max-height: 200px;
  object-fit: cover;
  border-top-left-radius: 10px; /* Rounded top corners */
  border-top-right-radius: 10px; /* Rounded top corners */
}

.btn-primary {
  background-color: #007bff; /* Primary button color */
  border: none;
  transition: background-color 0.3s; /* Smooth transition */
}

.btn-primary:hover {
  background-color: #0056b3; /* Darker shade on hover */
}

.btn-secondary {
  background-color: #fd7e14; /* Secondary button color */
  border: none;
}

.btn-secondary:hover {
  background-color: #e86c0f; /* Darker shade on hover */
}

.card-body {
  text-align: center; /* Center text in cards */
}



#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  padding-top: 60px;
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
