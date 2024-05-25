 // JavaScript code
 function validateForm() {
    var password1 = document.getElementById("pass1").value;
    var password2 = document.getElementById("pass2").value;

    if (password1 !== password2) {
      document.getElementById("error-message").style.display = "block";
      return false;
    } else {
      document.getElementById("error-message").style.display = "none";
      return true;
    }
  }
