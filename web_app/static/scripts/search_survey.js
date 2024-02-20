import axios from 'https://cdn.skypack.dev/axios';

$(document).ready(() => {
  let token = localStorage.getItem('token');
  token = JSON.parse(token) ? JSON.parse(token) : '';

  // Get survey api call
  const getSurveys = async () => {
    const survey_link = $('#survey-link').val();
    try {
      const response = await axios({
        url: '/survey',
        baseURL: 'http://0.0.0.0:5001/api/v1',
        method: 'get',
        params: { 
          'survey_link': survey_link
        },
        headers: {
          'Authorization': `Bearer ${token.token}`,
        }
      });
      return { stat: response.status, surveys: response.data };
    } catch (error) {
      console.error('Get Survey error:', error.message);
      return error;
    }
  }

  // Get survey
  $('.search_survey').on('click', async (event) => {
    event.preventDefault();
    $('.s-lds-ellipsis').css('display', 'inline-block');

    try {
      const surveys = await getSurveys();
      if (surveys.stat === 200) {
        $('.s-lds-ellipsis').css('display', 'none');
        window.location.href = '/survey';
        localStorage.setItem('survey', JSON.stringify(surveys.surveys));
      } else {
          $('.s-lds-ellipsis').css('display', 'none');
          alert('Error: \n\t- Survey not found.\n\tor\n\t- Invalid survey id.\n\tor\n\t- User not logged in');
        }
      } catch (error) {
        $('.s-lds-ellipsis').css('display', 'none');
        console.error('Error: ', error.message);
      }
  });

  // Load survey page
  const loadSurvey = () => {
    const survey = localStorage.getItem('survey');
    const surveyData = JSON.parse(survey);
    if (surveyData !== null) {
      // prep page
      let title = `<div class="title_desc">
      <h2 id="survey_title">${surveyData.survey.title}</h2>
      <p id="survey_desc">${surveyData.survey.description}</p>
      </div>`
      let form_div = `<form id="form_action" method="post" action="/survey/${surveyData.survey.id}">
      </form>`

      $('.sp-lds-ellipsis').css('display', 'none');
      $('.survey').append(title);
      $('.survey').append(form_div);

      // Load form
      const form = surveyData.form;
      for (let i = 0; i < form.length; i++) {
      let html_content = `<div class="survey_form"><h3>${form[i].question}</h3>`
        let type = form[i].type;
        switch (type) {
          // case of radio
          case 'radio':
            const options_radio = form[i].radio;
            options_radio.forEach(element => {
              html_content += `<label class="radio">
              <input type="radio" name="${form[i].question}" value="${element}">
              <span class="radio-dot"></span>
              ${element}
              </label><br>`
            });
            break;

          // case of checkbox
          case 'checkbox':
            const options_check = form[i].checkbox;
            options_check.forEach(element => {
              html_content += `<label class="checkbox">
              <input type="checkbox" name="${form[i].question}" value="${element}">
              <span class="radio-dot"></span>
              ${element}
              </label><br>`
            });
            break;

          // case of password
          case 'password':
            html_content += `<label class="text">
                <input type="password" name="${form[i].question}" placeholder="${form[i].password}">
            </label>`
            break;

          // case of date object
          case 'date':
            html_content += `<label class="date_option">
                    <p>${form[i].date}:</p>
                    <input type="date" name=' ${form[i].question}'>
                </label><br></br>`
            break;

          // case of range object
          case 'range':
            html_content += `<label class="range_option">
              <input type="range" id="range_input" name='${ form[i].question }' min="${ form[i].range[0] }" max="${ form[i].range[1] }">
              <span id="range_value">${form[i].range[0]}</span>
            </label><br>`
            break;

          // defaults to a text input.
          default:
            html_content += `<label class="text">
                <input type="text" name="${form[i].question}" placeholder="${form[i].text}">
            </label>`
        }
        $('#form_action').append(html_content);
      }
      $('#form_action').append('<button type="submit">Submit Survey</button>');
    }
    
  }

  loadSurvey();
});