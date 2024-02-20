import axios from 'https://cdn.skypack.dev/axios';

const loginData = async () => {
  const email = document.getElementById('login_email').value;
  const password = document.getElementById('inPass').value;
  const en_data = btoa(`${email}:${password}`);

  try {
    const response = await axios({
      url: '/login',
      baseURL: 'http://0.0.0.0:5001/api/v1',
      method: 'get',
      headers: {
        'Authorization': `Basic ${en_data}`,
      }
    });

    const status = response.status;
    const data  = response.data;

    localStorage.setItem('token', JSON.stringify(data));

    return { status };
  } catch (error) {
    console.error('Get Id error:', error.message);
    throw new Error('Login failed');
  }
}

const fetchUser = async () => {
  let token = localStorage.getItem('token');
  token = JSON.parse(token);

  try {
    const response = await axios({
      url: `/user/${token.id}`,
      baseURL: 'http://0.0.0.0:5001/api/v1',
      method: 'get',
      headers: {
        'Authorization': `Bearer ${token.token}`,
      }
    });
    localStorage.setItem('userData', JSON.stringify(response.data));
    return { stat: response.status, user: response.data };
  } catch (error) {
    console.error('Get User error:', error.message);
    return null;
  }
}

document.getElementById('login_submit').addEventListener("click", async (event) => {
  event.preventDefault();
  $('.lds-ellipsis').css('display', 'inline-block');

  try {
    // Fetch data
    const success = await loginData();
    const newUrl = 'http://0.0.0.0:5000/';
    const data = await fetchUser();

    if (success.status === 200) {
      $('.lds-ellipsis').css('display', 'none');
      alert('Login successful!');
      if (data.stat === 200) {
        let userData = localStorage.getItem('userData');
        userData = JSON.parse(userData);
        console.log(`user = ${userData}`);
      }
      window.location.href = newUrl;
    } else {
      $('.lds-ellipsis').css('display', 'none');
      console.log('Invalid email or password!');
    }
  } catch (error) {
    $('.lds-ellipsis').css('display', 'none');
    console.error('Error:', error.message);
    alert('Error: Invalid Login');
  }
});

export { fetchUser };