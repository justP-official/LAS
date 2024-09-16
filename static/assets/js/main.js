let current_page = window.location.pathname;

let active_link = document.querySelector(`.nav-link[href='${current_page}']`);

active_link.classList.add('active');