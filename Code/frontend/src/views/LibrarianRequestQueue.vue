<template>
    <NavBar />
    <h2> User Request Queue   </h2>
    <div class="Books mt-5">
    
      <table class="table table-bordered table-hover">
        <thead class="table-dark">
          <tr>
            <th>Book ID</th>
            <th>User ID</th>
            <th>Status</th>
            <th>Issue Date</th>
            <th>Due Date </th>
            <th> Actions </th>
        </tr>
        </thead>
        <tbody>
          <tr v-for="bookreq in bookrequest" :key="bookreq.status">
            <td>{{ bookreq.book_id }}</td>
            <td>{{ bookreq.user_id }}</td>
            <td>{{ bookreq.status }}</td>
            <td>{{ bookreq.issue_date}}</td>
            <td>{{ bookreq.due_date}}</td>

            <td>
              <div class="btn-group" role="group">
                <button v-if="this.islibrarian && (bookreq.status==='renew' || bookreq.status==='request') " class="btn btn-outline-primary" @click="approveBook(bookreq.id)">Issue</button>
                <button v-if="this.islibrarian  && (bookreq.status==='request' ||bookreq.status==='renew') " class="btn btn-outline-primary" @click="rejectBook(bookreq.id)">Reject</button>
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
        this.getBookByStatus();
    },
    methods: {
        getBookByStatus() {
            console.log("GETBookByStatus")
          
            fetch(`http://127.0.0.1:5000/bookrequest/status`, {
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
        
        approveBook(req_id) {
          fetch(`http://127.0.0.1:5000/bookrequest/status/${req_id}`, {
            method : "PUT",
            headers : {
              'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
            status: "approve",
          }),
          })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            console.log("Book request approved");
            this.$router.push('/book_request_status');
          })
          .catch(error => {
            console.log("Book request could not be approved")
          })
        },
          rejectBook(req_id) {
          fetch(`http://127.0.0.1:5000/bookrequest/status/${req_id}`, {
            method : "PUT",
            headers : {
              'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
            status: "reject",
          }),
          })
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }
            console.log("Book request rejected");
            this.$router.push('/book_request_status');
          })
          .catch(error => {
            console.log("Book request could not be rejected")
          });
          
          
      },
    }
  }
        
    
  
</script>