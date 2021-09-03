if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}

// Chnage the state of display while receiving response from backend
const LoadImage=(e)=>{

    document.getElementsByClassName('inicio')[0].style.display='none';
    document.getElementsByClassName('esperar')[0].style.display='flex';
    e.form.submit()

   
}

    
   