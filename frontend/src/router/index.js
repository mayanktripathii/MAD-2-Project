import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupUser from '../views/SignupUser.vue'
import LoginUser from '../views/LoginUser.vue'
import AdminLogin from '../views/Admin/AdminLogin.vue'
import SponsorLogin from '../views/Sponsor/SponsorLogin.vue'
import SponsorRegistration from '../views/Sponsor/SponsorRegistration.vue'
import InfluLogin from '../views/Influencer/InfluLogin.vue'
import InflueRegister from '../views/Influencer/InfluRegister.vue'
import AdminDashboard from '../views/Admin/AdminDashboard.vue'
import Logout from '../views/Logout/performLogout.vue'
import AdminPendingSponsor from '../views/Admin/AdminPendingSponsor.vue'
import SponsorDashboard from '../views/Sponsor/SponsorDashboard.vue'
import SponsorAddCampaign from '../views/Sponsor/SponsorAddCampaign.vue'
import SponsorEditCampaign from '@/views/Sponsor/SponsorEditCampaign.vue'
import SearchInfluencer from '@/views/Sponsor/SearchInfluencer.vue'
import SponsorAdRequest from '@/views/Sponsor/SponsorAdRequest.vue'
import SponsorEditAdRequest from '@/views/Sponsor/SponsorEditAdRequest.vue'
import SponsorAdd_AdRequest from '@/views/Sponsor/SponsorAdd_AdRequest.vue'



import InfluDashboard from '../views/Influencer/InfluDashboard.vue'
import InfluProfile from '../views/Influencer/InfluProfile.vue'
import SearchPublicCampaigns from '@/views/Influencer/SearchPublicCampaigns.vue'
import InfluAccept from '@/views/Influencer/InfluAccept.vue'
import InfluReject from '@/views/Influencer/InfluReject.vue'
import InfluNego from '@/views/Influencer/InfluNego.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  
  { path: "/logout", name: "Logout", component: Logout },

  {
    path: '/signup',
    name: 'signup',
    component: SignupUser
  },
  {
    path: '/login',
    name: 'login',
    component: LoginUser
  },

  // Admin paths
   {
    path: "/admin/login",
    name: "AdminLogin",
    component: AdminLogin,
  },
  {
    path: "/admin/dashboard",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true, role: "admin" },
  },
  {
    path: "/admin/pending_sponsors",
    name: "AdminPendingSponsor",
    component: AdminPendingSponsor,
    meta: { requiresAuth: true, role: "admin" },
  },


  // Sponsor paths
  {
    path: "/sponsor/login",
    name: "SponsorLogin",
    component: SponsorLogin,
  },

  {
    path: "/sponsor/register",
    name: "SponsorRegistration",
    component: SponsorRegistration,
  },
  {
    path: "/sponsor/dashboard",
    name: "SponsorDashboard",
    component: SponsorDashboard,
    meta: { requiresAuth: true, role: "sponsor" },
  },
  {
    path: "/sponsor/addcampaign",
    name: "SponsorAddCampaign",
    component: SponsorAddCampaign,
    meta: { requiresAuth: true, role: "sponsor" },
  },
  {
    path: "/sponsor/editcampaign/:campaign_id",
    name: "SponsorEditCampaign",
    component: SponsorEditCampaign,
    meta: { requiresAuth: true, role: "sponsor" },
  },
  {
    path: "/sponsor/search_influencer",
    name: "SearchInfluencer",
    component: SearchInfluencer,
    meta: { requiresAuth: true, role: "sponsor" },
  },
  {
  path: "/sponsor/adrequest/:campaign_id",
  name: "SponsorAdRequest",
  component: SponsorAdRequest,
  meta: { requiresAuth: true, role: "sponsor" },
},
{
  path: "/sponsor/edit_adrequest_data/:ad_request_id",
  name: "SponsorEditAdRequest",
  component: SponsorEditAdRequest,
  meta: { requiresAuth: true, role: "sponsor" },
},
{
  path: "/sponsor/add_adRequest_data/:campaign_id",
  name: "SponsorAddAdRequestData",
  component: SponsorAdd_AdRequest,
  meta: { requiresAuth: true, role: "sponsor" },
},

  // Influencer paths
  {
    path: "/influencer/login",
    name: "InfluLogin",
    component: InfluLogin,
  },

  {
    path: "/influencer/register",
    name: "InflueRegister",
    component: InflueRegister,
  },
  {
    path: "/influencer/dashboard",
    name: "InfluDashboard",
    component: InfluDashboard,
    meta: { requiresAuth: true, role: "influencer" },
  },
  {
    path: "/influencer/profile",
    name: "InfluProfile",
    component: InfluProfile,
    meta: { requiresAuth: true, role: "influencer" },
  },
  {
    path: "/influencer/search_pubcamp",
    name: "SeachPubCamp",
    component: SearchPublicCampaigns,
    meta: { requiresAuth: true, role: "influencer" },
  },
  {
    path: "/influencer/acceptAdRequest/:ad_request_id",
    name: "InfluAccept",
    component: InfluAccept,
    meta: { requiresAuth: true, role: "influencer" },
  },

  {
    path: "/influencer/rejectAdRequest/:ad_request_id",
    name: "InfluReject",
    component: InfluReject,
    meta: { requiresAuth: true, role: "influencer" },
    },
    {
      path: "/influencer/negoAdRequest/:ad_request_id",
      name: "InfluNego",
      component: InfluNego,
      meta: { requiresAuth: true, role: "influencer" },
    },


  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]


// Router guard to check if a route requires authentication


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
