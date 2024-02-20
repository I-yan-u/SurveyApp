import axios from 'https://cdn.skypack.dev/axios';

$(document).ready(() => {

  // token
  let token = localStorage.getItem('token');
  token = JSON.parse(token) ? JSON.parse(token) : '';

  // Banner slider
  $('.banner_left #survey_editor button').click(() => {
    $(".banner").animate({ height: '5vh' }, 1000);
    $(".banner_left").animate({ height: '0', opacity: 0 }, 1000);
    $(".banner_right").animate({ height: '0', opacity: 0 }, 1000);
    $('#show_how').animate({opacity: '1'}, 1000);
    $("#survey-title").trigger('focus');
  });

  $('#show_how').click(() => {
    $(".banner").animate({ height: '80vh' }, 1000);
    $(".banner_left").animate({height: '80vh', opacity: 1 }, 1000);
    $(".banner_right").animate({height: '80vh', opacity: 1 }, 1000);
    $('#show_how').animate({opacity: '0'}, 1000);
  });

  $('#editor_temp_button').on('click', () => {
    $('#editor_temp_button').css({
      color: '#fff',
      backgroundColor: '#05386b',
      border: '1px solid #05386b',
    });
    $('#json_temp_button').css({
      color: '#05386b',
      backgroundColor: '#fff',
      border: '1px solid #fff',
    });
    $('#json_format p').animate({opacity: '0'}, 500);
    $('#json_format').animate({width: '20%'}, 1000);
    $('#editor_temp').animate({width: '80%'}, 1000);
    $('#editor_temp p').animate({opacity: '1'}, 2000);
  })

  $('#json_temp_button').on('click', () => {
    $('#json_temp_button').css({
      color: '#fff',
      backgroundColor: '#05386b',
      border: '1px solid #05386b',
    });
    $('#editor_temp_button').css({
      color: '#05386b',
      backgroundColor: '#fff',
      border: '1px solid #fff',
    });
    $('#editor_temp p').animate({opacity: '0'}, 500);
    $('#editor_temp').animate({width: '20%'}, 1000);
    $('#json_format').animate({width: '80%'}, 1000);
    $('#json_format p').animate({opacity: '1'}, 2000);
  })

  let count = 1;


  // Add questions
  $('#add-questions').click(() => {
    let questionId = `Question-${count}`;
    let label = `Question ${count}`;
    const input = `${questionId}-input`;
    const placeholder = `question: What is the question?\nchoices: ['choice1', 'choice2', 'choice3', 'choice4']\nor\nchoices: None (for textbox).`;

    $('#add-questions').before(`
    <div class="questions" id=${questionId}>
      <label> ${label} </label>
      <textarea name=${questionId} cols="50" rows="5" placeholder="${placeholder}"></textarea>
    </div>
    `);
    count++;
    console.log(questionId);
  });


  // Remove the questions
  $('#remove-questions').click(() => {
    if (count >= 2) {
      count--;
    } else {
      count = 1;
    }
  
    let questionId = `#Question-${count}`;
    console.log(questionId);
    $(questionId).remove();
  });

  // upload json file
  const upload_json = async (file) => {
    const response = await axios({
      url: '/upload_json',
      baseURL: 'http://0.0.0.0:5001/api/v1',
      method: 'post',
      headers: {
        'Authorization': `Bearer ${token.token}`,
      },
      data: file,
    });
    if (response.status === 401) {
      return { stat: response.status, data: response.data };
    }
    return { stat: response.status, data: response.data };
  }

  // handle upload json event
  $('#upload_json_btn').on('click', async (event) => {
    event.preventDefault();
    const fileInput = document.getElementById('myfile');
    let file = fileInput.files[0];
    if (file && file.type === 'application/json') {
      try {
        const response = await upload_json(file);
        if (response.stat === 401) {
          console.log(response.data);
          alert('User not logged in or User not a creator');
        } else {
          localStorage.setItem('new_survey_link', response.data.survey_id);
          console.log(response.data);
        }
      } catch (error) {
        alert(error.message);
      }
    } else {
      alert('No file selected or Invalid File type');
    }
  });

  $('#myfile').on('change', () => {
    const fileInput = document.getElementById('myfile');
    $('#input-file-name').append(fileInput.files[0].name);
  })

});

