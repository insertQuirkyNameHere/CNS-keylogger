const btn = document.querySelector('#rec-btn');

btn.addEventListener('click', ()=>{
    document.querySelector('#before-click').style.display = 'none';
    document.querySelector('#after-click').style.display = 'block';
});