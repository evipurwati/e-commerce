function checkValidation() {

    if (document.forms.username.value == "") {
        console.log(alert("Username harus diisi"));
        username.focus();
        return false;
    }

    if (document.forms.psw.value == "") {
        console.log(alert("Password harus diisi"));
        psw.focus();
        return false;
    }

    if (document.forms.pswRepeat.value == "") {
        console.log(alert("Konfirmasi passwordnya dulu yaaa"));
        pswRepeat.focus();
        return false;
    }

    if (document.forms.pswRepeat.value != document.forms.psw.value) {
        console.log(alert("Password yang anda masukkan tidak sama"));
    }

    if (document.forms.email.value == "") {
        console.log(alert("Email harus diisi"));
        email.focus();
        return false;
    }

    if (document.forms.email.value.indexOf("@", 0) < 0) {
        console.log(alert("Email yang anda masukkan tidak valid"));
        email.focus();
        return false;
    }

    if (document.forms.email.value.indexOf(".", 0) < 0) {
        console.log(alert("Email yang anda masukkan tidak valid"));
        email.focus();
        return false;
    }

    if (document.forms.emailRepeat.value == "") {
        console.log(alert("Konfirmasi email harus diisi"));
        emailRepeat.focus();
        return false;
    }

    if (document.forms.emailRepeat.value.indexOf("@", 0) < 0) {
        console.log(document.forms.emailRepeat.value.indexOf("@", 0))
        console.log(alert("Email yang anda masukkan tidak valid"));
        emailRepeat.focus();
        return false;
    }

    if (document.forms.emailRepeat.value.indexOf(".", 0) < 0) {
        console.log(alert("Email yang anda masukkan tidak valid"));
        emailRepeat.focus();
        return false;
    }

    if (document.forms.emailRepeat.value != document.forms.email.value) {
        console.log(alert("Email yang anda masukkan harus sama dengan sebelumnya"));
    }

    return true;

}

