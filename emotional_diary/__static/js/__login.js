
function error_vib(msg_string){
  let element = $('.vib')
  element.addClass('error_login');
  setTimeout(() => {
      element.removeClass('error_login');
  }, 300) 
  $('#error_msg').text(msg_string)
  document.getElementById('error_msg').style.display = "block";
}

function request_ajax(url, method, data_dic) {
  $.ajax({
      url:url,
      type:method,
      async:false,
      data:data_dic,
      success: function (response) {
              result = response
                  let msg = "임시"
                  if (msg == "error") {
                      error_vib("에러메시지 추가")
                  } else {
                      let val = 1 
                      
                  }
              },
  error: function (e) {
      result = "error"
      error_vib("서버와의 연결에 문제가 있습니다.")
      }
  });
  return result;
}

function handleLoginClick(){
          const email = $("#email").val();
          const password = $("#password").val();
          let ajax_url = "http://127.0.0.1:8000/accounts/token/"
          console.log(ajax_url)
          const data_dic = {"email":email,"password":password};

          result = request_ajax(ajax_url,"POST",data_dic);
          if (result.response=="complete"){
              localStorage.setItem("access",result.access);
              localStorage.setItem("refresh",result.refresh);
              localStorage.setItem("email",result.email);
              console.log("storage complete")
              let intro_url = "http://127.0.0.1:8000/layout_test/"
              location.href = intro_url
              }
          else{
              console.log("email activate");
          }
      }
$(document).on("click","#submit_join", function(){
  email = $("#join_email").val();
  nickname = $("#join_username").val();
  password = $("#join_password").val();
  let ajax_url = "http://127.0.0.1:8000/accounts/signup/validate/"
  data_dic = {"email":email, "nickname":nickname, "password":password}
  console.log(data_dic)
  result = request_ajax(ajax_url,"GET",data_dic);
  console.log(result)
  if (result.validation=="True"){
      let ajax_url = "http://127.0.0.1:8000/accounts/signup/";
      data_dic = {"email":email,"password":password,"username":nickname};
      result = request_ajax(ajax_url,"POST",data_dic);

  }
  else {
      const element = document.getElementById('error');
      element.innerHTML = '<div id="error">' + result.message + '</div>';
  }

})
$(document).on("click","#to_signup", function(){
  const modals = document.querySelector('#modal_signup');
  let modal = bootstrap.Modal.getOrCreateInstance(modals)  
  modal.show()
})

$(document).on("click","#to_findpw", function(){
    const modals = document.querySelector('#modal_findpw');
    let modal = bootstrap.Modal.getOrCreateInstance(modals)  
    modal.show()
  })