// validation.js

function showAlert(msg){
  alert(msg);
  return false;
}

function validateLogin(){
  var nameEl = document.getElementById('name');
  var pwEl = document.getElementById('password');
  if(!nameEl || !pwEl) return true; // if elements not present, allow
  var name = nameEl.value.trim();
  var password = pwEl.value;

  if(!name){
    return showAlert('Please enter email or mobile.');
  }

  if(!validatePasswordRules(password)){
    return false;
  }
  return true;
}

function validateRegister(){
  var nameEl = document.getElementById('reg_name');
  var pwEl = document.getElementById('reg_password');
  var mobileEl = document.getElementById('reg_mobile');
  var emailEl = document.getElementById('reg_email');

  if(!nameEl || !pwEl) return true;

  var name = nameEl.value.trim();
  var password = pwEl.value;
  var mobile = mobileEl ? mobileEl.value.trim() : '';
  var email = emailEl ? emailEl.value.trim() : '';

  var nameRegex = /^[A-Za-z\s]+$/;
  if(!nameRegex.test(name)){
    return showAlert('Name must contain only letters and spaces.');
  }

  if(mobile && !/^\d{10}$/.test(mobile)){
    return showAlert('Mobile must be exactly 10 digits.');
  }

  if(email && !validateEmail(email)){
    return showAlert('Enter a valid email.');
  }

  if(!validatePasswordRules(password)){
    return false;
  }

  return true;
}

function validateEmail(email){
  var re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function validatePasswordRules(pw){
  if(pw.length !== 10){
    return showAlert('Password must be exactly 10 characters.');
  }
  // At least one lowercase, one uppercase, one special char
  var lower = /[a-z]/;
  var upper = /[A-Z]/;
  var special = /[!@#\$%\^\&*\)\(+=._-]/;
  if(!lower.test(pw)){
    return showAlert('Password must include at least one lowercase letter.');
  }
  if(!upper.test(pw)){
    return showAlert('Password must include at least one uppercase letter.');
  }
  if(!special.test(pw)){
    return showAlert('Password must include at least one special character.');
  }
  return true;
}
