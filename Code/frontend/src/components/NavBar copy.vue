<template>
<nav class="navbar navbar-expand-sm">
  <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li v-if="!this.loggedin" class="nav-item-register">
          <router-link class="nav-link" to="/register">Register</router-link>
        </li>
        <li v-if="!this.loggedin" class="nav-item-login">
          <router-link class="nav-link" to="/login">Login</router-link>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Dropdown
          </a>
          <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            <router_link class="dropdown-item" to="#">Action</router_link>
        
            <div class="dropdown-divider"></div>
             <a class="dropdown-item" href="#">Something else here</a>
          </div>
      </li>

       <li v-if="this.loggedin" class="nav-item-logout">
          <a @click="logout" class="nav-link" > Logout </a>
        </li>

      </ul>
    </div>
</nav>
</template>

<script>
import UserMixin from "../mixins/userMixin";

export default {
  mixins: [UserMixin],
};
</script>

<style>
.navitems {
  display: flex;
  align-items: center;
}

.navitems a {
  margin-left: 15px;
}
</style>
