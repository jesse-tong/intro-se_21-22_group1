<template>
<nav class="navbar bg-body-tertiary">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="#">Simple Library</RouterLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavigation" aria-controls="offcanvasNavigation" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="offcanvas offcanvas-start" tabindex="-1" id="offcanvasNavigation" aria-labelledby="offcanvasNavbarLabel">
        <div class="offcanvas-header">
          <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Sidebar</h5>
          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body">
          <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">      
            <form class="d-flex mt-3" role="search">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
              <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
            <li class="nav-item">
              <RouterLink class="nav-link active" aria-current="page" to="#">Home</RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/books/category">Categories</RouterLink>
            </li>
            <li class="nav-item dropdown">
              <button class="nav-link dropdown-toggle" to="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Admin
              </button>
              <ul class="dropdown-menu">
                <li><RouterLink class="dropdown-item" to="/admin/manage-books">Manage books</RouterLink></li>
                <li><RouterLink class="dropdown-item" to="/admin/manage-borrow">Manage borrow</RouterLink></li>
                <li>
                  <hr class="dropdown-divider">
                </li>
                <li><RouterLink class="dropdown-item" to="/admin/reports">Reports</RouterLink></li>
              </ul>
            </li>
            <li class="nav-item dropdown">
              <button class="nav-link dropdown-toggle" to="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                Books
              </button>
              <ul class="dropdown-menu">
                <li><RouterLink class="dropdown-item" to="/books/advanced-search">Advanced search</RouterLink></li>
                <li><RouterLink class="dropdown-item" to="/admin/manage-borrow">Authors</RouterLink></li>
                <li>
                  <hr class="dropdown-divider">
                </li>
                <li><RouterLink class="dropdown-item" to="/books/by-genre">Genres/categories</RouterLink></li>
                <li><RouterLink class="dropdown-item" to="/books/by-author">Authors</RouterLink></li>
                <li>
                  <hr class="dropdown-divider">
                </li>
                <li><RouterLink class="dropdown-item" to="/borrow">Manage borrow/return book</RouterLink></li>
              </ul>
            </li>
            <li class="nav-item dropdown">
              <button class="nav-link dropdown-toggle" to="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                User
              </button>
              <ul class="dropdown-menu">
                <li><RouterLink class="dropdown-item" to="/user/profile">User profile</RouterLink></li>
                <li><RouterLink class="dropdown-item" to="/user/settings">User settings</RouterLink></li>
                <li>
                  <hr class="dropdown-divider">
                </li>
                <li><RouterLink class="dropdown-item" to="/login">Log in</RouterLink></li>
                <li><RouterLink class="dropdown-item" to="/register">Register</RouterLink></li>
                <li><RouterLink class="dropdown-item" to="/logout">Log out</RouterLink></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
      
    </div>
  </nav>
</template>

<script setup>
    
</script>