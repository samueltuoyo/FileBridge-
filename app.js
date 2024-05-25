const input = document.getElementById("input");
const text = document.getElementById("iptext");
const entrance= document.getElementById('main-app');
function check(){
if (input.value === ''){
   text.innerHTML = 'Enter an ip address';
   text.style.color = 'red';
   text.style.fontSize = '20px';
}

else{
    text.textContent = '';
}
}

entrance.addEventListener('animationend', () => {
    entrance.style.display = 'none';
});