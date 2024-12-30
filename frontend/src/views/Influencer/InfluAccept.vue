<template>
    <div class="container">
      <h2 class="my-4 text-center text-primary">Ad Request Details</h2>
  
      <!-- Flash messages -->
      <div v-if="flashMessages.length" class="alert alert-success">
        <ul class="mb-0">
          <li v-for="message in flashMessages" :key="message">{{ message }}</li>
        </ul>
      </div>
  
      <!-- Ad request details -->
      <div v-if="adRequest" class="card shadow-lg p-4">
        <dl class="row">
          <dt class="col-sm-4">Campaign Name:</dt>
          <dd class="col-sm-8">{{ adRequest.campaign_name }}</dd>
  
          <dt class="col-sm-4">Description:</dt>
          <dd class="col-sm-8">{{ adRequest.description }}</dd>
  
          <dt class="col-sm-4">Start Date:</dt>
          <dd class="col-sm-8">{{ formatDate(adRequest.start_date) }}</dd>
  
          <dt class="col-sm-4">End Date:</dt>
          <dd class="col-sm-8">{{ formatDate(adRequest.end_date) }}</dd>
  
          <dt class="col-sm-4">Goals:</dt>
          <dd class="col-sm-8">{{ adRequest.goals }}</dd>
  
          <dt class="col-sm-4">Niche:</dt>
          <dd class="col-sm-8">{{ adRequest.niche }}</dd>
  
          <dt class="col-sm-4">Sponsor Name:</dt>
          <dd class="col-sm-8">{{ adRequest.sponsor_name }}</dd>
  
          <dt class="col-sm-4">Messages:</dt>
          <dd class="col-sm-8">{{ adRequest.messages }}</dd>
  
          <dt class="col-sm-4">Payment Amount:</dt>
          <dd class="col-sm-8">${{ adRequest.payment_amount }}</dd>
  
          <dt class="col-sm-4">Negotiated Amount:</dt>
          <dd class="col-sm-8">${{ adRequest.negotiated_amount }}</dd>
  
          <dt class="col-sm-4">Requirements:</dt>
          <dd class="col-sm-8">{{ adRequest.requirements }}</dd>
  
          <dt class="col-sm-4">Status:</dt>
          <dd class="col-sm-8">
            <span
              class="badge"
              :class="{
                'badge-primary': adRequest.status === 'Pending',
                'badge-success': adRequest.status === 'Accepted',
                'badge-danger': adRequest.status === 'Rejected'
              }"
            >
              {{ adRequest.status }}
            </span>
          </dd>
  
          <dt class="col-sm-4">Negotiation Status:</dt>
          <dd class="col-sm-8">{{ adRequest.negotiation_status }}</dd>
        </dl>
  
        <div class="text-center mt-4">
          <button type="button" class="btn btn-success btn-lg" @click="acceptAdRequest">
            Accept Ad Request
          </button>
        </div>
      </div>
  
      <div v-else class="text-center text-muted mt-4">
        <p>Loading ad request details...</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import axios from "axios";
  import { useRoute, useRouter } from "vue-router";
  
  const adRequest = ref(null);
  const flashMessages = ref([]);
  const route = useRoute();
  const router = useRouter();
  const adRequestId = route.params.ad_request_id;
  
  const fetchAdRequestDetails = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get(`/influencer/acceptAdRequest/${adRequestId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      adRequest.value = response.data;
    } catch (error) {
      console.error("Error fetching ad request details:", error);
    }
  };
  
  const acceptAdRequest = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.post(
        `http://localhost:5000/influencer/acceptAdRequest/${adRequestId}`,
        {},
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      flashMessages.value = [response.data.message];
      setTimeout(() => {
        router.push("/influencer/dashboard");
      }, 3000);
    } catch (error) {
      console.error("Error accepting ad request:", error);
      flashMessages.value = ["Error accepting ad request. Please try again."];
    }
  };
  
  const formatDate = (dateString) => {
    const options = { year: "numeric", month: "long", day: "numeric" };
    return new Date(dateString).toLocaleDateString(undefined, options);
  };
  
  onMounted(() => {
    fetchAdRequestDetails();
  });
  </script>
  
  <style scoped>
  .container {
    max-width: 800px;
    margin: 20px auto;
  }
  
  h2 {
    font-weight: bold;
  }
  
  .card {
    background: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
  
  .badge {
    padding: 0.5em 1em;
    font-size: 0.9em;
  }
  
  .badge-primary {
    background-color: #007bff;
  }
  
  .badge-success {
    background-color: #28a745;
  }
  
  .badge-danger {
    background-color: #dc3545;
  }
  
  .text-center {
    text-align: center;
  }
  </style>
  