<template>
  <NavBar />
  <div class="home">
    <td style="width:100%; height:100%;">
      <h1 style="position:absolute;top: 30%; left: 25%;"> Welcome to your Library </h1>
    </td>
  </div>
</template>

<script>
// @ is an alias to /src
import HomePage from '@/components/HomePage.vue';
import NavBar from "@/components/NavBar.vue";

export default {
  name: 'HomeView',
  components: {
    HomePage,
    NavBar,
  },
};


</script>
