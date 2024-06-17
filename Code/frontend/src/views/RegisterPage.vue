<template>
<NavBar />
  <div class="container my-5">
    <div class="col-md-6">
      <div class="card">
        <div class="card-body">
          <h2 class="card-title text-center">REGISTER</h2>
          <form @submit.prevent="signup"> 
            <div class="mb-2">
              <label for="name" class="form-label">Name</label>
              <input
                type="text"
                id="name"
                class="form-control"
                v-model="name" 
                required 
              />
            </div>
            <div class="mb-2">
              <label for="email" class="form-label">Email</label>
              <input
                type="email"
                id="email"
                class="form-control"
                v-model="email"
                required
              />
            </div>
            
            <div class="mb-2">
              <label for="password" class="form-label">password</label>
              <input
                type="password"
                id="password"
                class="form-control"
                v-model="password"
                required
              />
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
export default {
    components: {
    NavBar,
  },
  data() {
    return {
      name: "",
      email: "",
      password: "",

    };
  },
  methods: {
    async signup() {
      const formdata = {
        email: this.email,
        name: this.name,
        password: this.password,

      };
      try {
        const response = await fetch("http://127.0.0.1:5000/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formdata),
        });
        console.log(formdata);
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          this.$router.push("/login");
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error("Registration error:", error);
        alert("An error occurred while attempting to register.");
      }
    },
  },
};
</script>

<style scoped></style>
