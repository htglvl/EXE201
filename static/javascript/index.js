// var logoImage1 = document.getElementsByClassName("logo-icon-footer");
// if (logoImage1) {
//     logoImage1.addEventListener("click", function () {
//         var anchor = document.querySelector("[data-scroll-to='navbar']");
//         if (anchor) {
//             anchor.scrollIntoView({ block: "start", behavior: "smooth" });
//         }
//     });
// }


// let params = {}
// let regex = /([^&=]+)=([^&]*)/g,m

// while (m=regex.exec(location.href)){
//     params[decodeURIComponent(m[1])] = decodeURIComponent(m[2])
// }

// if(Object.keys(params).length > 0){
//     localStorage.setItem('authInfo', JSON.stringify(params))
// }

// window.history.pushState({}, document.title,"/")

// let info = JSON.parse(localStorage.getItem('authInfo'))
// console.log(JSON.parse(localStorage.getItem('authInfo')))
// console.log(info['access_token'])
// console.log(info['express_in'])
// console.log(info)

// fetch("https://www.googleapis.com/oauth2/v3/userinfo", {
//     headers:{
//     "Authorization":`Bearer ${info['access_token']}`
//     }
// })
// .then((data) => data.json())
// .then((info) =>{
//     console.log(JSON.stringify(info))
//     // document.getElementById('name').innerHTML = info.name
//     document.getElementById('user-image').setAttribute('src', info.picture)
//     document.getElementById('user-image').setAttribute('alt', info.name)
//     document.getElementById('sign-in-button').setAttribute('onclick','logout()')
//     document.getElementById('sign-in-button').setAttribute('href','#')
//     document.getElementById('sign-in-button-text').textContent = 'Log out';
// })
// .then((info)=>{
// fetch('/', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(info)})
// })




// function logout(){
//     fetch("https://oauth2.googleapis.com/revoke?token=" + info['access_token'], {
//         method:'POST',
//         headers:{
//             'Content-type':'application/x-www-form-urlencoded'
//         }})
//     .then((info) =>{
//             // document.getElementById('name').innerHTML = info.name
//             document.getElementById('user-image').setAttribute('src', "../static/public/default.jpeg")
//             document.getElementById('user-image').setAttribute('alt', "Guess")
//             document.getElementById('sign-in-button').setAttribute('onclick','')
//             document.getElementById('sign-in-button').setAttribute('href','/login')
//             document.getElementById('sign-in-button-text').textContent = 'Signup/Login';
//     })
// }
    