<template>
    <NavBar />
    <div class="container mt-5">
      <h2>Update Section</h2>
      <form @submit.prevent="updateSection" class="mt-3">
          <div class="form-group row">
            <label for="section-name" class="col-sm-2 form-label">Section Name</label>
            <div class="col-sm-10">
              <input v-model="section_name" type="text" class="form-control" id="section_name" placeholder="section_name">
            </div>
          </div>
          <div class="form-group row">
            <label for="section-name" class="col-sm-2 form-label">Section Name</label>
            <div class="col-sm-10">
              <input v-model="section_description" type="text" class="form-control" id="section_description" placeholder="section_description">
            </div>
          </div>
          <div class="form-group row">
            <div class="col-sm-10">
              <button type="submit" class="btn btn-primary">Update Section</button>
            </div>
          </div> 
     </form>
   </div> 

</template>

<script>
export default {
    data() {
      return {
        section_name: "",
        section_description: "",
      };
    },
    mounted() {
      const sectionId = this.$route.params.id;
      this.getSectionDetails(sectionId);
    },
    methods: {
      getSectionDetails(sectionId) {
        const token = localStorage.getItem("access_token");
        console.log("TOKEN" + token)
        if (!token) {
          console.error("Access token is null");
          return;
        }
  
        fetch(`http://127.0.0.1:5000/section/${sectionId}`, {
          method: 'GET',
          headers: {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
          },
        })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
          })
          .then(data => {
            this.section_name = data.section.name;
            this.section_description = data.section.description;

          })
          .catch(error => {
            console.error(`Error fetching category details for ID ${sectionId}:`, error);
          });
      },
      updateSection() {
        
        const sectionId = this.$route.params.id;
        fetch(`http://127.0.0.1:5000/section/${sectionId}`, {
          method: 'PUT',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.section_name,
            description: this.section_description
          }),
        })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            console.log(`Section with ID ${sectionId} updated successfully`);
            this.$router.push('/view_sections');
          })
          .catch(error => {
            console.error(`Error updating section with ID ${sectionId}:`, error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Placeholder for custom styles */
  </style>
  