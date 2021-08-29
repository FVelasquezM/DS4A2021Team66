const urlVerifyImage = "http://127.0.0.1:5000/app";

/* Inicio */
const $btnImage = document.getElementById('loadImage')
const $photoLoader = document.getElementById('photo')
const $effectLoader = document.getElementById('loader')
const $labelPhoto = document.getElementById('label-photo')
/* App */ 
const $visualMap = document.getElementById('visual-map2')
const $imagePreview = document.querySelector('.image_preview')
$photoLoader.onchange = (e) => {
    verifyImage()
}

const verifyImage = () => {
    
    let archivoRuta = $photoLoader.value;
    const allowExtensions = /(.tif|.tiff)$/i;

    if(!allowExtensions.exec(archivoRuta)){
        alert('Incorrect file!')
        $photoLoader = 0;
        return false;
    }else{
        if($photoLoader.files && $photoLoader.files[0]){
            let visor = new FileReader();

            var data = new FormData()
            data.append('file', $photoLoader.files[0])

            const settings = {
                method: "POST",
                body: data
            };

            visor.onload = async (e) => {
                $labelPhoto.style.display = "none";
                $effectLoader.style.opacity = "1";
                $effectLoader.style.transform = "translateY(0)";
                alert('ok')
                const res = await fetch(`${urlVerifyImage}`, settings);
            }
            visor.readAsDataURL($photoLoader.files[0]);
        }else{
            alert("some fails")
        }
    }
};
