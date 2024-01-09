$(document).ready(() => {

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

});

//     <input type="text" name=${questionId} class=${questionId} id=question-box placeholder="${placeholder}"><br><br>
