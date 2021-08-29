/* No dispo */
const $noDispo = document.getElementById('no-dispo')
const $main = document.getElementById('main')

window.onresize = () =>{
    if (window.innerWidth < 1200) {
        $noDispo.style.display = "inline";
        $main.style.display = "none";
    }
    if (window.innerWidth > 1200) {
        $noDispo.style.display = "none";
        $main.style.display = "grid";
    }
}