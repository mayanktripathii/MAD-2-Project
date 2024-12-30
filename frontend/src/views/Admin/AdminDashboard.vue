

<template>
<div style="margin-top: 5.5em;">
  <Logout DashboardTitle="Admin Dashboard"></Logout>
  <div class="dashboard container mt-5">
    <div v-if="stats" class="row">
  <div class="col-md-6 col-lg-4 mb-3" v-for="(value, key) in {
    'Total Users': stats.total_users,
    'Total Sponsors': stats.total_sponsors,
    'Public Campaigns': stats.total_campaigns_public,
    'Private Campaigns': stats.total_campaigns_private,
    'Pending Ad Requests': stats.total_ad_requests_pending ,
    'Flagged User': stats.flagged_users,
  }" :key="key">
    <div class="card shadow-sm h-100">
      <div class="card-body d-flex flex-column justify-content-between">
        <h5 class="card-title text-center">{{ key }}</h5>
        <p class="card-text text-center display-4">{{ value }}</p>
      </div>
    </div>
  </div>



      <!-- New Row for Pending Sponsors Approval -->
<div class="row">
  <div class="col-md-12 col-lg-4 offset-lg-4 mb-3" style="margin-left: 11.67cm;">
    <div class="card highlight">
      <div class="card-body">
        <h5 class="card-title text-center">
          <a
            href="http://localhost:8080/admin/pending_sponsors"
            class="highlight-link"
          >Pending Sponsors Approval</a>
        </h5>
        <p class="card-text text-center">{{ stats.pending_sponsors }}</p>
      </div>
    </div>
  </div>
</div>
</div>
    <div v-else>
      <p>Loading...</p>
    </div>
    
    

    <div style="margin-top: 1em;margin-bottom: 1em;">
      <h1 style="font-weight: bold;">All Users Registered on Sponsorly</h1>
    </div>

    <h2>Admins</h2>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>User ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="adminItem in admin" :key="adminItem.id">
          <td>{{ adminItem.id }}</td>
          <td>{{ adminItem.username }}</td>
          <td>{{ adminItem.email }}</td>
          <td>{{ adminItem.created_at }}</td>
          <td>
            <button class="flag-button" @click="flagUser(adminItem.id)">Flag User</button>
          </td>
        </tr>
      </tbody>
    </table>

    <h2>Influencers</h2>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>User ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="influencerItem in influencer" :key="influencerItem.id">
          <td>{{ influencerItem.id }}</td>
          <td>{{ influencerItem.username }}</td>
          <td>{{ influencerItem.email }}</td>
          <td>{{ influencerItem.created_at }}</td>
          <td>
            <button class="flag-button" @click="flagUser(influencerItem.id)">Flag User</button>
          </td>
        </tr>
      </tbody>
    </table>

    <h2>Sponsors</h2>
    <table class="table table-bordered">
      <thead>
        <tr>
          <th>User ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sponsorItem in sponsor" :key="sponsorItem.id">
          <td>{{ sponsorItem.id }}</td>
          <td>{{ sponsorItem.username }}</td>
          <td>{{ sponsorItem.email }}</td>
          <td>{{ sponsorItem.created_at }}</td>
          <td>
            <button class="flag-button" @click="flagUser(sponsorItem.id)">Flag User</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  </div>
</template>



<script setup>
import Logout from "../Logout/performLogout.vue";
import { ref, onMounted } from 'vue';
import axios from 'axios';

const stats = ref(null);
const admin = ref([]);
const influencer = ref([]);
const sponsor = ref([]);

const fetchStats = async () => {
  try {
    const response = await axios.get("http://localhost:5000/admin/dashboard/data", {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    });
    stats.value = response.data;
  } catch (error) {
    console.error("Failed to fetch dashboard data:", error);
  }
};

const fetchUsers = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/api/users');
    admin.value = response.data.admin;
    influencer.value = response.data.influencer;
    sponsor.value = response.data.sponsor;
  } catch (error) {
    console.error("Error while fetching users:", error);
  }
};

// Fetch data when component is mounted
onMounted(() => {
  fetchStats();
  fetchUsers();
});

// Define flagUser function
const flagUser = async (userId) => {
  const reason = prompt('Enter reason for flagging:');
  if (reason) {
    try {
      const response = await axios.post('http://localhost:5000/admin/flag_user', { user_id: userId, reason }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      alert('User flagged successfully!');
      console.log(response.data);
    } catch (error) {
      console.error('Error flagging user:', error);
      alert('Failed to flag user.');
    }
  }
};
</script>

<style scoped>

.card {
  border-radius: 10px; /* Rounded corners for the cards */
  background-color: #f8f9fa; /* Light background color */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Light shadow effect */
}

.card-title {
  font-size: 1.25rem; /* Slightly larger font for titles */
  color: #495057; /* Dark color for the title */
  font-weight: bold; /* Make the title bold */
}

.card-text {
  font-size: 2rem; /* Increase the font size of the values */
  color: #007bff; /* Blue color for values */
  font-weight: bold;
}

.card-body {
  padding: 20px;
}

.card-body .text-center {
  text-align: center;
}

.display-4 {
  font-size: 2rem; /* Larger font size for the numbers */
}

.row {
  margin-top: 20px; /* Spacing from the top */
}

@media (max-width: 768px) {
  .col-md-6 {
    margin-bottom: 15px; /* Extra spacing on small screens */
  }
}


.highlight {
  border: 2px solid blueviolet; /* Highlight border color */
}

.highlight-link {
  color: #ffcc00; /* Highlight link color */
  font-weight: bold;
}

.flag-button {
  background-color:  #007bff; /* Example color */
  color: #fff;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

</style>