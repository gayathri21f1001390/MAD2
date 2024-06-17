<template>
    <NavBar />
    <div class="container mt-5">
      <h2>Update Book</h2>
      <form @submit.prevent="updateBook" class="mt-3">
          <div class="form-group row">
            <label for="book-name" class="col-sm-2 form-label">Book Name</label>
            <div class="col-sm-10">
              <input v-model="book_name" type="text" class="form-control" id="book_name" placeholder="book_name">
            </div>
          </div>
          <div class="form-group row">
            <label for="book_content" class="col-sm-2 form-label">Content</label>
            <div class="col-sm-10">
              <input v-model="book_content" type="text" class="form-control" id="book_content" placeholder="book_content">
            </div>
          </div>
          <div class="form-group row">
            <label for="authors" class="col-sm-2 form-label">Authors(, seperated)</label>
            <div class="col-sm-10">
              <input v-model="authors" type="text" class="form-control" id="authors" placeholder="authors">
            </div>
          </div>
          <div class="form-group row">
            <label for="book_path" class="col-sm-2 form-label">Book Path</label>
            <div class="col-sm-10">
              <input v-model="book_path" type="text" class="form-control" id="book_content" placeholder="book_path">
            </div>
          </div>
          <div class="form-group row">
            <div class="col-sm-10">
              <button type="submit" class="btn btn-primary">Update Book</button>
            </div>
          </div> 
     </form>
   </div> 

</template>

<script>
export default {
    data() {
      return {
        book_id:"",
        book_name: "",
        book_content: "",
        authors: "",
        book_path: "",
        section_id: "",
      };
    },
    mounted() {
      const bookId = this.$route.params.id;
      this.getBookDetails(bookId);
    },
    methods: {
      getBookDetails(bookId) {
        const token = localStorage.getItem("access_token");
  
        if (!token) {
          console.error("Access token is null");
          return;
        }
  
        fetch(`http://127.0.0.1:5000/book/${bookId}`, {
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
            console.log(data)
            this.book_id = data.book.id;
            this.book_name = data.book.name;
            this.book_content = data.book.content;
            this.authors = data.book.authors;
            this.book_path = data.book.book_path;
            this.section_id = data.book.section_id;
          })
          .catch(error => {
            console.error(`Error fetching category details for ID ${this.book.id}:`, error);
          });
      },
      updateBook() {
     
        const bookId = this.$route.params.id;
        const sectionId = this.section_id
        console.log("in updateBook")
        console.log(bookId)
        console.log(sectionId)
        
        fetch(`http://127.0.0.1:5000/book/${bookId}`, {
          method: 'PUT',
          headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.book_name,
            content: this.book_content,
            authors: this.authors,
            book_path: this.book_path,
            section_id: this.section_id
          }),
        })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            console.log(`Book with ID ${bookId} updated successfully`);

            this.$router.push({name: "view_section_books", params: {id: sectionId}});
            
          })
          .catch(error => {
            console.error(`Error updating book with ID ${bookId}:`, error);
          });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Placeholder for custom styles hee */
  </style>
  
  