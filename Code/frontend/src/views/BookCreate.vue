<template>
<NavBar />
    <div class="container mt-5">
      <h2>Create Book</h2>
      <form @submit.prevent="createBook" class="mt-3">
          <div class="form-group row">
            <label for="book-name" class="col-sm-2 form-label">Book Name</label>
            <div class="col-sm-10">
              <input v-model="book_name" type="text" class="form-control" id="book_name" required>
            </div>
          </div>
          <div class="form-group row">
            <label for="book_content" class="col-sm-2 form-label">Content</label>
            <div class="col-sm-10">
              <input v-model="book_content" type="text" class="form-control" id="book_content" required>
            </div>
          </div>
          <div class="form-group row">
            <label for="authors" class="col-sm-2 form-label">Authors(, seperated)</label>
            <div class="col-sm-10">
              <input v-model="authors" type="text" class="form-control" id="authors" required>
            </div>
          </div>
          <div class="form-group row">
            <label for="book_path" class="col-sm-2 form-label">Book Path"</label>
            <div class="col-sm-10">
              <input v-model="book_path" type="text" class="form-control" id="book_content" required>
            </div>
          </div> 

          <div class="form-group row">
            <div class="col-sm-10">
              <button type="submit" class="btn btn-primary">Create Book</button>
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
   
        book:{
        book_name: "",
        book_content: "",
        authors: "",
        book_path: "",
        },
      };
    },



    methods: {

      async createBook() {
        try {
          const sectionId = this.$route.params.id;
          const response = await fetch(`http://127.0.0.1:5000/book/${sectionId}`, {
                   
            method: 'POST',
            headers: {
              'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              name: this.book_name,
              content: this.book_content,
              authors: this.authors,
              book_path: this.book_path,
            }),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            alert(data.message);
            
            this.$router.push({name: "view_section_books", params: {id: this.section_id}});
      
          } else {
            alert('Error: ' + data.error);
          }
        } catch (error) {
          console.error('Create book error:', error);
          alert('An error occurred while creating the book.');
        }
      },
    },
  };
  </script>
  
  <style>
  /* Placeholder for custom sytles */
  </style>
  