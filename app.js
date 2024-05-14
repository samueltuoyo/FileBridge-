const input = document.getElementById("input");
let text = document.getElementById("iptext");
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