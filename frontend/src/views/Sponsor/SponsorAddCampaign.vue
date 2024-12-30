<script setup>
import Logout from "@/views/Logout/performLogout.vue";
</script>

<template>
    <div>
      <Logout DashboardTitle="Sponsor Manage Campaign"></Logout>
    </div>
  
    <div class="wrapper" style="margin-top: 2em;">
      <h2>Add New Campaign</h2>
      <form @submit.prevent="submitCampaign">
        <div class="form-row">
          <!-- Left Column (Fields) -->
          <div class="left-column">
            <div class="input-box">
              <input
                type="text"
                v-model="campaign.name"
                placeholder="Campaign Name"
                required
              />
            </div>
  
            <div class="input-box">
              <textarea
                v-model="campaign.description"
                placeholder="Campaign Description"
                required
              ></textarea>
            </div>
  
            <div class="input-box">
              <textarea
                v-model="campaign.goals"
                placeholder="Campaign Goals"
                required
              ></textarea>
            </div>
  
            <div class="input-box">
              <input
                type="number"
                v-model="campaign.budget"
                placeholder="Campaign Budget"
                min="0"
                required
              />
            </div>
          </div>
  
          <!-- Right Column (Fields) -->
          <div class="right-column">
            <div class="input-box">
              <label>Campaign Visibility:</label><br />
              <div class="visibility-options">
                <div class="form-check" style="margin-left: 8em;margin-top: 1em;">
                  <input
                    class="form-check-input"
                    type="radio"
                    id="public"
                    value="public"
                    v-model="campaign.visibility"
                    required
                  />
                  <label class="form-check-label" for="public">Public</label>
                </div>
                <div class="form-check" style="margin-left: 8em;">
                  <input
                    class="form-check-input"
                    type="radio"
                    id="private"
                    value="private"
                    v-model="campaign.visibility"
                    required
                  />
                  <label class="form-check-label" for="private">Private</label>
                </div>
              </div>
            </div>
  
            <div class="input-box">
              <input
                type="date"
                v-model="campaign.start_date"
                placeholder="Campaign Start Date"
                required
              />
            </div>
  
            <div class="input-box">
              <input
                type="date"
                v-model="campaign.end_date"
                placeholder="Campaign End Date"
                required
              />
            </div>
          </div>
        </div>
  
        <div class="input-box button">
          <input type="submit" value="Submit" :disabled="!isFormValid" />
        </div>
  
        <!-- Error and Success Message -->
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
        <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
      </form>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    name: "AddCampaign",
    data() {
      return {
        campaign: {
          name: "",
          description: "",
          goals: "",
          budget: 0,
          visibility: "public",
          start_date: "",
          end_date: "",
        },
        messages: [],
        successMessage: "",
        errorMessage: "",
      };
    },
    computed: {
      isFormValid() {
        return (
          this.campaign.name &&
          this.campaign.description &&
          this.campaign.goals &&
          this.campaign.budget &&
          this.campaign.visibility &&
          this.campaign.start_date &&
          this.campaign.end_date
        );
      },
    },
    methods: {
      async submitCampaign() {
        try {
          const response = await axios.post(
            "/sponsor/addcampaign",
            this.campaign,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`,
              },
            }
          );
          if (response.data.success) {
            this.successMessage =
              "Campaign Added successfully! Redirecting to Dashboard...";
            this.messages = [];
            setTimeout(() => {
              this.$router.push("/sponsor/dashboard");
            }, 3000);
          } else {
            this.messages = response.data.messages || ["An error occurred"];
          }
        } catch (error) {
          console.error("Error submitting campaign:", error);
          this.messages = ["An error occurred"];
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
  
  .input-box input,
  .input-box textarea {
    width: 100%;
    padding: 15px;
    font-size: 17px;
    border: 1.5px solid #c7bebe;
    border-radius: 6px;
    transition: all 0.3s ease;
    color: #333;
  }
  
  .input-box textarea {
    height: 100px;
  }
  
  .input-box input:focus,
  .input-box textarea:focus,
  .input-box input:valid,
  .input-box textarea:valid {
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
  
  .visibility-options {
    display: flex;
    flex-direction: column;
  }
  
  .form-check {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .form-check input {
    margin-right: 8px;
    transform: scale(0.7); /* Keep the default size for radio buttons */
    border-radius: 60%; /* Ensures the radio buttons are perfectly circular */
    width: 20px;
    height: 20px;
    border: 2px solid #4070f4;
    background-color: #fff;
    transition: all 0.3s ease;
  }
  
  .form-check input:checked {
    background-color: #4070f4; /* Change background on checked */
    border-color: #4070f4;    /* Border color when checked */
  }
  
  .form-check input:hover {
    background-color: #5c8df0;
    border-color: #5c8df0;
  }
  
  .form-check label {
    font-size: 16px;
    color: #333;
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
  