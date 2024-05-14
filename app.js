const input = document.getElementById("input");
const click = document.getElementById("click");
let text = document.getElementById("iptext");

click.addEventListener('click', function check(){
if(input.value === '') {
   text.innerHTML = 'Enter an ip address';
   text.style.color = 'red';
   text.style.fontSize = '20px';
}

else{
    text.textContent = '';
}
});