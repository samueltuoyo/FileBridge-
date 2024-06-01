const input = document.getElementById("input");
const text = document.getElementById("iptext");
const entrance= document.getElementById('main-app');
const contentElement = document.querySelector('.content');
function check(){
if (input.value === ''){
   text.innerHTML = 'Enter an ip address';
   text.style.color = 'red';
   text.style.fontSize = '20px';
}
}
// else{
//     text.textContent = '';
// }

entrance.addEventListener('animationend', () => {
    window.location.href = '/main';
});
