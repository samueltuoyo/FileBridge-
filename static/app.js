const inputField1 = document.getElementById('username');
const inputField2 = document.getElementById('Room_Name')
const text = document.getElementById("iptext");
const contentElement = document.querySelector('.content');
const currentPage = window.location.pathname;
const links = document.querySelectorAll('#footer a');
function check(){
  if (inputField1.value === '' || inputField2.value === ''){
    text.innerHTML = 'Please Create a room or join || create a room number';
    text.style.color = 'red';
    text.style.fontSize = '20px';
    
  } else{
    text.textContent = '';
  }
  
  inputField1.addEventListener('input', check);
inputField2.addEventListener('input', check);
}
links.forEach(link => {
    if (link.href.includes(currentPage)) {
      link.classList.add('active');
    }
  });


