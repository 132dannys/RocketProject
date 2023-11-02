function copyEmail(email){
    console.log(email)
    navigator.clipboard.writeText(email).then(r => alert(email + " copied."));
}
