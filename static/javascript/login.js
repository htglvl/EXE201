// function signIn(){
//     let oauth2Endpoint = "https://accounts.google.com/o/oauth2/v2/auth"


//     let form = document.createElement('form')
//     form.setAttribute('method', 'GET')
//     form.setAttribute('action', oauth2Endpoint)
//     let params = {
//         "client_id":"442704096089-bernp6oal7mdtgdjo175spun3422s0ro.apps.googleusercontent.com",
//         "redirect_uri":"http://localhost:5000",
//         "response_type":"token",
//         "scope":"https://www.googleapis.com/auth/userinfo.profile ",
//         "include_granted_scopes":'true',
//         'state':'pass-through-value'
//     }

//     for (var p in params){
//         let input = document.createElement('input')
//         input.setAttribute('type', 'hidden')
//         input.setAttribute('name',p)
//         input.setAttribute('value', params[p])
//         form.appendChild(input)
//     }

//     document.body.appendChild(form)

//     form.submit()
// }