function copyEmail(id){
    console.log(id)
    let uuid = id.slice(0, -3)
    let email = document.getElementById(uuid);
    navigator.clipboard.writeText(email.innerText).then(r => alert(email.innerText + " copied."));
}
