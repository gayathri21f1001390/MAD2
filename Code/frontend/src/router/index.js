import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import RegisterPage from "../views/RegisterPage.vue";
import LoginPage from "../views/LoginPage.vue";
import SectionsView from "../views/SectionsView.vue";
import SectionCreate from "../views/SectionCreate.vue"
import SectionUpdate from "../views/SectionUpdate.vue";
import BookCreate from "../views/BookCreate.vue";
import BookUpdate from "../views/BookUpdate.vue";
import SectionBooksView from "../views/BookBySectionView.vue";
import AllBooksView from "../views/AllBooksView.vue";
import UserView from "../views/UserView.vue";
import LibrarianView from "../views/LibrarianRequestQueue.vue"

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterPage,
  },
  {
    path: "/login",
    name: "login",
    component: LoginPage,
  },
  {
    path: "/create_section",
    name: "create_section",
    component: SectionCreate,
  },
  {
    path: "/view_sections",
    name: "view_sections",
    component: SectionsView,
  },
  {
    path: "/update_section/:id",
    name: "update_section",
    component: SectionUpdate,
  },
  {
    path: "/create_book/:id",
    name: "create_book",
    component: BookCreate,
  },
  {
    path: "/view_section_books/:id",
    name: "view_section_books",
    component: SectionBooksView,
  },
  {
    path: "/update_book/:id",
    name: "update_book",
    component: BookUpdate,
  },
  {
    path: "/view_books",
    name: "view_books",
    component: AllBooksView,
  },

  {
    path: "/book_request_user",
    name: "book_request_user",
    component: UserView,
  },
  {
    path: "/book_request_status",
    name: "book_request_status",
    component: LibrarianView,
  },
 
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },


]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router;
