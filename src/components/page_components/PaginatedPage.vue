
<template>
    <div class='d-flex flex-row mx-md-4' >
            <ul class='pagination my-3 '>
                <li class="page-item pe-auto"  @click="prevPage" :class="[(currentPage === 1)? 'disabled' : '']"><span class='page-link'>{{'<<'}}</span></li>
                    <li class="page-item pointer-cursor" v-for="i in Number(endPagination - startPagination + 1)"
                @click="handlePageButtonClick(startPagination + i -1)" :class="[(currentPage == startPagination + i -1) ? 'active' : '']"  >
                        <span class='page-link'>{{startPagination + i - 1}}</span>
                    </li>
                <li class="page-item pe-auto"  @click="nextPage" :class="[(currentPage === maxPages)? 'disabled' : '']"><span class='page-link'>{{'>>'}}</span></li>
            </ul>
    </div>
    <div class="row mx-md-2 align-stretch">
        <div class="col-sm-12 col-md-6 col-lg-4 anime-card-container my-3 my-md-2" v-for="book, index in pageData" :key="index">
            <BookCard :authors="book.authors" :title="book.title" :avg_rating="book.avg_rating" :description="book.description"
            :bookId="book.id" :img_src="book.img_src" />
        </div> 
    </div>
</template>

<script>
    import BookCard from './BookCard.vue';

    export default {
        components: {
            BookCard,
        },
        data() {
            return {
                currentPage: 1,
                maxPerPage: 6,
                maxPagination: 5,
                pageData: [],
                books: [
                    {
                        authors: ["Marijn Haverbeke"],
                        isbn: "9781593279509",
                        title: "Eloquent JavaScript, Third Edition",
                        avg_rating: 4.6,
                        description: "JavaScript lies at the heart of almost every modern web application, from social apps like Twitter to browser-based game frameworks like Phaser and Babylon. Though simple for beginners to pick up and play with, JavaScript is a flexible, complex language that you can use to build full-scale applications.",
                        id: 2,
                        img_src: "https://m.media-amazon.com/images/I/41VvIauMuuL._SY445_SX342_.jpg",
                    },
                    {
                        authors: ["Scott Chacon", "Ben Straub"],
                        isbn: "9781484200766",
                        title: "Pro Git",
                        avg_rating: 4.5,
                        description: "Pro Git (Second Edition) is your fully-updated guide to Git and its usage in the modern world. Git has come a long way since it was first developed by Linus Torvalds for Linux kernel development. It has taken the open source world by storm since its inception in 2005, and this book teaches you how to use it like a pro.",
                        id: 3,
                        img_src: "https://m.media-amazon.com/images/I/51QQtVlsWsL._SX342_SY445_.jpg",
                    },
                    {
                        authors: ["Akira Toriyama", "Ben Straub"],
                        isbn: "1974743608",
                        title: "Dragon Ball Super, Vol. 20 (20)",
                        avg_rating: 4.7,
                        description: "Goku’s adventure from the best-selling classic manga Dragon Ball continues in this new series written by Akira Toriyama himself!",
                        id: 12,
                        img_src: "https://m.media-amazon.com/images/I/51ZVBjxRz-L._SY445_SX342_.jpg",
                    },
                    {
                        authors: ["Marijn Haverbeke"],
                        isbn: "9781593279509",
                        title: "Eloquent JavaScript, Third Edition",
                        avg_rating: 4.6,
                        description: "JavaScript lies at the heart of almost every modern web application, from social apps like Twitter to browser-based game frameworks like Phaser and Babylon. Though simple for beginners to pick up and play with, JavaScript is a flexible, complex language that you can use to build full-scale applications.",
                        id: 2,
                        img_src: "https://m.media-amazon.com/images/I/41VvIauMuuL._SY445_SX342_.jpg",
                    },
                    {
                        authors: ["Scott Chacon", "Ben Straub"],
                        isbn: "9781484200766",
                        title: "Pro Git",
                        avg_rating: 4.5,
                        description: "Pro Git (Second Edition) is your fully-updated guide to Git and its usage in the modern world. Git has come a long way since it was first developed by Linus Torvalds for Linux kernel development. It has taken the open source world by storm since its inception in 2005, and this book teaches you how to use it like a pro.",
                        id: 3,
                        img_src: "https://m.media-amazon.com/images/I/51QQtVlsWsL._SX342_SY445_.jpg",
                    },
                    {
                        authors: ["Akira Toriyama", "Ben Straub"],
                        isbn: "1974743608",
                        title: "Dragon Ball Super, Vol. 20 (20)",
                        avg_rating: 4.7,
                        description: "Goku’s adventure from the best-selling classic manga Dragon Ball continues in this new series written by Akira Toriyama himself!",
                        id: 12,
                        img_src: "https://m.media-amazon.com/images/I/51ZVBjxRz-L._SY445_SX342_.jpg",
                    },
                    {
                        authors: ["Marijn Haverbeke"],
                        isbn: "9781593279509",
                        title: "Eloquent JavaScript, Third Edition",
                        avg_rating: 4.6,
                        description: "JavaScript lies at the heart of almost every modern web application, from social apps like Twitter to browser-based game frameworks like Phaser and Babylon. Though simple for beginners to pick up and play with, JavaScript is a flexible, complex language that you can use to build full-scale applications.",
                        id: 2,
                        img_src: "https://m.media-amazon.com/images/I/41VvIauMuuL._SY445_SX342_.jpg",
                    },
                    {
                        authors: ["Scott Chacon", "Ben Straub"],
                        isbn: "9781484200766",
                        title: "Pro Git",
                        avg_rating: 4.5,
                        description: "Pro Git (Second Edition) is your fully-updated guide to Git and its usage in the modern world. Git has come a long way since it was first developed by Linus Torvalds for Linux kernel development. It has taken the open source world by storm since its inception in 2005, and this book teaches you how to use it like a pro.",
                        id: 3,
                        img_src: "https://m.media-amazon.com/images/I/51QQtVlsWsL._SX342_SY445_.jpg",
                    },
                    {
                        authors: ["Akira Toriyama", "Ben Straub"],
                        isbn: "1974743608",
                        title: "Dragon Ball Super, Vol. 20 (20)",
                        avg_rating: 4.7,
                        description: "Goku’s adventure from the best-selling classic manga Dragon Ball continues in this new series written by Akira Toriyama himself!",
                        id: 12,
                        img_src: "https://m.media-amazon.com/images/I/51ZVBjxRz-L._SY445_SX342_.jpg",
                    },
                    {
                        authors: ["Marijn Haverbeke"],
                        isbn: "9781593279509",
                        title: "Eloquent JavaScript, Third Edition",
                        avg_rating: 4.6,
                        description: "JavaScript lies at the heart of almost every modern web application, from social apps like Twitter to browser-based game frameworks like Phaser and Babylon. Though simple for beginners to pick up and play with, JavaScript is a flexible, complex language that you can use to build full-scale applications.",
                        id: 2,
                        img_src: "https://m.media-amazon.com/images/I/41VvIauMuuL._SY445_SX342_.jpg",
                    },
                    {
                        authors: ["Scott Chacon", "Ben Straub"],
                        isbn: "9781484200766",
                        title: "Pro Git",
                        avg_rating: 4.5,
                        description: "Pro Git (Second Edition) is your fully-updated guide to Git and its usage in the modern world. Git has come a long way since it was first developed by Linus Torvalds for Linux kernel development. It has taken the open source world by storm since its inception in 2005, and this book teaches you how to use it like a pro.",
                        id: 3,
                        img_src: "https://m.media-amazon.com/images/I/51QQtVlsWsL._SX342_SY445_.jpg",
                    },
                    {
                        authors: ["Akira Toriyama", "Ben Straub"],
                        isbn: "1974743608",
                        title: "Dragon Ball Super, Vol. 20 (20)",
                        avg_rating: 4.7,
                        description: "Goku’s adventure from the best-selling classic manga Dragon Ball continues in this new series written by Akira Toriyama himself!",
                        id: 12,
                        img_src: "https://m.media-amazon.com/images/I/51ZVBjxRz-L._SY445_SX342_.jpg",
                    },
                    {
                        authors: ["Marijn Haverbeke"],
                        isbn: "9781593279509",
                        title: "Eloquent JavaScript, Third Edition",
                        avg_rating: 4.6,
                        description: "JavaScript lies at the heart of almost every modern web application, from social apps like Twitter to browser-based game frameworks like Phaser and Babylon. Though simple for beginners to pick up and play with, JavaScript is a flexible, complex language that you can use to build full-scale applications.",
                        id: 2,
                        img_src: "https://m.media-amazon.com/images/I/41VvIauMuuL._SY445_SX342_.jpg",
                    },
                    {
                        authors: ["Scott Chacon", "Ben Straub"],
                        isbn: "9781484200766",
                        title: "Pro Git",
                        avg_rating: 4.5,
                        description: "Pro Git (Second Edition) is your fully-updated guide to Git and its usage in the modern world. Git has come a long way since it was first developed by Linus Torvalds for Linux kernel development. It has taken the open source world by storm since its inception in 2005, and this book teaches you how to use it like a pro.",
                        id: 3,
                        img_src: "https://m.media-amazon.com/images/I/51QQtVlsWsL._SX342_SY445_.jpg",
                    },
                    {
                        authors: ["Akira Toriyama", "Ben Straub"],
                        isbn: "1974743608",
                        title: "Dragon Ball Super, Vol. 20 (20)",
                        avg_rating: 4.7,
                        description: "Goku’s adventure from the best-selling classic manga Dragon Ball continues in this new series written by Akira Toriyama himself!",
                        id: 12,
                        img_src: "https://m.media-amazon.com/images/I/51ZVBjxRz-L._SY445_SX342_.jpg",
                    },
                    {
                        authors: ["Marijn Haverbeke"],
                        isbn: "9781593279509",
                        title: "Eloquent JavaScript, Third Edition",
                        avg_rating: 4.6,
                        description: "JavaScript lies at the heart of almost every modern web application, from social apps like Twitter to browser-based game frameworks like Phaser and Babylon. Though simple for beginners to pick up and play with, JavaScript is a flexible, complex language that you can use to build full-scale applications.",
                        id: 2,
                        img_src: "https://m.media-amazon.com/images/I/41VvIauMuuL._SY445_SX342_.jpg",
                    },
                    {
                        authors: ["Scott Chacon", "Ben Straub"],
                        isbn: "9781484200766",
                        title: "Pro Git",
                        avg_rating: 4.5,
                        description: "Pro Git (Second Edition) is your fully-updated guide to Git and its usage in the modern world. Git has come a long way since it was first developed by Linus Torvalds for Linux kernel development. It has taken the open source world by storm since its inception in 2005, and this book teaches you how to use it like a pro.",
                        id: 3,
                        img_src: "https://m.media-amazon.com/images/I/51QQtVlsWsL._SX342_SY445_.jpg",
                    },
                    {
                        authors: ["Akira Toriyama", "Ben Straub"],
                        isbn: "1974743608",
                        title: "Dragon Ball Super, Vol. 20 (20)",
                        avg_rating: 4.7,
                        description: "Goku’s adventure from the best-selling classic manga Dragon Ball continues in this new series written by Akira Toriyama himself!",
                        id: 12,
                        img_src: "https://m.media-amazon.com/images/I/51ZVBjxRz-L._SY445_SX342_.jpg",
                    },
                ]
            }
        },
        watch: {
            "books": function(newData, oldData){
                this.maxPages = Math.max(1, Math.ceil(newData.length/this.maxPerPage));
            },
            "currentPage": function(newPage, oldPage){
                console.log('Old page:', oldPage, ', new page: ', newPage);
                console.log(this.getDataForPage(newPage));
                this.pageData = this.getDataForPage(newPage);
            }
        },
        methods: {
            prevPage: function(){
                console.log(this.currentPage);
                if (this.currentPage > 1){
                    this.currentPage -= 1;
                }
            },
            nextPage: function(){
                console.log(this.currentPage);
                if (this.currentPage < this.maxPages){
                    this.currentPage += 1;
                }
            },
            getDataForPage: function(page){
                return this.books.slice((page-1)*this.maxPerPage
                    , Math.min(this.books.length + 1, page*this.maxPerPage));
            },
            handlePageButtonClick: function(page){
                this.currentPage = page;
            }
        },
        beforeMount() {
            this.maxPages = Math.max(1, Math.ceil(this.books.length/this.maxPerPage) );
            this.paginationBlock = Math.floor((this.currentPage-1) / this.maxPagination);
            this.startPagination = this.maxPagination * this.paginationBlock + 1;
            this.endPagination = Math.min((this.paginationBlock + 1) * this.maxPagination, this.maxPages);
            this.pageData = this.getDataForPage(this.currentPage);
        },
    }
</script>