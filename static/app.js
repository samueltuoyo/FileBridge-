const mobNavLinks = document.querySelector('#footer div');
mobNavLinks.forEach((link) => {
   link.addEventListener('click', () => {
   mobNavLinks.forEach((others) => {
       others.classList.remove('active');
   })
       link.classList.toggle('active');
   })
});