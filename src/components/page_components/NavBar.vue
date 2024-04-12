<template>
<div class="offcanvas offcanvas-start w-50 w-md-25" tabindex="-1" id="offcanvas" data-bs-keyboard="false" data-bs-backdrop="false">
    <div class="offcanvas-header">
        <h6 class="offcanvas-title d-block" id="offcanvas">My Library</h6>
        <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>
    <div class="offcanvas-body px-0">
        <ul class="nav nav-pills flex-column mb-sm-auto mb-0 align-items-start" id="menu">
            <li class="nav-item">
                <form class="form-inline" onsubmit="searchLibrary">
                    <div class="input-group">
                        <div class="dropdown input-group-prepend">
                            <a href="#" class="nav-link dropdown-toggle btn btn-outline-secondary" data-bs-toggle="dropdown" ><span>All</span></a>
                            <ul class="dropdown-menu shadow-small">
                                <li class="dropdown-item" ><span>All</span></li>
                                <li class="dropdown-item" ><span>Bookname</span></li>
                                <li class="dropdown-item" ><span>Author</span></li>
                                <li class="dropdown-item" ><span>ISBN</span></li>
                                <li class="dropdown-item" ><a href="/advanced-search">Advanced</a></li>
                            </ul>
                        </div>
                        <input type="text" class="form-control" placeholder="Search" name="query" aria-label="Search query"/>
                        <button type="submit" class="input-group-append btn btn-primary"><span>Search</span></button>
                    </div>
                </form>
                
            </li>
            <hr class="hr nav-item"/>
            <li class="nav-item my-2">
                <div class="d-flex flex-row justify-content-between w-100">
                    <a href="/login" class="btn btn-outline-primary mx-1" type="button">
                            <span class=""><i class="bi bi-person"></i>Login</span>
                    </a>
                    <a href="/register" class="btn btn-primary mx-1" type="button">
                            <span class=""><i class="bi bi-person-plus"></i>Sign up</span>
                    </a>
                </div>
            </li>
            <li class="nav-item">
                <a href="#" class="nav-link text-truncate">
                    <i class="fs-5 bi-type"></i><span class="ms-1  d-sm-inline">Genre/Subject</span>
                </a>
            </li>
            <li>
                <a href="#submenu1" data-bs-toggle="collapse" class="nav-link text-truncate">
                    <i class="fs-5 bi-fire"></i><span class="ms-1 d-sm-inline">Trending</span> </a>
            </li>
            <li>
                <a href="#" class="nav-link text-truncate">
                    <i class="fs-5 bi-table"></i><span class="ms-1 d-none d-sm-inline">Advanced Search</span></a>
            </li>
            <li class="dropdown">
                <a href="#" class="nav-link dropdown-toggle  text-truncate" id="dropdown" data-bs-toggle="dropdown" aria-expanded="false">
                    <i class="fs-5 bi-bootstrap"></i><span class="ms-1 d-none d-sm-inline">User</span>
                </a>
                <ul class="dropdown-menu text-small shadow" aria-labelledby="dropdown">
                    <li><a class="dropdown-item" href="#">Borrow book...</a></li>
                    <li><a class="dropdown-item" href="#">Favorite</a></li>
                    <li><a class="dropdown-item" href="#">Profile</a></li>
                    <li>
                        <hr class="dropdown-divider">
                    </li>
                    <li><a class="dropdown-item" href="#"><i clss="fs-5 bi-book-arrow-out"></i>Sign out</a></li>
                </ul>
            </li>
            <li>
                <a href="#" class="nav-link text-truncate">
                    <i class="fs-5 bi-speedometer2"></i><span class="ms-1 d-sm-inline">Admin</span></a>
            </li>
            <li>
                <a href="#" class="nav-link text-truncate">
                    <i class="fs-5 bi-info-circle"></i><span class="ms-1 d-sm-inline">About</span> </a>
            </li>
        </ul>
    </div>
</div>
<button class="btn float-end" data-bs-toggle="offcanvas" data-bs-target="#offcanvas" role="button" aria-label="More">
    <i class="bi bi-arrow-right-square-fill fs-3" data-bs-toggle="offcanvas" data-bs-target="#offcanvas"></i>
</button>
</template>