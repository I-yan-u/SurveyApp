import axios from 'https://cdn.skypack.dev/axios';

document.addEventListener('DOMContentLoaded', function() {

const url = 'http://0.0.0.0:5001/api/v1/login';
const url2 = 'http://0.0.0.0:5001/api/v1/user/';
const url3 = 'http://0.0.0.0:5000/login';

  document.getElementById('login_submit').addEventListener("click", (event) => {
    // event.preventDefault();
    
    const email = document.getElementById('login_email').value;
    const password = document.getElementById('inPass').value;

    const pass_en = btoa(password);

    const data1 = {
      email,
      password,
    }

    // Send user cred to server to get session_id
    const fetchId = async (url, data1) => {
      try {
        const response = await axios.post(url, data1);
        let status = response.status;
        console.log(status);
        return status;
      } catch (error) {
        console.error('Get Id error:', error.message);
        alert(error.message);
      }
    }

    fetchId(url, data1).then(status => {
      // console.log( status);
      if (status === 201) {
        alert('Login successful!');
      } else {
        alert('Invalid email or Password!');
      }
    }).catch(error => {
      alert(`Error: ${error.message}`);
    })

  });
})




