<template>
    <NavBar />
    <h2> All Books   </h2>
    <div class="Books mt-5">
    
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
                <button v-if="this.isuser" class="btn btn-outline-primary" @click="requestBook(book.id)">Request Book</button>
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
            books: [],
            user: {},
        };
    },
    mounted() {
        this.getAllBooks()
    },
    methods: {
        getAllBooks() {
            fetch("http://127.0.0.1:5000/book", {
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
            console.log("MIXIN USER")
            console.log(this.user)
          
        },
        requestBook(book_id){

        fetch(`http://127.0.0.1:5000/bookrequest/${this.userid}/${book_id}`, {
          method: 'POST',
          headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
          'Content-Type': 'application/json',
          },
        })
        .then(response => {
          if (!response.ok){
            throw new Error("Book request is not completed ");
          }
          
          return response.json();
        })
        .then(data => {
          console.log("RESPONSE")
          console.log(data);
          alert(data.message);
        })
        .catch(error => {
          console.error("Error:" , error)
          alert(error)
        })
      }, 
    },
  };
  </script>