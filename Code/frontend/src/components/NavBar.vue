<template>
<nav class="navbar navbar-expand-sm">
  <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav mr-auto">
        <li v-if="this.loggedin" class="nav-item">
          <a class="nav-link disabled" href="#">{{this.username}} Profile</a>
        </li>
        <li v-if="this.loggedin" class="nav-item">
          <router-link class="nav-link" to="/">Home</router-link>
        </li>
        <li v-if="!this.loggedin" class="nav-item-register">
          <router-link class="nav-link" to="/register">Register</router-link>
        </li>
        <li v-if="!this.loggedin" class="nav-item-login">
          <router-link class="nav-link" to="/login">Login</router-link>
        </li>
        <li v-if="this.islibrarian" class="nav-item-login">
          <router-link class="nav-link" to="/create_section">Create Section
          </router-link>
        </li>
        <li 
         class="nav-item-login">
          <router-link class="nav-link" to="/view_sections">View Sections
          </router-link>
        </li>
      <li v-if="this.isuser"
        class="nav-item-login">
          <router-link class="nav-link" to="/view_books">View Books
          </router-link>
      </li>
      <li v-if="this.isuser"
        class="nav-item-login">
        <router-link class="nav-link" to="/book_request_user">My Books </router-link>
      </li>
      <li v-if="this.islibrarian"
        class="nav-item-login">
        <router-link class="nav-link" to="/book_request_status">Librarian Dashboard </router-link>
      </li>
       <li  v-if="this.loggedin" class="nav-item-logout">
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
