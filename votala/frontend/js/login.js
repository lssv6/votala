
function handleLogin() {
  let email = document.getElementById('user_email').value;
  let password = document.getElementById('user_password').value;

  // URLSearchParams is a object that holds key-value data which
  // we are going to pass in the body of the request.
  let sp = new URLSearchParams();
  sp.append("username", email);
  sp.append("password", password);



  var req = new XMLHttpRequest();// Request handler
  req.open("POST", "/api/token");
  req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  req.send(sp.toString());

  req.onload = () => {
    if(req.status != 200){
      let data = JSON.parse(req.responseText)
      alert(data["message"]);
      return;
    }
    sessionStorage.setItem("token", req.responseText);
    window.location = "/user-profile.html";
  };
  return false;
}
