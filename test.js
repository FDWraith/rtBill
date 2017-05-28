var loginF = function(){
    var email = document.getElementById("email-log").value;
    var pass = document.getElementById("password-log").value;
    $.post("/authen", { "email": email, "password": pass,"authen": "login"}, function(d){
        if( d != False ){
            window.location.href = d;
        }else{
            alert("Incorrect Email or Password");
        };
    };
          );
};

//var login_btn = document.getElementById("login");
//login_btn.addEventListener("click", loginF );

var registerF = function(){
    console.log("clicked");
    var email = document.getElementById("email-reg").value;
    var pass = document.getElementById("password-reg").value;
    var name = document.getElementById("name-reg").value;
    $.post("/authen", { "email": email, "password": pass, "name":name, "authen": "signup"}, function(v){
        if( v == True){
            alert("Login Successful. Please verify your email by using the link we sent you");
        }else{
            alert("Invalid Email: it already exists. Please try another email");
        }});
};

var register_btn = document.getElementById("register");
register-btn.addEventListener("click", registerF);
