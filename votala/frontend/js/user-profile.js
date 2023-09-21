function getToken(){
  let token = sessionStorage.getItem("token");
  // token is stored as string.
  // then parsing to a object.
  token = JSON.parse(token);
  return token["access_token"];
}

function drawUserData(user_data){
  var name_element = document.getElementById("name");
  name_element.textContent = user_data["nickname"];

  var id_element = document.getElementById("user-id");
  id_element.textContent = user_data["id"];

  var created_element = document.getElementById("created");
  created_element.textContent = user_data["created"];

  var title_element = document.getElementsByTagName("title")[0];
  title_element.textContent += " - " + user_data["nickname"];
}

function createGroupLink(group_name, group_id){
  let link = document.createElement("a");
  link.innerText = group_name;
  link.setAttribute("href", "/group_page.html?group_id="+ group_id);
  return link;
}

function drawGroupData(group_data){
  let listOfGroups = document.getElementById("group-list");
  group_data.forEach(element => {
    let listItem = document.createElement("li");
    let groupLink = createGroupLink(element["name"], element["id"])
    listItem.appendChild(groupLink);
    listOfGroups.appendChild(listItem);
  });
}

function getGroupData(user_id){
  let token = getToken();
  if(!token){
    return;
  }
  let xhr = new XMLHttpRequest();
  let url = "/api/users/" + user_id + "/groups";
  xhr.open("GET",url);
  xhr.setRequestHeader("Authorization", "bearer"+ " " + token);
  xhr.send();
  xhr.onload = () => {
    if(xhr.status != 200){
      alert("Error.");
    }
    let data = JSON.parse(xhr.responseText);
    drawGroupData(data);
  };
}

function getUserData(){
  let token = getToken();
  if(!token){
    return;
  }
  let xhr = new XMLHttpRequest();
  xhr.open("GET", "/api/users/me");
  xhr.setRequestHeader("Authorization", "bearer"+ " " + token);
  xhr.send();
  xhr.onload = () => {
    if(xhr.status != 200){
      alert("something went wrong!");
    }
    let data = JSON.parse(xhr.responseText);
    drawUserData(data);
    getGroupData(data["id"]);
  };
  
}
window.onload = getUserData;

