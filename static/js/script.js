let video;
let canvas;
let nameInput;
let formLogin;
let formRegister;
let toast1;

function init(){
    // tự động mở webcam khi chạy web lần đầu tiên
    video = document.getElementById("video")
    canvas = document.getElementById("canvas")
    nameInput = document.getElementById("name")
    formLogin = document.getElementById("login-controls")
    formRegister = document.getElementById("register-controls")
    toast1 = document.getElementById("toast1")

    navigator.mediaDevices.getUserMedia({video:true})
        .then(stream => {
            video.srcObject = stream
            video1.srcObject = stream
        })
        .catch(error => {
            console.log("Errer access webcam", error);
            alert("cannot access webcam")
        })
}

// hàm capture
function capture(){
    const context = canvas.getContext("2d")
    context.drawImage(video,0,0,canvas.width,canvas.height)
    canvas.style.display = "block"
    video.style.display = "none"
}

// hàm đăng ký
function register(){
    const name = nameInput.value
    const photo =  dataURItoBlob(canvas.toDataURL())

    if(!name || !photo){
        alert("Name nad photo required")
        return
    }

    const formData = new FormData()
    formData.append("name", name)
    formData.append("photo", photo, `${name}.jpg`)

    fetch("/register",{
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.success){
            formRegister.style.display = "none"
            formLogin.style.display = "flex"
        }else{
            alert("Failed Register")
        }
    })
    .catch(error => {
        console.log("error", error);
    })
}

// hàm đăng nhập
function login(){
    const context = canvas.getContext("2d")
    context.drawImage(video,0,0, canvas.width, canvas.height)
    const photo =  dataURItoBlob(canvas.toDataURL())

    if(!photo){
        alert("photo required")
        return
    }

    const formData = new FormData()
    formData.append("photo", photo, "login.jpg")

    fetch("/login",{
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if(data.success){
            alert("login success !!!")
            window.location.href = "/success?user_name=" + data.name
        }else{
            alert("login failed")

        }
    }).catch(error => {
        console.log("error ", error);
    })
}

function dataURItoBlob(dataURI){
    const byteString = atob(dataURI.split(",")[1])
    const mimeString = dataURI.split(",")[0].split(":")[1].split(";")[0]

    const ab = new ArrayBuffer(byteString.length)
    const ia = new Uint8Array(ab)
    
    for (let i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i)
    }
    return new Blob([ab], {type: mimeString})
}

function openLogin(){
    formRegister.style.display = "none"
    formLogin.style.display = "flex"
}

init()