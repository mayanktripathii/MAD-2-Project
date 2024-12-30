<template>
    <div class="container">
      <h2 class="my-4 text-center text-primary">Ad Request Negotiation</h2>
  
      <!-- Flash messages -->
      <div v-if="flashMessages.length" class="alert alert-info">
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
          <dd class="col-sm-8">
            <span v-if="adRequest.negotiated_amount">${{ adRequest.negotiated_amount }}</span>
            <span v-else class="text-muted">Not yet proposed</span>
          </dd>
  
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
          <dd class="col-sm-8">
            <span
              class="badge"
              :class="{
                'badge-warning': adRequest.negotiation_status === 'pending',
                'badge-success': adRequest.negotiation_status === 'approved',
                'badge-danger': adRequest.negotiation_status === 'rejected'
              }"
            >
              {{ adRequest.negotiation_status }}
            </span>
          </dd>
        </dl>
  
        <!-- Negotiation Form -->
        <div v-if="adRequest.negotiation_status === 'pending'" class="mt-4">
          <div class="form-group">
            <label for="negotiationAmount" class="form-label">Propose New Amount:</label>
            <input
              type="number"
              id="negotiationAmount"
              v-model.number="negotiationAmount"
              class="form-control"
              placeholder="Enter your proposed amount"
              min="0"
            />
          </div>
          <div class="text-center mt-3">
            <button type="button" class="btn btn-primary btn-lg" @click="negotiateAdRequest">
              Propose Amount
            </button>
          </div>
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
  const negotiationAmount = ref(null);
  const route = useRoute();
  const router = useRouter();
  const adRequestId = route.params.ad_request_id;
  
  const fetchAdRequestDetails = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.get(
        `/influencer/acceptAdRequest/${adRequestId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      adRequest.value = response.data;
    } catch (error) {
      console.error("Error fetching ad request details:", error);
    }
  };
  
  const negotiateAdRequest = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await axios.post(
        `/influencer/negoAdRequest/${adRequestId}`,
        new URLSearchParams({
          nego_amount: negotiationAmount.value,
        }),
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      flashMessages.value = [response.data.message];
  
      // Refresh ad request details after negotiation
      fetchAdRequestDetails();
      setTimeout(() => {
        router.push("/influencer/dashboard");
      }, 3000);
    } catch (error) {
      console.error("Error proposing new amount:", error);
      flashMessages.value = ["Error proposing new amount. Please try again."];
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
  
  .badge-warning {
    background-color: #ffc107;
  }
  
  .badge-danger {
    background-color: #dc3545;
  }
  
  .form-label {
    font-weight: bold;
  }
  
  .form-control {
    border-radius: 5px;
  }
  
  .text-center {
    text-align: center;
  }
  </style>
  