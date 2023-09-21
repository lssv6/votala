/*
 * This is a function that returns
 * a list of users sorted by nickname.
 * */
function queryUserByNickname(nickname,callback){
  var req = new XMLHttpRequest();
  req.open("GET", "/api/users?query=" + nickname);
  req.send();
  req.onload = () => {
    if(req.status == 200){
      var data = JSON.parse(req.responseText);
      callback(data);
    }else{
    }

  };
}

function manipulateUserList(data){
  let usersList = document.getElementById("users-list");
  usersList.innerHTML = "";
  data.forEach(item => {
    let listItem = document.createElement("li");
    let p = document.createElement("p");
    p.innerText = item["nickname"];
    listItem.appendChild(p);
    usersList.appendChild(listItem);
  });
}

function updateUserList(){ 
  let searchBarElem = document.getElementById("user-search-bar");
  var nickname = searchBarElem.value;
  if(nickname.length < 3){
    manipulateUserList([]);
    return;
  }
  console.log(nickname);
  queryUserByNickname(nickname, (data) => {
    manipulateUserList(data);
  });
}
