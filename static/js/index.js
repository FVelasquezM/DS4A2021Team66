const urlVerifyImage = "http://127.0.0.1:5000/verify-image";

const $btnImage = document.getElementById('loadImage')

$btnImage.onclick = (e) => {
  e.preventDefault();
  verifyImage();
};

const verifyImage = async () => {
    const settings = {
      method: "POST",
      headers: new Headers({
        "content-type": "application/json",
      }),
      mode: "no-cors",
    };
    response = await fetch(`${urlVerifyImage}`, settings);
    console.log(response);
  };