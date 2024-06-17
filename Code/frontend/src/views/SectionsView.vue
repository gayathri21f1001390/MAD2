<template>
    <NavBar />
    <h2> Sections <button v-if="this.islibrarian" class="btn btn-outline-primary" @click="createSection()">Create New Section</button> </h2>
    <div class="sections mt-5">
    
      <table class="table table-bordered table-hover">
        <thead class="thead-light">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Action(s)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="section in sections" :key="section.id">
            <td>{{ section.id }}</td>
            <td>{{ section.name }}</td>
            <td>{{ section.description}}</td>
            <td>
              <div class="btn-group" role="group">
                <button v-if="this.islibrarian" class="btn btn-outline-primary" @click="updateSection(section.id)">Update</button>
                <button v-if="this.islibrarian" class="btn btn-outline-danger" @click="deleteSection(section.id)">Delete</button>
                <button  class="btn btn-outline-danger" @click="getBooks(section.id)">Books</button>

              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>

  <script>
  
  import userMixins from '../mixins/userMixin';
  import NavBar from '../components/NavBar.vue';
  
  export default{
    mixins: [userMixins],
    data(){
        return{
            sections: [],
        };
    },
    mounted() {
        this.getSections();
    },
    methods: {
        getSections() {
            fetch('http://127.0.0.1:5000/section', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                this.sections = data.sections;
            })
            .catch(error => {
                console.error('Error:', error);
            })
        },
    updateSection(sectionId) {
      this.$router.push({ name: 'update_section', params: { id: sectionId } });
    },
    createSection() {
      this.$router.push("/create_section");
    },
    getBooks(sectionId) {
      this.$router.push({ name: 'view_section_books', params: { id: sectionId } });
    },
    deleteSection(sectionId) {
      fetch(`http://127.0.0.1:5000/section/${sectionId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          'Content-Type': 'application/json',
        },
      })
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          console.log(`Section with ID ${sectionId} deleted successfully`);
          this.getSections();
        })
        .catch(error => {
          console.error(`Error deleting section with ID ${sectionId}:`, error);
        });
    },
    }
  }
  </script>