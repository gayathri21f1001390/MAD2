<template>
<NavBar />
    <div class="container mt-5">
      <h2>Create Category</h2>
      <form @submit.prevent="createSection" class="mt-3">
          <div class="form-group row">
            <label for="section-name" class="col-sm-2 form-label">Section Name</label>
            <div class="col-sm-10">
              <input v-model="section_name" type="text" class="form-control" id="section_name" required>
            </div>
          </div>
          <div class="form-group row">
            <label for="Section-desc" class="col-sm-2 form-label">Section Description</label>
            <div class="col-sm-10">
              <input v-model="section_desc" type="text" class="form-control" id="section_desc" required>
            </div>
          </div>

          <div class="form-group row">
            <div class="col-sm-10">
              <button type="submit" class="btn btn-primary">Create Section</button>
            </div>
          </div>  
      </form>
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
        sectionName: '',
      };
    },
    methods: {
      async createSection() {
        try {
          const response = await fetch('http://127.0.0.1:5000/section', {
            method: 'POST',
            headers: {
              'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              name: this.section_name,
              description: this.section_desc
            }),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            alert(data.message);
            
           this.$router.push('/view_sections');
       

          } else {
            alert('Error: ' + data.error);
          }
        } catch (error) {
          console.error('Create section error:', error);
          alert('An error occurred while creating the section.');
        }
      },
    },
  };
  </script>
  
  <style>
  /* Add your custom styles here */
  </style>
  