import axios from 'https://cdn.skypack.dev/axios';

$(document).ready(() => {

  const confirmPword = (p1, p2) => {
    if (p1 === p2) {
      return true;
    }
    return false;
  }

const createUser = async () => {
  const creator = $('#creator-true').is(':checked') ? 'True' : 'False';

  const signUpData = {
    first_name: $('#first_name').val(),
    last_name: $('#last_name').val(),
    email: $('#email').val(),
    password: $('.confirmPass').val(),
    creator: creator,
  };

  try {
      const response = await axios({
      url: `/create_user`,
      baseURL: 'http://0.0.0.0:5001/api/v1',
      method: 'post',
      data: signUpData,
      headers: {
        'Content-Type': 'application/json'
      }
    });
    return { stat: response.status, user: response.data };
  } catch (error) {
    console.error('Get User error:', error.message);
  }
}

  $('#signup_submit').on("click", async (event) => {
    event.preventDefault();
    $('.signup_lds-ellipsis').css('display', 'inline-block');
    const newUrl = 'http://0.0.0.0:5000/login';

    const actual = $('.acPass').val();
    const confim = $('.confirmPass').val();
    if (confirmPword(actual, confim) === true){
      const newUser = await createUser();
      try {
        if (newUser.stat === 201){
          $('.signup_lds-ellipsis').css('display', 'none');
          alert('User created successfully');
          console.log(`Created user: ${newUser.user}`);
          window.location.href = newUrl;
        } else {
          $('.signup_lds-ellipsis').css('display', 'none');
          alert('Error in user creation');
        }
      } catch (error) {
        $('.signup_lds-ellipsis').css('display', 'none');
        console.error('Error:', error.message);
        alert('Error in user creation');
      }
    } else {
      $('.signup_lds-ellipsis').css('display', 'none');
      $('.confirmPass').focus();
      alert("Password doesn't match");
    }
  });
  
})