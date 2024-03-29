import axios from 'https://cdn.skypack.dev/axios';

const fetchResponse = async (index) => {

  const surveyId = $('#search_survey').val();
  const url = `http://127.0.0.1:5001/api/v1/response/`;
  let cookie = document.cookie;
  cookie = cookie.split('=')[1]

  await $.ajax({
  type: 'GET',
  url: `${url}${surveyId}`,
  xhrFields: {
      withCredentials: true,
  },
  headers: {
      "Content-Type": "application/json",
      'custom-header': cookie
  },
  data: {
      index,
  },
  contentType: "application/json",
  success: data => {
      const len = data.data_length;
      if (len > 10) {
          let noOfPages = Math.floor(len / 10);
          const prev_sId = $('td#table_survey_id').first().text();
              if (prev_sId === undefined || prev_sId !== data.data[0].survey_id) {
                  $('.pager').children().remove();
                  for (let i = 1; i <= noOfPages + 1; i++) {
                      $('.pager').append(`<a href=# id=${i} value=${i} onClick=fetchResponse(${(i - 1) * 10})>${i}</a>`);
              }
          }
      }

      $('th#survey_title').empty();
      $('th#survey_title').append(data.data[0].title);

      $('tr').children('td').remove();
      data.data.forEach(response => {
          let resString = '';
          let res = response.response;
          if (res.length > 120) {
              resString += res.slice(0, 120);
              resString += '...';
              $('table').append(
              `<tr onClick=getSpecificResponse("${response.id}")>
                  <td id="table_response_id">${response.id}</td>
                  <td id="table_survey_id">${response.survey_id}</td>
                  <td id="table_response">${resString}</td>
                  <td id="table_created_at">${response.created_at}</td>
              </tr>
              `)
          } else {
              $('table').append(
              `<tr onClick=getSpecificResponse("${response.id}")>
                  <td id="table_response_id">${response.id}</td>
                  <td id="table_survey_id">${response.survey_id}</td>
                  <td id="table_response">${res}</td>
                  <td id="table_created_at">${response.created_at}</td>
              </tr>
              `)
          }
      });
      placeActive($('.pager').children());
      console.log($('.pager').children());
  },
  error: (xhr, status, error) => {
      $('tr').children('td').remove();
      alert(`Error code: ${status}, Massage: ${error}`);
  },
  dataType: "json",
  })
}

const placeActive = (children) => {
  children.each(function() {
      $(this).click(() => {
          children.removeClass('active');                    
          $(this).addClass('active');
      });
  });
};

(async () => {
  $('#search_survey_btn').click(async () => {
      const index = ($('.pager #1').text() - 1) * 10;
      await fetchResponse(index);
      $('.pager #1').addClass('active');
  });
})()

const getSpecificResponse = async (id) => {
  $('div .modal .insert').empty();
  const surveyId = $('#search_survey').val();
  console.log(id, surveyId);
  const url = `http://127.0.0.1:5001/api/v1/response/${surveyId}/${id}`;
  let cookie = document.cookie;
  cookie = cookie.split('=')[1]

  await $.ajax({
      type: 'GET',
      url: url,
      xhrFields: {
          withCredentials: true,
      },
      headers: {
          "Content-Type": "application/json",
          'custom-header': cookie
      },
      contentType: "application/json",
      success: data => {
          const obj = JSON.parse(data.response);
          console.log(obj);
          for (let x in obj) {
              $('div .modal .insert').append(`<p><span>${x}:</span></p>`);
              $('div .modal .insert').append(`<p id=answer>${obj[x]}</p>`);
          }
      },
      error: (xhr, status, error) => {
          $('tr').children('td').remove();
          alert(`Error code: ${status}, Massage: ${error}`);
      },
      dataType: "json",
  })

  $('div .modal').css({'display': 'block'});
  $('div .modal').animate({'opacity': '1'}, 500)
  $('div .modal').append(`<a id=close href=# onClick=hideModal()>Close</a>`);
  $('.response_search').css({'filter': 'blur(5px)'});
  $('.response_search').slideUp();
  $('.response table').css({'filter': 'blur(5px)'});
}

const hideModal = () => {
  $('.response_search').css({'filter': 'blur(0px)'});
  $('.response table').css({'filter': 'blur(0px)'});
  $('.response_search').slideDown();
  $('div .modal').animate({'transform': 'scale(0)'}, 1000)
  $('div .modal').css({'display': 'none'});
  $('div .modal a').remove();
}