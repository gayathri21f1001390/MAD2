<template>
    <NavBar />
    <h2> Books in {{ sectionName }} section <button v-if="this.islibrarian" class="btn btn-outline-primary" @click="createBook(sectionId)"> Create New Book</button> </h2>
    <div class="sections mt-5">
    
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Content</th>
            <th>Authors</th>
            <th>Book Path</th>
            <th>Action(s)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.id">
            <td>{{ book.id }}</td>
            <td>{{ book.name }}</td>
            <td>{{ book.content}}</td>
            <td>{{ book.authors}}</td>
            <td>{{ book.book_path}}</td>
            <td>
              <div class="btn-group" role="group">
                <button v-if="this.islibrarian" class="btn btn-outline-primary" @click="updateBook(book.id)">Update</button>
                <button v-if="this.islibrarian" class="btn btn-outline-danger" @click="deleteBook(book.id)">Delete</button>
                
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
            sectionName: "",
            books: [],
        };
    },
    mounted() {
        const sectionId = this.$route.params.id;
        this.getBooks(sectionId)
    },
    methods: {
        getBooks(sectionId) {
            fetch(`http://127.0.0.1:5000/section/${sectionId}`, {
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
                this.sectionName = data.section.name;
            })
            .catch(error => {
                console.error('Error:', error);
            })
            fetch(`http://127.0.0.1:5000/book/section/${sectionId}`, {
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
                this.books = data.books;
            })
            .catch(error => {
                console.error('Error:', error);
            })
        },
        createBook(sectionId) {
          this.$router.push({name: "create_book", params: { id:sectionId }});
        },
        requestBook(book_id){
          this.$router.push({name: "request_book", params: { id: book_id}});
        },

        updateBook(bookId) {
          console.log("In books by sections view" )
          console.log(this.books.id)
          this.$router.push({ name: 'update_book', params: { id: bookId } });
        },
        deleteBook(bookId) {
          console.log("In Delete Book")
          console.log(bookId)
          const sectionId = this.$route.params.id;
          fetch(`http://127.0.0.1:5000/book/${bookId}`,{
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
                }
          })
          .then(response => {
            if (!response.ok){
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            console.log(`Book with ID ${bookId} deleted successfully`)
            this.getBooks(sectionId)
          });
        },
    }
  }
  </script>