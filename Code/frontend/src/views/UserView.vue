<template>
    <NavBar />
    <h2> User Dashboard   </h2>
    <div class="Books mt-5">
    
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Book ID</th>
            <th>Status</th>
            <th>Request Date</th>
            <th>Issue Date </th>
            <th> Actions </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="bookreq in bookrequest" :key="bookreq.status">
            <td>{{ bookreq.book_id }}</td>
            <td>{{ bookreq.status }}</td>
            <td>{{ bookreq.request_date}}</td>
            <td>{{ bookreq.issue_date}}</td>
            <td>
              <div class="btn-group" role="group">
                <button v-if="this.isuser && bookreq.status != 'request'" class="btn btn-outline-primary" @click="returnBook(bookreq.id)">Return </button>
                <button v-if="this.isuser  && bookreq.status != 'request'" class="btn btn-outline-primary" @click="renewBook(bookreq.id)">Renew </button>
                <button v-if="this.isuser  && bookreq.status != 'request'" class="btn btn-outline-primary" @click="">Review</button>
              

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
            bookrequest: [],
        };
    },
    mounted() {
        this.getBookByUser();
    },
    methods: {
        getBookByUser() {
            console.log("GETBookByuser")
          
            fetch(`http://127.0.0.1:5000/bookrequest/user`, {
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
                this.bookrequest = data.bookrequest;
            })
            .catch(error => {
                console.error('Error:', error);
            })
        },
        returnBook(req_id) {
          fetch(`http://127.0.0.1:5000/bookrequest/status/${req_id}`, {
            method : "PUT",
            headers : {
              'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
            status: "return",
          }),
          })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            console.log("Book returned");
            this.$router.push('/book_request_user');
          })
          .catch(error => {
            console.log("Book  could not be returned")
          });
    },
    renewBook(req_id) {
          fetch(`http://127.0.0.1:5000/bookrequest/status/${req_id}`, {
            method : "PUT",
            headers : {
              'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
            status: "return",
          }),
          })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            console.log("Book returned");
            this.$router.push('/book_request_user');
          })
          .catch(error => {
            console.log("Book  could not be returned")
          });
    }
    }
  }
</script>